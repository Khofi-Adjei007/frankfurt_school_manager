from django.urls import path, re_path
from django.views.generic import RedirectView
from . import views

app_name = 'gateway'

urlpatterns = [
    path('logins/', views.logins, name='logins'),
    path('register/', views.register_school, name='register'),
    re_path(r'^school-registration/$', RedirectView.as_view(url='/gateway/register/', permanent=True)),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('setup/step1/', views.setup_step1, name='setup_step1'),
    path('setup/step2/', views.setup_step2, name='setup_step2'),
    path('setup/step3/', views.setup_step3, name='setup_step3'),
    path('logout/', views.logout_view, name='logout'),
]