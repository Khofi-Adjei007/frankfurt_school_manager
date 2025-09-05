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
    user = request.user
    # Check for school relationship
    if not hasattr(user, 'school') or not user.school:
        school_id = request.session.get('school_id')
        if not school_id:
            logger.error("No school_id in session for user: %s", user.email)
            raise Http404("No school associated with this account.")
        try:
            school = School.objects.get(id=school_id)
            # Optionally update user.school if missing (for future consistency)
            if not hasattr(user, 'school') or not user.school:
                user.school = school
                user.save()
                logger.info("Updated user %s school to %s", user.email, school_id)
        except School.DoesNotExist:
            logger.error("School not found for id: %s", school_id)
            raise Http404("No school associated with this account.")
    else:
        school = user.school

    context = {
        'school_name': school.school_name,  # Adjust to your School model field
        'user_role': 'Admin',
    }
    return render(request, "moderators_service_page.html", context)

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

    # Handle both forms in the same view
    admin_settings_form = AdminSettingsForm()
    admin_school_setup_form = AdminAndSchoolSetupForm()

    if request.method == 'POST':
        if 'admin_settings' in request.POST:
            admin_settings_form = AdminSettingsForm(request.POST, request.FILES, instance=user)
            if admin_settings_form.is_valid():
                admin_settings_form.save()
                logger.info("Admin settings updated for user: %s", user.email)
                return redirect('moderators_service:settings_page')  # Reload settings page
        elif 'admin_school_setup' in request.POST:
            admin_school_setup_form = AdminAndSchoolSetupForm(request.POST, request.FILES, instance=school)
            if admin_school_setup_form.is_valid():
                admin_school_setup_form.save()
                logger.info("School settings updated for school: %s", school.school_name)
                return redirect('moderators_service:settings_page')  # Reload settings page

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