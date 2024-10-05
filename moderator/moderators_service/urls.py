from django.urls import path
from . import views


#url patterns for access_control/gatewa
urlpatterns = [
    path('moderators_service_page/', views.moderators_service_page, name='moderators_service_page'),
    path('admissions_and_registrations/', views.admissions_and_registrations, name='admissions_and_registrations')
]