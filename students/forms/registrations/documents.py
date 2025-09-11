from django import forms
from students.models import Student

class StudentDocumentsForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            "birth_certificate", "transfer_certificate", 
            "previous_academic_report", "passport_photo", 
            "parent_id_proof"
        ]
    