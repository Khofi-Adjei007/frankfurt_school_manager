from django import forms
from ..models import School
from django.utils.translation import gettext_lazy as _
import re

class SchoolRegistrationForm(forms.ModelForm):
    class Meta:
        model = School
        fields = [
            'name', 'school_type', 'year_established', 'physical_address', 
            'digital_address', 'official_telephone_number', 'email', 
            'social_media', 'population'
        ]

        widgets = {
            'name': forms.TextInput(attrs={
                'id': 'school_name',
                'class': 'mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-red-500 focus:border-red-500 sm:text-sm',
                'placeholder': 'School Name'
            }),
            'school_type': forms.Select(attrs={
                'id': 'school_type',
                'class': 'mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-red-500 focus:border-red-500 sm:text-sm'
            }),
            'year_established': forms.NumberInput(attrs={
                'id': 'year_established',
                'class': 'mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-red-500 focus:border-red-500 sm:text-sm'
            }),
            'physical_address': forms.TextInput(attrs={
                'id': 'physical_address',
                'class': 'mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-red-500 focus:border-red-500 sm:text-sm',
                'placeholder': 'Physical Address'
            }),
            'digital_address': forms.TextInput(attrs={
                'id': 'digital_address',
                'class': 'mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-red-500 focus:border-red-500 sm:text-sm',
                'placeholder': 'Digital Address'
            }),
            'official_telephone_number': forms.TextInput(attrs={
                'id': 'official_telephone_number',
                'class': 'mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-red-500 focus:border-red-500 sm:text-sm',
                'placeholder': 'Official Telephone Number'
            }),
            'email': forms.EmailInput(attrs={
                'id': 'email',
                'class': 'mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-red-500 focus:border-red-500 sm:text-sm',
                'placeholder': 'Email'
            }),
            'population': forms.NumberInput(attrs={
                'id': 'student_population',
                'class': 'mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-red-500 focus:border-red-500 sm:text-sm'
            }),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name or not re.match(r'^[a-zA-Z\s]*$', name):
            raise forms.ValidationError(_("Enter a valid school name (letters and spaces only)."))
        return name

    def clean_physical_address(self):
        physical_address = self.cleaned_data.get('physical_address')
        if not physical_address:
            raise forms.ValidationError(_("Physical address cannot be empty."))
        return physical_address

    def clean_digital_address(self):
        digital_address = self.cleaned_data.get('digital_address')
        if not digital_address:
            raise forms.ValidationError(_("Digital address cannot be empty."))
        return digital_address

    def clean_official_telephone_number(self):
        official_telephone_number = self.cleaned_data.get('official_telephone_number')
        if not official_telephone_number:
            raise forms.ValidationError(_("Official telephone number cannot be empty."))
        if not re.match(r'^\+?1?\d{9,15}$', official_telephone_number): 
            raise forms.ValidationError(_("Enter a valid official telephone number."))
        return official_telephone_number

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError(_("Email address cannot be empty."))
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            raise forms.ValidationError(_("Enter a valid email address."))
        return email

    def clean_population(self):
        population = self.cleaned_data.get('population')
        if population is None or population < 0:
            raise forms.ValidationError(_("Enter a valid student population (must be a positive number)."))
        return population

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        email = cleaned_data.get('email')

        # Check for duplicate school names
        if name and School.objects.filter(name=name).exists():
            self.add_error('name', _("This School Already Exist."))

        # Check for duplicate email addresses
        if email and School.objects.filter(email=email).exists():
            self.add_error('email', _("A school with this email address already exists."))

        return cleaned_data
