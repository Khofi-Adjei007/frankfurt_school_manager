from django.urls import path
from . import views


#url patterns for access_control/gatewa
urlpatterns = [
    path('logins/', views.logins, name='logins'),
    path('school_registration/', views.school_registration, name='school_registration'),
    path('register/success/', views.school_registration_success, name='school_registration_success'),
]