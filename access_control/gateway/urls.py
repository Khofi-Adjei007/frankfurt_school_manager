from django.urls import path
from . import views


#url patterns for access_control/gatewa
app_name = 'gateway'

urlpatterns = [
    path('logins/', views.logins, name='logins'),
    path('school_registration/', views.school_registration, name='school_registration'),
    path('school_registration_success', views.school_registration_success, name='school_registration_success'),
    path('logout/', views.logout_view, name='logout'),
    path('animation/', views.animation_page, name='animation_page'),

]