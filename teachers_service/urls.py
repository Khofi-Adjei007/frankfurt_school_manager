from django.urls import path
from . import views
from .teachers_api.teachers_api_views import teachers_service_api



#url patterns for access_control/gatewa
urlpatterns = [
    
    #Template url
    path('teachers_service_page/', views.teachers_service_page, name='teachers_service_page'),

    #API url
    path('teachers_api/teachers_service_api/', teachers_service_api, name='teachers_service_api' )
]