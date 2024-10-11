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

        # Check if the form is valid
        if form.is_valid():
            
            # Get the cleaned data from the form
            school_name = form.cleaned_data.get('name')
            digital_address = form.cleaned_data.get('digital_address')
            physical_address = form.cleaned_data.get('physical_address')
            official_telephone_number = form.cleaned_data.get('official_telephone_number')
            email = form.cleaned_data.get('email')

            # Check if any school has the same name, email, phone, digital address, or physical address
            if School.objects.filter(
                name=school_name
            ).exists():
                messages.error(request, "A school with this name already exists. Please choose a different name.")
            elif School.objects.filter(
                email=email
            ).exists():
                messages.error(request, "A school with this email already exists. Please use a different email.")
            elif School.objects.filter(
                official_telephone_number=official_telephone_number
            ).exists():
                messages.error(request, "A school with this phone number already exists. Please use a different phone number.")
            elif School.objects.filter(
                digital_address=digital_address
            ).exists():
                messages.error(request, "A school with this digital address already exists. Please use a different digital address.")
            elif School.objects.filter(
                physical_address=physical_address
            ).exists():
                messages.error(request, "A school with this physical address already exists. Please use a different physical address.")
            else:
                # If no duplicates found, save the school data
                form.save()
                messages.success(request, "School registered successfully!")

                # Redirect to the success page and clear the form
                return redirect(reverse('school_registration_success'))

        else:
            # If the form is invalid, show errors to the user
            messages.error(request, "There were errors in your submission. Please correct them and try again.")

    else:
        # Display a blank form when the page is first loaded
        form = SchoolRegistrationForm()

    # Render the form with the current state
    return render(request, 'school_registration.html', {'form': form})








#Success page view
def school_registration_success(request):
    return render(request, 'school_registration_success.html')