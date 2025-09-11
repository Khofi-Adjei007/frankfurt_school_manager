from django import forms
from students.models import Student

class StudentEducationBackgroundForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            "last_school_attended", "last_class_completed"
        ]
