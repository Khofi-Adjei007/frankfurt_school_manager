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
        name = self.cleaned_data.get('name').lower()  # Convert to lowercase
        if not name or not re.match(r'^[a-zA-Z\s]*$', name):
            raise forms.ValidationError(_("Enter a valid school name (letters and spaces only)."))
        return name

    def clean_email(self):
        email = self.cleaned_data.get('email').lower()  # Convert to lowercase
        if not email:
            raise forms.ValidationError(_("Email address cannot be empty."))
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            raise forms.ValidationError(_("Enter a valid email address."))
        return email

    def clean_physical_address(self):
        physical_address = self.cleaned_data.get('physical_address').lower()  # Convert to lowercase
        if not physical_address:
            raise forms.ValidationError(_("Physical address cannot be empty."))
        return physical_address

    def clean_digital_address(self):
        digital_address = self.cleaned_data.get('digital_address').lower()  # Convert to lowercase
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

    def clean_population(self):
        population = self.cleaned_data.get('population')
        if population is None or population < 0:
            raise forms.ValidationError(_("Enter a valid student population (must be a positive number)."))
        return population

    def clean(self):
        """
        Custom clean method to check for duplicates across multiple fields 
        and ensure password and confirm password match.
        """
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password:
            if password != confirm_password:
                self.add_error('confirm_password', _("The two password fields must match."))

        # Check for duplicate entries
        name = cleaned_data.get('name')
        email = cleaned_data.get('email')
        official_telephone_number = cleaned_data.get('official_telephone_number')
        digital_address = cleaned_data.get('digital_address')
        physical_address = cleaned_data.get('physical_address')

        # Check for duplicate entries
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
