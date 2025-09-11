from django import forms
from students.models import Student

class StudentTalentsSportsForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ["talents", "sports"]
        widgets = {
            "talents": forms.CheckboxSelectMultiple,
            "sports": forms.CheckboxSelectMultiple,
        }
