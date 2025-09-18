# teachers/api/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Health check
    path("ping/", views.ping_view, name="teachers-ping"),

    # Teachers service API
    path("service/", views.teachers_service_api, name="teachers-service-api"),
]
