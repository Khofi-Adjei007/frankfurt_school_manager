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

            # Check for duplicates by school name
            school_name = form.cleaned_data.get('name')
            if School.objects.filter(name=school_name).exists():
                messages.error(request, "A school with this name already exists. Please choose a different name.")
            else:
                
                # If no duplicates, save the form
                form.save()
                messages.success(request, "School registered successfully!") 

                # Clear the form by creating a new instance
                form = SchoolRegistrationForm()

                # Redirect to the success page
                return redirect(reverse('school_registration_success'))
        else:

            # If the form is invalid, print this errors for debugging
            print(form.errors)
            messages.error(request, "There were some errors in your submission. Please correct them.")
    else:
        form = SchoolRegistrationForm()
    
    return render(request, 'school_registration.html', {'form': form})







#Success page view
def school_registration_success(request):
    return render(request, 'school_registration_success.html')