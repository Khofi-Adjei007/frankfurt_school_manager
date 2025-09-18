
# Create your views here.
from django.shortcuts import render
from . import urls




def parents_service_page(request):
    return render(request, "parents_service_page.html")