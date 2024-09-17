from django.shortcuts import render
from . import urls




# Create your views here.
def logins(request):
    return render(request, "logins.html")


def create_school(request):
    return render(request, "new_school_instance.html")
