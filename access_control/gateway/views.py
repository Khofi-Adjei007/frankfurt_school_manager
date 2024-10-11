from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_POST
from .forms_auth.registrations_forms import SchoolRegistrationForm
from .models import School
from django.urls import reverse



# Create your views here.
def logins(request):
    return render(request, "logins.html")



def school_registration(request):
    if request.method == 'POST':
        form = SchoolRegistrationForm(request.POST, request.FILES)

        if form.is_valid():
            # If no validation errors, save the form
            form.save()
            messages.success(request, "School registered successfully!")
            return redirect(reverse('school_registration_success'))

        else:
            # If the form is invalid, Django will automatically include error messages in the form
            messages.error(request, "There were errors in your submission. Please correct them and try again.")

    else:
        # Display a blank form for a GET request
        form = SchoolRegistrationForm()

    return render(request, 'school_registration.html', {'form': form})








#Success page view
def school_registration_success(request):
    return render(request, 'school_registration_success.html')