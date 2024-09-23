from django.urls import path
from . import views


#url patterns for access_control/gatewa
urlpatterns = [
    path('logins/', views.logins, name='logins'),
    path('school_registration/', views.school_registration, name='school_registration'),
    path('service_homepage/', views.service_homepage, name='service_homepage'),
    path('admissions_and_registrations/', views.admissions_and_registrations, name='admissions_and_registrations')
]