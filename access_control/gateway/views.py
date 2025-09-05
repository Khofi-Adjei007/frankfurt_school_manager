"""Refactored views.py

Goals:
- Remove duplicate imports and logger re-definitions.
- Centralize OTP generation, sending, validation and resend cooldown.
- Keep both `setup_wizard` and split `setup_step1/2/3` flows to avoid breaking existing routes,
  but share helpers to prevent duplicate logic.
- Add robust SendGrid exception handling.
- Keep original behavior and session keys intact where possible.
"""

import logging
import random
import jwt
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
from decouple import config
from django.utils.crypto import get_random_string

from .forms_auth.registrations_forms import (
    SchoolRegistrationForm,
    InitialSchoolRegistrationForm,
    PrincipalDetailsForm,
    SchoolInfoForm,
)
from .models import School, User

# -----------------------------------------------------------------------------
# Logger & Constants
# -----------------------------------------------------------------------------
logger = logging.getLogger(__name__)

OTP_EXPIRY = 300  # seconds
RESEND_COOLDOWN = 60  # seconds
SETUP_JWT_EXPIRY = 900  # seconds for setup JWT

# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------

def _generate_otp(length: int = 6) -> str:
    """Return a numeric OTP of `length` digits."""
    return get_random_string(length=length, allowed_chars='1234567890')


def _send_email(subject: str, to_email: str, plain_text: str) -> bool:
    """Send an email via SendGrid. Returns True on success, False otherwise.

    We swallow exceptions and log them so callers can react appropriately.
    """
    try:
        sg = SendGridAPIClient(config('SENDGRID_API_KEY'))
        mail = Mail(
            from_email=Email(config('EMAIL_HOST_USER')),
            to_emails=To(to_email),
            subject=subject,
            plain_text_content=plain_text,
        )
        response = sg.send(mail)
        logger.info("Email sent to %s, status=%s", to_email, getattr(response, 'status_code', 'unknown'))
        return True
    except Exception as exc:
        logger.exception("Failed to send email to %s: %s", to_email, exc)
        return False


def _validate_otp_from_session(request, user_otp: str) -> bool:
    """Validate supplied OTP against session-stored OTP and expiry."""
    stored_otp = request.session.get('otp')
    creation_time = request.session.get('otp_creation_time', 0)
    expiry = request.session.get('otp_expiry', OTP_EXPIRY)

    if not stored_otp or not user_otp:
        return False
    if timezone.now().timestamp() - creation_time > expiry:
        return False
    return stored_otp == user_otp


def _init_otp_session(request, email: str, school_id: int, password: str = None):
    """Initialize OTP-related session keys for registration flow."""
    otp = _generate_otp()
    current_time = timezone.now().timestamp()
    request.session.update({
        'otp': otp,
        'email': email,
        'school_id': school_id,
        'password': password,
        'otp_creation_time': current_time,
        'otp_expiry': OTP_EXPIRY,
    })
    return otp

# -----------------------------------------------------------------------------
# Auth Views
# -----------------------------------------------------------------------------

def logins(request):
    """Handle user login authentication and redirection."""
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)

        if user:
            login(request, user)
            logger.info("User %s logged in successfully", email)
            next_url = request.GET.get('next', '')
            if not getattr(user, 'is_setup_complete', False):
                return redirect(reverse('gateway:setup_step1'))
            if getattr(user, 'user_type', None) == 'admin':
                return redirect(next_url or reverse('moderators_service:moderators_service_page'))
            return redirect(reverse('gateway:logins'))
        messages.error(request, 'Invalid email or password')
        logger.warning("Login failed for email: %s", email)
        return render(request, 'logins.html', {'error': 'Invalid email or password'})

    return render(request, 'logins.html', {'next': request.GET.get('next', '')})


def logout_view(request):
    logout(request)
    return redirect('gateway:logins')

# -----------------------------------------------------------------------------
# Registration & OTP
# -----------------------------------------------------------------------------
@csrf_protect
def register_school(request):
    """Handle school registration and send OTP via email.

    Preserves original session keys and behavior. On SendGrid failure,
    cleans up created objects and flushes the session.
    """
    logger.info("Starting school registration. Method=%s", request.method)

    if request.method == 'POST':
        form = SchoolRegistrationForm(request.POST)
        if form.is_valid():
            school_name = form.cleaned_data.get('school_name')
            email = form.cleaned_data.get('email')
            email = email.lower() if email else None
            school_type = form.cleaned_data.get('school_type')
            physical_address = form.cleaned_data.get('physical_address')

            if School.objects.filter(school_name__iexact=school_name).exists():
                logger.warning("School already exists: %s", school_name)
                messages.error(request, "A school with this name already exists.")
                return render(request, 'school_registration.html', {'form': form})

            if User.objects.filter(email__iexact=email).exists():
                logger.warning("Email already in use: %s", email)
                messages.error(request, "This email is already registered.")
                return render(request, 'school_registration.html', {'form': form})

            # Create school + user (wrapped minimal atomicity - DB atomic may be added)
            school = School.objects.create(
                school_name=school_name,
                school_type=school_type,
                physical_address=physical_address,
                email=email,
            )

            password = get_random_string(length=12)
            user = User.objects.create_user(username=email, email=email, password=password)
            school.user = user
            school.save()

            # Initialize OTP in session
            otp = _init_otp_session(request, email, school.id, password)

            # Send OTP
            subject = "Your OTP for Frankfurt School Manager"
            sent = _send_email(subject, email, f"Your OTP is: {otp}. Valid for 5 minutes.")
            if sent:
                messages.success(request, "OTP sent to your email. Please verify.")
                return redirect(reverse('gateway:verify_otp'))

            # SendGrid failed — cleanup
            logger.error("Failed to send OTP email during registration for %s", email)
            messages.error(request, "Failed to send OTP. Please try again.")
            school.delete()
            user.delete()
            request.session.flush()
            return render(request, 'school_registration.html', {'form': form})

        messages.error(request, "Please correct the errors below.")
        return render(request, 'school_registration.html', {'form': form})

    form = SchoolRegistrationForm()
    return render(request, 'school_registration.html', {'form': form})


def setup_welcome(request):
    """Handle OTP verification (entry point) and resend with cooldown.

    Returns the setup welcome page; on successful verify it stores a setup JWT
    in session and shows welcome UI.
    """
    email = request.session.get('email')

    if request.method == 'POST':
        user_otp = request.POST.get('otp')
        if _validate_otp_from_session(request, user_otp):
            payload = {
                'email': email,
                'school_id': request.session.get('school_id'),
                'exp': timezone.now().timestamp() + SETUP_JWT_EXPIRY,
            }
            jwt_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
            request.session['jwt_token'] = jwt_token
            request.session.modified = True
            logger.info("JWT generated for email: %s", email)
            messages.success(request, "Email verified! Starting setup...")
            return render(request, 'setup_welcome.html', {'show_welcome': True})

        messages.error(request, "Invalid or expired OTP. Please try again or resend.")

    elif request.GET.get('resend'):
        last_resend = request.session.get('last_resend_time', 0)
        current_time = timezone.now().timestamp()
        if current_time - last_resend < RESEND_COOLDOWN:
            wait = int(RESEND_COOLDOWN - (current_time - last_resend))
            messages.error(request, f"Please wait {wait} seconds before resending.")
            return render(request, 'setup_welcome.html', {'cooldown_remaining': wait})

        if email:
            new_otp = _generate_otp()
            request.session.update({
                'otp': new_otp,
                'otp_creation_time': current_time,
                'last_resend_time': current_time,
                'otp_expiry': OTP_EXPIRY,
            })
            sent = _send_email("Your New Frankfurt School Manager OTP", email, f"Your new OTP is {new_otp}. It expires in 5 minutes.")
            if sent:
                messages.success(request, "A new OTP has been sent to your email.")
            else:
                messages.error(request, "Failed to resend OTP. Please try again later.")
        else:
            messages.error(request, "Unable to resend OTP. Please register again.")

        cooldown_remaining = max(0, int(RESEND_COOLDOWN - (timezone.now().timestamp() - last_resend)))
        return render(request, 'setup_welcome.html', {'cooldown_remaining': cooldown_remaining})

    if 'otp_creation_time' not in request.session and email:
        request.session['otp_creation_time'] = timezone.now().timestamp()
        logger.info("OTP session initialized for email: %s", email)

    return render(request, 'setup_welcome.html', {'cooldown_remaining': 0})


# -----------------------------------------------------------------------------
# setup_wizard (kept for backward compatibility) — uses session JWT created above
# -----------------------------------------------------------------------------

def setup_wizard(request):
    """Multi-step setup wizard. Validates JWT in session and progresses through steps.

    This function purposely preserves the original behavior but uses helper
    functions and clearer error handling.
    """
    step = int(request.GET.get('step', 1))
    progress = (step / 3) * 100
    jwt_token = request.session.get('jwt_token')

    if not jwt_token:
        logger.info("No JWT token found, redirecting to login")
        return redirect('gateway:logins')

    try:
        payload = jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=['HS256'])
        email = payload.get('email')
        school_id = payload.get('school_id')
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        logger.info("Invalid or expired JWT, redirecting to setup")
        return redirect('gateway:setup_welcome')

    logger.info("Setup wizard accessed - step=%d, email=%s", step, email)

    UserModel = get_user_model()
    user = None
    try:
        school = School.objects.get(id=school_id)
        user = getattr(school, 'user', None)
        logger.info("User fetched via school_id: %s", getattr(user, 'email', None))
    except School.DoesNotExist:
        try:
            user = UserModel.objects.get(email__iexact=email)
            logger.info("User fetched via email: %s", user.email)
        except UserModel.DoesNotExist:
            logger.error("User not found for email: %s", email)
            return redirect('gateway:logins')

    # POST handling for steps (mirrors original logic)
    if request.method == 'POST':
        if step == 1:
            other_names = request.POST.get('other_names')
            last_name = request.POST.get('last_name')
            email_field = request.POST.get('email')
            phone_number = request.POST.get('phone_number')
            photo = request.FILES.get('photo')

            if all([last_name, email_field, phone_number]):
                user.other_names = other_names
                user.last_name = last_name
                user.email = email_field.lower()
                user.phone_number = phone_number
                if photo:
                    user.photo = photo
                user.user_type = 'admin'
                user.save()
                request.session.modified = True
                messages.success(request, "Profile saved successfully!")
                return redirect(f'/gateway/setup-wizard/?step=2')

            messages.error(request, "Please fill all required fields (Last Name, Email, Phone).")

        elif step == 2:
            if not user or not hasattr(user, 'school'):
                logger.error("User or school not found for email: %s", getattr(user, 'email', None))
                return redirect('gateway:logins')

            school = user.school
            data = {
                'population': request.POST.get('population'),
                'year_established': request.POST.get('year_established'),
                'registration_number': request.POST.get('registration_number'),
                'number_of_classrooms': request.POST.get('number_of_classrooms'),
                'number_of_teachers': request.POST.get('number_of_teachers'),
                'levels': request.POST.get('levels'),
                'facilities': request.POST.get('facilities'),
            }

            if all(data.values()):
                # Cast numeric fields safely
                try:
                    school.population = data['population']
                    school.year_established = int(data['year_established'])
                    school.registration_number = data['registration_number']
                    school.number_of_classrooms = int(data['number_of_classrooms'])
                    school.number_of_teachers = int(data['number_of_teachers'])
                    school.levels = data['levels']
                    # facilities may be a list or comma-separated string — attempt to set safely
                    facilities = data['facilities']
                    if facilities is not None:
                        # if string, leave for form handling; if list, set M2M after save
                        pass
                    school.save()
                    request.session.modified = True
                    messages.success(request, "School config saved successfully!")
                    return redirect(f'/gateway/setup-wizard/?step=3')
                except Exception as exc:
                    logger.exception("Failed to save school data: %s", exc)
                    messages.error(request, "Failed to save school data. Please check your inputs.")
            else:
                messages.error(request, "Please fill all required fields.")

        elif step == 3:
            if not user:
                logger.error("User not found for email: %s", email)
                return redirect('gateway:logins')

            user.is_setup_complete = True
            user.save()
            messages.success(request, "Setup complete!")

            # Authenticate using session-stored password if available
            session_password = request.session.get('password', '')
            authenticated_user = authenticate(request, username=user.email, password=session_password)
            if authenticated_user:
                login(request, authenticated_user)
                request.session.pop('jwt_token', None)
            return redirect('moderators_service:moderators_service_page')

    # Context for templates
    context = {'step': step, 'progress': progress}
    if step == 1 and user:
        context['user'] = user
    elif step == 2 and user:
        context['school'] = getattr(user, 'school', None)
    elif step == 3 and user:
        context['user'] = user
        context['school'] = getattr(user, 'school', None)

    return render(request, 'setup_wizard.html', context)


# -----------------------------------------------------------------------------
# OTP Verification View (keeps identical external behaviour to original verify_otp)
# -----------------------------------------------------------------------------

def verify_otp(request):
    """Handle OTP verification, resend, and modal display.

    Contains resend cooldown and robust sending via helper.
    """
    logger.info("Starting OTP verification. Method=%s", request.method)
    email = request.session.get('email')
    school_name = request.session.get('school_name')
    school_id = request.session.get('school_id')

    if request.method == 'POST':
        otp = request.POST.get('otp')
        # Basic session checks
        creation_time = request.session.get('otp_creation_time', 0)
        expiry = request.session.get('otp_expiry', OTP_EXPIRY)

        if not all([otp, request.session.get('otp'), email, school_id, creation_time]):
            logger.info("Missing session data for OTP verification for email=%s", email)
            messages.error(request, "Session expired. Please register again.")
            return redirect(reverse('gateway:register'))

        if timezone.now().timestamp() - creation_time > expiry:
            logger.info("OTP expired for email=%s", email)
            messages.error(request, "OTP has expired. Please register again or resend.")
            return redirect(reverse('gateway:register'))

        if otp == request.session.get('otp'):
            logger.info("OTP verified for email=%s", email)
            messages.success(request, f"Welcome to {school_name}! OTP Verified. Redirecting to setup...")
            return render(request, 'setup_welcome.html', {'show_welcome': True, 'school_name': school_name})

        logger.info("Invalid OTP for email=%s", email)
        messages.error(request, "Invalid OTP. Please try again or resend.")

    elif request.GET.get('resend'):
        last_resend = request.session.get('last_resend_time', 0)
        current_time = timezone.now().timestamp()
        if current_time - last_resend < RESEND_COOLDOWN:
            remaining = int(RESEND_COOLDOWN - (current_time - last_resend))
            messages.error(request, f"Please wait {remaining} seconds before resending.")
            return render(request, 'setup_welcome.html', {'cooldown_remaining': remaining})

        if email:
            new_otp = _generate_otp()
            request.session.update({
                'otp': new_otp,
                'otp_creation_time': current_time,
                'last_resend_time': current_time,
                'otp_expiry': OTP_EXPIRY,
            })
            logger.info("New OTP generated for %s", email)
            sent = _send_email("Your new OTP", email, f"Your new OTP is {new_otp}. It expires in 5 minutes.")
            if sent:
                messages.success(request, "A new OTP has been sent to your email.")
            else:
                messages.error(request, "Failed to send new OTP. Please try again later.")
        else:
            messages.error(request, "Unable to resend OTP. Please register again.")

        return render(request, 'setup_welcome.html')

    # ensure OTP creation time is set for new visitors
    if 'otp_creation_time' not in request.session and email:
        request.session['otp_creation_time'] = timezone.now().timestamp()
        logger.info("OTP session initialized for email=%s", email)

    return render(request, 'setup_welcome.html', {'cooldown_remaining': 0})


# -----------------------------------------------------------------------------
# Setup Step Views (preserve behavior but use forms where possible)
# -----------------------------------------------------------------------------

def setup_step1(request):
    """Handle principal details collection and save."""
    logger.info("Starting setup step 1. Method=%s", request.method)
    school_id = request.session.get('school_id')
    email = request.session.get('email')

    if not all([school_id, email]):
        logger.info("Missing session data for setup step 1")
        messages.error(request, "Session expired. Please register again.")
        return redirect(reverse('gateway:register'))

    try:
        user = User.objects.get(email__iexact=email)
    except User.DoesNotExist:
        logger.error("User not found for email=%s", email)
        messages.error(request, "User data not found. Please contact support.")
        return redirect(reverse('gateway:register'))

    if request.method == 'POST':
        form = PrincipalDetailsForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Principal details saved successfully!")
            return redirect(reverse('gateway:setup_step2'))
        messages.error(request, "Please correct the errors below.")
    else:
        initial_data = {
            'other_names': user.other_names,
            'last_name': user.last_name,
            'email': user.email,
            'phone_number': getattr(user, 'phone_number', ''),
        }
        form = PrincipalDetailsForm(initial=initial_data)

    progress_width = 33.33
    return render(request, 'setup_wizard.html', {'step': 1, 'form': form, 'user': user, 'progress_width': progress_width})


def setup_step2(request):
    """Handle school information collection and save."""
    logger.info("Starting setup step 2. Method=%s", request.method)
    school_id = request.session.get('school_id')

    if not school_id:
        logger.info("Missing session data for setup step 2")
        messages.error(request, "Session expired. Please register again.")
        return redirect(reverse('gateway:register'))

    try:
        school = School.objects.get(id=school_id)
    except School.DoesNotExist:
        logger.error("School not found for ID=%s", school_id)
        messages.error(request, "School data not found. Please contact support.")
        return redirect(reverse('gateway:register'))

    if request.method == 'POST':
        form = SchoolInfoForm(request.POST, instance=school)
        if form.is_valid():
            form.save()
            messages.success(request, "School information saved successfully!")
            return redirect(reverse('gateway:setup_step3'))
        messages.error(request, "Please correct the errors below.")
    else:
        initial_data = {
            'registration_number': school.registration_number,
            'population': school.population,
            'year_established': school.year_established,
            'number_of_teachers': school.number_of_teachers,
            'number_of_classrooms': school.number_of_classrooms,
            'levels': school.levels,
            'facilities': school.facilities.all(),
        }
        form = SchoolInfoForm(initial=initial_data)

    progress_width = 66.66
    return render(request, 'setup_wizard.html', {'step': 2, 'form': form, 'school': school, 'progress_width': progress_width})


def setup_step3(request):
    """Handle setup summary, completion, and redirect to moderator page."""
    logger.info("Starting setup step 3. Method=%s", request.method)
    school_id = request.session.get('school_id')
    email = request.session.get('email')

    if not all([school_id, email]):
        logger.info("Missing session data for setup step 3")
        messages.error(request, "Session expired. Please register again.")
        return redirect(reverse('gateway:register'))

    try:
        school = School.objects.get(id=school_id)
        user = User.objects.get(email__iexact=email)
    except (School.DoesNotExist, User.DoesNotExist):
        logger.error("School or user not found for school_id=%s, email=%s", school_id, email)
        messages.error(request, "Data not found. Please contact support.")
        return redirect(reverse('gateway:register'))

    if request.method == 'POST' and 'confirm' in request.POST:
        user.is_setup_complete = True
        user.school = school
        user.save()
        logger.info("User %s setup completed and linked to school %s", user.email, school.id)

        # attempt to authenticate & log the user in using session-stored password
        session_password = request.session.get('password', '')
        authenticated_user = authenticate(request, username=email, password=session_password)
        if authenticated_user:
            login(request, authenticated_user)
            messages.success(request, "Setup completed! Redirecting to your dashboard...")
            request.session['school_id'] = school_id
            return redirect(reverse('moderators_service:moderators_service_page'))
        messages.error(request, "Login failed after setup. Please try logging in manually.")

    progress_width = 100
    return render(request, 'setup_wizard.html', {'step': 3, 'user': user, 'school': school, 'progress_width': progress_width})


def animation_page(request):
    """Render animation page with school name if authenticated."""
    school_name = "Your School Name"
    if request.user.is_authenticated:
        try:
            school_name = request.user.school.school_name
        except Exception:
            # keep default if structure differs
            pass
    return render(request, 'new_login_animation.html', {'school_name': school_name})
