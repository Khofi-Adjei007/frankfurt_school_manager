"""
URL configuration for frankfurt_school_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('moderator/moderators_service/', include("moderator.moderators_service.urls")),
    path('teachers/teachers_service/', include("teachers.teachers_service.urls")),
    path('parents/parents_service/', include("parents.parents_service.urls")),
    path('sia/sch_explorer/', include("sia.sch_explorer.urls")),
    path('access_control/gateway/', include("access_control.gateway.urls")),
    path('fsm_core_users/users/', include("fsm_core_users.users.urls")),
    path("__reload__/", include("django_browser_reload.urls")),
    path('admin/', admin.site.urls),
]
