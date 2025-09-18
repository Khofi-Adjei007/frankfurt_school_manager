# teachers/urls.py
from django.urls import path, include
from . import views

urlpatterns = [
    # Template view
    path("teachers_service_page/", views.teachers_service_page, name="teachers_service_page"),

    # API routes (everything inside teachers/api/urls.py)
    path("teachers_api/", include("teachers.api.urls")),
]
