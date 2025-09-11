from django import forms
from students.models import Student

class StudentOfficeUseForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            "application_number", "admission_approved", 
            "rejection_reason", "class_allotted", "admitted_by", 
            "remarks"
        ]
