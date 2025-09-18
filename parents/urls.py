from django.urls import path
from . import views


#url patterns for access_control/gatewa
urlpatterns = [
    path('parents_service_page/', views.parents_service_page, name='parents_service_page'),
]