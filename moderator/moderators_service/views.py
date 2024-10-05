from django.shortcuts import render
from . import urls



def moderators_service_page(request):
    return render(request, "moderators_service_page.html")


def admissions_and_registrations(request):
    return render(request, "admissions_and_registrations.html")