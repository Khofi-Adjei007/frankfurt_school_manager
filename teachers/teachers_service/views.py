from django.shortcuts import render

# Create your views here.
def teachers_service_page(request):
    return render (request, "teachers_service.html")