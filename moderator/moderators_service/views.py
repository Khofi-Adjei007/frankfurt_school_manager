from django.shortcuts import render, redirect
from . import urls
from .AdminSettingsForm import AdminSettingsForm
from access_control.gateway.models import School
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .admin_roles_decorator import role_required
from .AdminAndSchoolSetupForm import AdminAndSchoolSetupForm
from .models import Admin


@login_required(login_url='/gateway/logins/')
def moderators_service_page(request):
    user = request.user 
    school = get_object_or_404(School, id=user.school_id)

    context = {
        'school_name': school.name,
        'user_role': 'Admin',
    }
    return render(request, "moderators_service_page.html", context)



@login_required(login_url='/gateway/logins/')
def admissions_and_registrations(request):
    return render(request, "admissions_and_registrations.html")

@login_required(login_url='/gateway/logins/')
def settings_page(request):

    # Handle both forms in the same view
    admin_settings_form = AdminSettingsForm()
    admin_school_setup_form = AdminAndSchoolSetupForm()

    if request.method == 'POST':
        if 'admin_settings' in request.POST:
            admin_settings_form = AdminSettingsForm(request.POST, request.FILES)
            if admin_settings_form.is_valid():

                # Save admin data like in admin_settings view
                return redirect('success_page')

        elif 'admin_school_setup' in request.POST:
            admin_school_setup_form = AdminAndSchoolSetupForm(request.POST, request.FILES)
            if admin_school_setup_form.is_valid():

                # Save admin and school data like in admin_and_school_setup view
                admin_instance = Admin(
                    first_name=admin_school_setup_form.cleaned_data['first_name'],
                    middle_name=admin_school_setup_form.cleaned_data['middle_name'],
                    last_name=admin_school_setup_form.cleaned_data['last_name'],
                    email=admin_school_setup_form.cleaned_data['email'],
                    phone_number=admin_school_setup_form.cleaned_data['phone_number'],
                    photo=admin_school_setup_form.cleaned_data['photo']
                )
                admin_instance.save()

                school_instance = School(
                    logo=admin_school_setup_form.cleaned_data['logo'],
                    motto=admin_school_setup_form.cleaned_data['motto'],
                    govt_registration_number=admin_school_setup_form.cleaned_data['govt_registration_number'],
                    social_media_links=admin_school_setup_form.cleaned_data['social_media_links'],
                    number_of_teachers=admin_school_setup_form.cleaned_data['number_of_teachers'],
                    number_of_other_staff=admin_school_setup_form.cleaned_data['number_of_other_staff'],
                    number_of_classrooms=admin_school_setup_form.cleaned_data['number_of_classrooms'],
                    curriculum_types=admin_school_setup_form.cleaned_data['curriculum_types'],
                    board_of_directors=admin_school_setup_form.cleaned_data['board_of_directors'],
                    admin=admin_instance
                )
                school_instance.save()

                return redirect('success_page')

    return render(request, 'settings_page.html', {
        'admin_settings_form': admin_settings_form,
        'admin_school_setup_form': admin_school_setup_form
    })



def information_admin_page(request):
    return render(request, 'IT_admin/information_admin_page.html')
 