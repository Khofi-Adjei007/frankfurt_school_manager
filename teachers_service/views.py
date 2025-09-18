from django.shortcuts import render
from rest_framework.decorators import api_view



# Create your views here.
def teachers_service_page(request):
    return render (request, "teachers_service.html")

