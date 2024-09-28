from django.urls import path
from . import views


#url patterns for access_control/gatewa
urlpatterns = [
    path('explore_school/', views.explore_school, name='explore_school'),
]