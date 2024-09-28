from django.shortcuts import render

# Create your views here.
def explore_school(request):
    return render(request, 'explore_school.html')