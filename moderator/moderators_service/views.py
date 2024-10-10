from django.shortcuts import render, redirect
from . import urls
from . import AdminSettingsForm



def moderators_service_page(request):
    return render(request, "moderators_service_page.html")


def admissions_and_registrations(request):
    return render(request, "admissions_and_registrations.html")


def settings_page(request):
    if request.method == 'POST':
        form = AdminSettingsForm(request.POST, request.FILES)
        if form.is_valid():
            # Here you would save the form data to the database or process it as needed
            return redirect('success_page')  # Redirect to a success page or reload the settings page
    else:
        form = AdminSettingsForm()

    return render(request, 'settings_page.html', {'form': form})