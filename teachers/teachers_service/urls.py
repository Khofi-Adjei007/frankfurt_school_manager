from django.urls import path
from . import views


#url patterns for access_control/gatewa
urlpatterns = [
    path('teachers_service_page/', views.teachers_service_page, name='teachers_service_page'),
]