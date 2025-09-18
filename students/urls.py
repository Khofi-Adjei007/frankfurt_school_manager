from django.urls import path
from .views import StudentRegistrationView

app_name = "students"

urlpatterns = [
    path("register/step/<int:step>/", StudentRegistrationView.as_view(), name="registration_step"),
    path("register/", StudentRegistrationView.as_view(), name="registration_start"),
    path("register/success/<int:pk>/", StudentRegistrationView.as_view(), name="registration_success"),
]
