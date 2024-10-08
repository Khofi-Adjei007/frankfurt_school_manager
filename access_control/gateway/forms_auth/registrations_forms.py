from django import forms
from ..models import School
from django.utils.translation import gettext_lazy as _
import re



class SchoolRegistrationForm(forms.ModelForm):
    class Meta:
        model = School
        fields = [
            'name', 'school_type', 'year_established', 'physical_address', 'digital_address', 
            'official_contact', 'email', 'social_media', 'population'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'id': 'school_name', 'class': 'mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-red-500 focus:border-red-500 sm:text-sm', 'placeholder': 'School Name'}),
            'school_type': forms.Select(attrs={'id': 'school_type', 'class': 'mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-red-500 focus:border-red-500 sm:text-sm'}),
            'year_established': forms.NumberInput(attrs={'id': 'year_established', 'class': 'mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-red-500 focus:border-red-500 sm:text-sm'}),
            'physical_address': forms.TextInput(attrs={'id': 'physical_address', 'class': 'mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-red-500 focus:border-red-500 sm:text-sm', 'placeholder': 'Physical Address'}),
            'digital_address': forms.TextInput(attrs={'id': 'digital_address', 'class': 'mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-red-500 focus:border-red-500 sm:text-sm', 'placeholder': 'Digital Address'}),
            'official_contact': forms.TextInput(attrs={'id': 'official_contact', 'class': 'mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-red-500 focus:border-red-500 sm:text-sm', 'placeholder': 'Official Contact'}),
            'email': forms.EmailInput(attrs={'id': 'email', 'class': 'mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-red-500 focus:border-red-500 sm:text-sm', 'placeholder': 'Email'}),
            'social_media': forms.TextInput(attrs={'id': 'social_media', 'class': 'mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-red-500 focus:border-red-500 sm:text-sm', 'placeholder': 'Social Media'}),
            'population': forms.NumberInput(attrs={'id': 'student_population', 'class': 'mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-red-500 focus:border-red-500 sm:text-sm'})
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

    def clean_official_contact(self):
        official_contact = self.cleaned_data.get('official_contact')
        if not official_contact:
            raise forms.ValidationError(_("Official contact cannot be empty."))
        if not re.match(r'^\+?1?\d{9,15}$', official_contact):  # Adjust regex according to your needs
            raise forms.ValidationError(_("Enter a valid official contact number."))
        return official_contact

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError(_("Email address cannot be empty."))
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            raise forms.ValidationError(_("Enter a valid email address."))
        return email

    def clean_social_media(self):
        social_media = self.cleaned_data.get('social_media')
        if not social_media:
            raise forms.ValidationError(_("Social media cannot be empty."))
        return social_media

    def clean_population(self):
        population = self.cleaned_data.get('population')
        if population is None or population < 0:
            raise forms.ValidationError(_("Enter a valid student population (must be a positive number)."))
        return population

