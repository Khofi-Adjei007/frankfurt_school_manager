from django.shortcuts import render

# Create your views here.
def teachers_service(request):
    return render (request, "teachers_service.html")