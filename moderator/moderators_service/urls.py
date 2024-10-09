from django.urls import path
from . import views


#url patterns for access_control/gatewa
app_name = 'moderators_service'

urlpatterns = [
    path('moderators_service_page/', views.moderators_service_page, name='moderators_service_page'),
    path('admissions_and_registrations/', views.admissions_and_registrations, name='admissions_and_registrations'),
    path('settings_page/', views.settings_page, name='settings_page')
]