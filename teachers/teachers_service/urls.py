from django.urls import path
from . import views


#url patterns for access_control/gatewa
urlpatterns = [
    path('teachers_service/', views.teachers_service, name='teachers_service'),
]