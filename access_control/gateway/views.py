from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_POST
from .forms_auth.registrations_forms import SchoolRegistrationForm
from .models import School
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
import logging
logger = logging.getLogger(__name__)
from django.contrib.auth import get_user_model
from django.contrib.auth import logout
import random
import string
from django.utils import timezone
from django.contrib.auth.decorators import login_required
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content

# Create your views here.
# Generate a 6-digit OTP
def generate_otp():
    return ''.join(random.choices(string.digits, k=6))


def logins(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)

            # Check if user has completed setup
            if not user.is_setup_complete:

                # Redirect to the animation page if the setup is incomplete
                return redirect('gateway:setup_wizard')
                #return redirect('gateway:animation_page')
            
            else:

                # Redirect to the main service page if setup is complete
                return redirect('moderators_service:moderators_service_page')
        else:
            return render(request, 'logins.html', {'error': 'Invalid email or password'})

    return render(request, 'logins.html')



def animation_page(request):
    # Assuming the user is authenticated and has a related school
    if request.user.is_authenticated and hasattr(request.user, 'admin'):

        school_name = request.user.admin.school.name  # Accessing the related School name
    else:
        school_name = "Your School Name"

    return render(request, 'new_login_animation.html', {'school_name': school_name})

   

def logout_view(request):
    logout(request)
    return redirect('gateway:logins')





logger = logging.getLogger(__name__)
def generate_otp():
    return ''.join(random.choices(string.digits, k=6))

from django.conf import settings

def school_registration(request):
    if request.method == 'POST':
        form = SchoolRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            school = form.save(commit=False)
            school.population = None
            school.year_established = None
            try:
                school.save()
                User = get_user_model()
                user = User.objects.create_user(
                    username=school.email,
                    email=school.email,
                    password=form.cleaned_data['password'],
                    school=school,
                    is_setup_complete=False
                )
                otp = generate_otp()
                request.session['otp'] = otp
                request.session['email'] = school.email
                request.session['otp_expiry'] = 300
                request.session['otp_creation_time'] = timezone.now().timestamp()

                # Debug API key
                api_key = settings.SENDGRID_API_KEY
                print(f"Loaded API Key: {api_key}")
                sg = SendGridAPIClient(api_key)
                from_email = Email(settings.EMAIL_HOST_USER)
                to_email = To(school.email)
                subject = "Your Frankfurt School Manager OTP"
                content = Content("text/plain", f"Your OTP is {otp}. It expires in 5 minutes.")
                mail = Mail(from_email, to_email, subject, content)
                response = sg.send(mail)
                logger.info(f"OTP email sent to {school.email}, response: {response.status_code}")

                return redirect(reverse('gateway:setup_welcome'))
            except Exception as e:
                logger.error(f"Error during user creation: {str(e)}", exc_info=True)
                messages.error(request, "An error occurred. Please try again.")
    else:
        form = SchoolRegistrationForm()
    return render(request, 'school_registration.html', {'form': form})






from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
import logging

logger = logging.getLogger(__name__)

@login_required
def setup_wizard(request):
    user = request.user
    step = int(request.GET.get('step', 1))
    progress = (step / 3) * 100

    if request.method == 'POST':
        if step == 1:
            other_names = request.POST.get('other_names')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            phone_number = request.POST.get('phone_number')
            photo = request.FILES.get('photo')
            if last_name and email and phone_number:  # other_names and photo are optional
                user.other_names = other_names
                user.last_name = last_name
                user.email = email
                user.phone_number = phone_number
                if photo:
                    user.photo = photo
                user.user_type = 'admin'  # Set as principal
                user.save()
                messages.success(request, "Profile saved!")
                return redirect(f'/gateway/setup-wizard/?step=2')
            else:
                messages.error(request, "Please fill all required fields (Last Name, Email, Phone).")
        elif step == 2:
            school = user.school
            population = request.POST.get('population')
            year_established = request.POST.get('year_established')
            registration_number = request.POST.get('registration_number')
            number_of_classrooms = request.POST.get('number_of_classrooms')
            number_of_teachers = request.POST.get('number_of_teachers')
            levels = request.POST.get('levels')
            facilities = request.POST.get('facilities')
            if (population and year_established and registration_number and number_of_classrooms and
                number_of_teachers and levels and facilities):
                school.population = int(population)
                school.year_established = int(year_established)
                school.registration_number = registration_number
                school.number_of_classrooms = int(number_of_classrooms)
                school.number_of_teachers = int(number_of_teachers)
                school.levels = levels
                school.facilities = facilities
                school.save()
                messages.success(request, "School config saved!")
                return redirect(f'/gateway/setup-wizard/?step=3')
            else:
                messages.error(request, "Please fill all required fields.")
        elif step == 3:
            user.is_principal = True  # Ensure User model has is_principal field
            user.is_setup_complete = True
            user.save()
            messages.success(request, "Setup complete!")
            return redirect(reverse('gateway:logins'))

    context = {'step': step, 'progress': progress}
    if step == 1:
        context.update({'user': user})
    elif step == 2:
        context.update({'school': user.school})
    elif step == 3:
        context.update({'user': user, 'school': user.school})
    return render(request, 'setup_wizard.html', context)








def setup_welcome(request):
    email = request.session.get('email')  # Get email from session on GET
    if request.method == 'POST':
        user_otp = request.POST.get('otp')
        stored_otp = request.session.get('otp')
        email = request.session.get('email') 
        expiry = request.session.get('otp_expiry', 0)

        if stored_otp and user_otp == stored_otp and (timezone.now().timestamp() - request.session.get('otp_creation_time', 0)) < expiry:
            del request.session['otp']
            del request.session['email']
            del request.session['otp_expiry']
            del request.session['otp_creation_time']
            messages.success(request, "Email verified! Starting setup...")
            return redirect(reverse('gateway:setup_wizard'))
        else:
            messages.error(request, "Invalid or expired OTP. Please try again or resend.")

    # Store OTP creation time on GET if not set
    if 'otp_creation_time' not in request.session and email:
        request.session['otp_creation_time'] = timezone.now().timestamp()
        logger.info(f"OTP {request.session.get('otp')} sent to {email} - implement SendGrid here")

    return render(request, 'setup_welcome.html')

#Success page view
def school_registration_success(request):
    return render(request, 'school_registration_success.html')