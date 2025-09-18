from django.shortcuts import render, redirect
from . import urls
from .AdminSettingsForm import AdminSettingsForm
from access_control.gateway.models import School
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .admin_roles_decorator import role_required
from .AdminAndSchoolSetupForm import AdminAndSchoolSetupForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404
from access_control.gateway.models import School, User
import logging



logger = logging.getLogger(__name__)
@login_required(login_url='/gateway/logins/')
def moderators_service_page(request):
    """
    Render the moderator home page with user and school information.

    Args:
        request: HTTP request object

    Returns:
        Rendered moderator home template with context

    Raises:
        Http404: If no school is associated with the user
    """
    user = request.user

    # Fetch or assign school based on user relationship
    school = None
    if hasattr(user, 'school') and user.school:
        school = user.school
        logger.debug("Fetched school %s from user relationship for user: %s", school.school_name, user.email)
    else:
        school_id = request.session.get('school_id')
        if school_id:
            try:
                school = School.objects.get(id=school_id)
                # Update user.school if missing (for consistency)
                if not hasattr(user, 'school') or not user.school:
                    user.school = school
                    user.save()
                    logger.info("Updated user %s school to %s", user.email, school_id)
            except School.DoesNotExist:
                logger.error("School not found for id: %s for user: %s", school_id, user.email)
                raise Http404("No school associated with this account.")
        else:
            logger.error("No school_id in session and no school relationship for user: %s", user.email)
            raise Http404("No school associated with this account.")

    # Determine user role dynamically
    user_role = 'Admin' if user.is_superuser else 'Moderator'  # Adjust based on your role model if exists

    # Prepare context
    context = {
        'user_role': user_role,
        'school_name': school.school_name,
    }

    return render(request, "moderators_service_page.html", context)

# Other views remain unchanged for now, but can be standardized later
@login_required(login_url='/gateway/logins/')
def admissions_and_registrations(request):
    user = request.user
    if not hasattr(user, 'school') or not user.school:
        logger.error("No school associated with user: %s", user.email)
        raise Http404("No school associated with this account.")
    school = user.school

    context = {
        'school_name': school.school_name,
    }
    return render(request, "admissions_and_registrations.html", context)

@login_required(login_url='/gateway/logins/')
def settings_page(request):
    user = request.user
    if not hasattr(user, 'school') or not user.school:
        logger.error("No school associated with user: %s", user.email)
        raise Http404("No school associated with this account.")
    school = user.school

    admin_settings_form = AdminSettingsForm()
    admin_school_setup_form = AdminAndSchoolSetupForm()

    if request.method == 'POST':
        if 'admin_settings' in request.POST:
            admin_settings_form = AdminSettingsForm(request.POST, request.FILES, instance=user)
            if admin_settings_form.is_valid():
                admin_settings_form.save()
                logger.info("Admin settings updated for user: %s", user.email)
                return redirect('moderators_service:settings_page')
        elif 'admin_school_setup' in request.POST:
            admin_school_setup_form = AdminAndSchoolSetupForm(request.POST, request.FILES, instance=school)
            if admin_school_setup_form.is_valid():
                admin_school_setup_form.save()
                logger.info("School settings updated for school: %s", school.school_name)
                return redirect('moderators_service:settings_page')

    context = {
        'admin_settings_form': admin_settings_form,
        'admin_school_setup_form': admin_school_setup_form,
        'school_name': school.school_name,
    }
    return render(request, 'settings_page.html', context)

def information_admin_page(request):
    return render(request, 'IT_admin/information_admin_page.html')

def financeAndAccounts(request):
    return render(request, 'AccountsAndFinance/financeAdmin.html')