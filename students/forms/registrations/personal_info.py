from django import forms
from students.models import Student

class StudentPersonalInfoForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            "first_name", "middle_name", "last_name", 
            "gender", "date_of_birth", "complexion", 
            "religion", "preferred_language", "photo", "address"
        ]
