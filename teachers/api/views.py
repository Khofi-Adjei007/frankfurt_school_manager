# teachers/api/views.py
from django.http import JsonResponse

def ping_view(request):
    return JsonResponse({"status": "teachers api ok"})

def teachers_service_api(request):
    return JsonResponse({"message": "Teachers service API working!"})
