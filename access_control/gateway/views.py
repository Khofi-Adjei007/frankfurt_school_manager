from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from .forms_auth.registrations_forms import SchoolRegistrationForm



# Create your views here.
def logins(request):
    return render(request, "logins.html")


def school_registration(request):
    if request.method == 'POST':
        form = SchoolRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('registration_success')
    else:
        form = SchoolRegistrationForm()
    return render(request, 'school_registration.html', {'form': form})
