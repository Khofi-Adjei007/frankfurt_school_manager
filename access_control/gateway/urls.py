from django.urls import path
from . import views

app_name = 'gateway'

urlpatterns = [
    path('logins/', views.logins, name='logins'),
    path('school-registration/', views.school_registration, name='school_registration'),
    path('setup-welcome/', views.setup_welcome, name='setup_welcome'),
    path('setup-wizard/', views.setup_wizard, name='setup_wizard'),
    path('logout/', views.logout_view, name='logout'),
]