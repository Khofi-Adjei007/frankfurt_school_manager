from django import forms
from students.models import Student

class StudentFamilyInfoForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            "has_sibling_here", "sibling_name", "sibling_class"
        ]
