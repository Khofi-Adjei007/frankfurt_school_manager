"""
URL configuration for frankfurt_school_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # API routes
    path("api/students/", include("students.api.urls")),
    path("api/teachers/", include("teachers.api.urls")),
    path("api/moderators/", include("moderators.api.urls")), 
    path("api/parents/", include("parents.api.urls")),

    # Web routes (HTML templates, forms, dashboards)
    path("students/", include("students.urls")),
    path("teachers/", include("teachers.urls")),
    path("moderators/", include("moderators.urls")),
    path("parents/", include("parents.urls")),
    path("sia/sch_explorer/", include("sia.sch_explorer.urls")),
    path("fsm_core_users/users/", include("fsm_core_users.users.urls")),

    # Utilities
    path("__reload__/", include("django_browser_reload.urls")),
    path("gateway/", include("access_control.gateway.urls", namespace="gateway")),
    path("admin/", admin.site.urls),
]
