from django import forms
from django.utils.translation import gettext_lazy as _
from ..models import School
import re

class SchoolRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(attrs={
            'id': 'password',
            'class': 'mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-red-500 focus:border-red-500 sm:text-sm',
            'placeholder': 'Password'
        }),
        strip=False,
    )

    confirm_password = forms.CharField(
        label=_("Confirm Password"),
        widget=forms.PasswordInput(attrs={
            'id': 'confirm_password',
            'class': 'mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-red-500 focus:border-red-500 sm:text-sm',
            'placeholder': 'Confirm Password'
        }),
        strip=False,
    )

    class Meta:
        model = School
        fields = [
            'name', 'school_type', 'physical_address', 
            'digital_address', 'official_telephone_number', 'email', 
            'social_media'
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
        
        }

    # Existing clean methods unchanged
    def clean_name(self):
        name = self.cleaned_data.get('name').lower()
        if not name or not re.match(r'^[a-zA-Z\s]*$', name):
            raise forms.ValidationError(_("Enter a valid school name (letters and spaces only)."))
        return name

    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        if not email:
            raise forms.ValidationError(_("Email address cannot be empty."))
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            raise forms.ValidationError(_("Enter a valid email address."))
        return email

    def clean_physical_address(self):
        physical_address = self.cleaned_data.get('physical_address').lower()
        if not physical_address:
            raise forms.ValidationError(_("Physical address cannot be empty."))
        return physical_address

    def clean_digital_address(self):
        digital_address = self.cleaned_data.get('digital_address').lower()
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

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password:
            if password != confirm_password:
                self.add_error('confirm_password', _("The two password fields must match."))

        name = cleaned_data.get('name')
        email = cleaned_data.get('email')
        official_telephone_number = cleaned_data.get('official_telephone_number')
        digital_address = cleaned_data.get('digital_address')
        physical_address = cleaned_data.get('physical_address')

        if name and School.objects.filter(name__iexact=name).exists():
            self.add_error('name', _("A school with this name already exists."))

        if email and School.objects.filter(email__iexact=email).exists():
            self.add_error('email', _("A school with this email already exists."))

        if official_telephone_number and School.objects.filter(official_telephone_number=official_telephone_number).exists():
            self.add_error('official_telephone_number', _("A school with this telephone number already exists."))

        if digital_address and School.objects.filter(digital_address__iexact=digital_address).exists():
            self.add_error('digital_address', _("A school with this digital address already exists."))

        if physical_address and School.objects.filter(physical_address__iexact=physical_address).exists():
            self.add_error('physical_address', _("A school with this physical address already exists."))

        return cleaned_data