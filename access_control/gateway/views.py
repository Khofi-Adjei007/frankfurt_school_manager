from django.shortcuts import render
from . import urls




# Create your views here.
def logins(request):
    return render(request, "logins.html")


def school_registration(request):
    return render(request, "school_registrations.html")

def service_homepage(request):
    return render(request, "service_homepage.html")