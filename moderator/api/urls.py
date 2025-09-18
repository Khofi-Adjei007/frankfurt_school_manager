from django.urls import path
from django.http import JsonResponse

def ping_view(request):
    return JsonResponse({"status": "moderators api ok"})

urlpatterns = [
    path("ping/", ping_view, name="moderators-ping"),
]
