from django.urls import path
from . import views


#url patterns for access_control/gatewa
urlpatterns = [
    path('', views.logins, name='logins'),
]