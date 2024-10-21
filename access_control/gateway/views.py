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
from time import sleep


# Create your views here.
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
                return redirect('gateway:animation_page')
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


# Set up logging
logger = logging.getLogger(__name__)

def school_registration(request):
    if request.method == 'POST':
        form = SchoolRegistrationForm(request.POST, request.FILES)

        if form.is_valid():
            # Create a School instance
            school = form.save(commit=False)  # Don't save to the database yet

            # Save the school first
            try:
                school.save()  # Now save the school instance
                User = get_user_model()

                # Create a User instance
                User = User.objects.create_user(
                    username=school.email,
                    email=school.email,
                    password=form.cleaned_data['password'],
                    school=school
                )

                messages.success(request, "School registered successfully!")
                return redirect(reverse('gateway:school_registration_success'))

            except Exception as e:
                # Log the error with traceback
                logger.error(f"Error occurred during user creation: {str(e)}", exc_info=True)
                messages.error(request, "An error occurred while creating the user. Please try again.")
        else:
            messages.error(request, "There were errors in your submission. Please correct them and try again.")

    else:
        form = SchoolRegistrationForm()

    return render(request, 'school_registration.html', {'form': form})





#Success page view
def school_registration_success(request):
    return render(request, 'school_registration_success.html')