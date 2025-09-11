from django import forms
from students.models import Student

class StudentMedicalInfoForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ["blood_group", "allergies_or_conditions"]
