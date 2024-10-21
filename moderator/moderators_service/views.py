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
    if request.method == 'POST':
        form = AdminSettingsForm(request.POST, request.FILES)
        if form.is_valid():
            return redirect('success_page')
    else:
        form = AdminSettingsForm()

    return render(request, 'settings_page.html', {'form': form})




def admin_and_school_setup(request):
    if request.method == 'POST':
        print("POST request received.")  # Debugging print
        form = AdminAndSchoolSetupForm(request.POST, request.FILES)

        if form.is_valid():
            print("Form is valid.")  # Debugging print

            # Save admin data
            admin_instance = Admin(
                first_name=form.cleaned_data['first_name'],
                middle_name=form.cleaned_data['middle_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                phone_number=form.cleaned_data['phone_number'],
                photo=form.cleaned_data['photo']
            )
            admin_instance.save()
            print("Admin instance saved.")  # Debugging print

            # Save school data
            school_instance = School(
                logo=form.cleaned_data['logo'],
                motto=form.cleaned_data['motto'],
                govt_registration_number=form.cleaned_data['govt_registration_number'],
                social_media_links=form.cleaned_data['social_media_links'],
                number_of_teachers=form.cleaned_data['number_of_teachers'],
                number_of_other_staff=form.cleaned_data['number_of_other_staff'],
                number_of_classrooms=form.cleaned_data['number_of_classrooms'],
                curriculum_types=form.cleaned_data['curriculum_types'],
                board_of_directors=form.cleaned_data['board_of_directors'],
                admin=admin_instance  # Link to the admin instance
            )
            school_instance.save()
            print("School instance saved.")  # Debugging print
            
            # Redirect to a success page or another view
            return redirect('success_page')  # Replace with your desired URL name

        else:
            print("Form is invalid.")  # Debugging print
            print(form.errors)  # Print form errors for debugging

    else:
        form = AdminAndSchoolSetupForm()  # Instantiate the form for GET request

    return render(request, 'settings_page.html', {'form': form})



