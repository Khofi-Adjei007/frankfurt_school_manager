from django import forms
from django.core.exceptions import ValidationError
from access_control.gateway.models import School
from .models import Admin
import re

def validate_phone_number(value):
    """Custom validator for phone numbers."""
    if not re.match(r'^\+?\d{10,13}$', value):
        raise ValidationError('Phone number must be in the format: "+1234567890" or "1234567890" with 10 to 13 digits.')

def validate_curriculum_types(value):
    """Custom validator for curriculum types."""
    if not re.match(r'^[a-zA-Z, ]+$', value):
        raise ValidationError('Curriculum types must contain only letters, commas, and spaces.')


class AdminAndSchoolSetupForm(forms.Form):
    # Admin fields
    first_name = forms.CharField(
        max_length=255,
        required=True,
        error_messages={'required': 'First name is required.'},
        widget=forms.TextInput(attrs={
            'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-red-500 focus:border-red-500 sm:text-sm',
            'placeholder': 'First Name'
        })
    )
    middle_name = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-red-500 focus:border-red-500 sm:text-sm',
            'placeholder': 'Middle Name'
        })
    )
    last_name = forms.CharField(
        max_length=255,
        required=True,
        error_messages={'required': 'Last name is required.'},
        widget=forms.TextInput(attrs={
            'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-red-500 focus:border-red-500 sm:text-sm',
            'placeholder': 'Last Name'
        })
    )
    email = forms.EmailField(
        required=True,
        error_messages={'required': 'Email is required.'},
        widget=forms.EmailInput(attrs={
            'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-red-500 focus:border-red-500 sm:text-sm',
            'placeholder': 'Email'
        })
    )
    phone_number = forms.CharField(
        max_length=13,
        required=True,
        validators=[validate_phone_number],
        widget=forms.TextInput(attrs={
            'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-red-500 focus:border-red-500 sm:text-sm',
            'placeholder': 'Phone Number'
        })
    )
    photo = forms.ImageField(required=False)

    # School fields
    logo = forms.ImageField(required=False)
    motto = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-red-500 focus:border-red-500 sm:text-sm',
            'placeholder': 'Motto'
        })
    )
    govt_registration_number = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-red-500 focus:border-red-500 sm:text-sm',
            'placeholder': 'Government Registration Number'
        })
    )
    social_media_links = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={
            'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-red-500 focus:border-red-500 sm:text-sm',
            'placeholder': 'Social Media Links'
        })
    )
    number_of_teachers = forms.IntegerField(
        required=True,
        error_messages={'required': 'Number of teachers is required.'},
        widget=forms.NumberInput(attrs={
            'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-red-500 focus:border-red-500 sm:text-sm',
            'placeholder': 'Number of Teachers'
        })
    )
    number_of_other_staff = forms.IntegerField(
        required=True,
        error_messages={'required': 'Number of other staff is required.'},
        widget=forms.NumberInput(attrs={
            'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-red-500 focus:border-red-500 sm:text-sm',
            'placeholder': 'Number of Other Staff'
        })
    )
    number_of_classrooms = forms.IntegerField(
        required=True,
        error_messages={'required': 'Number of classrooms is required.'},
        widget=forms.NumberInput(attrs={
            'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-red-500 focus:border-red-500 sm:text-sm',
            'placeholder': 'Number of Classrooms'
        })
    )
    curriculum_types = forms.CharField(
        max_length=255,
        required=True,
        validators=[validate_curriculum_types],
        error_messages={'required': 'Curriculum types are required.'},
        widget=forms.TextInput(attrs={
            'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-red-500 focus:border-red-500 sm:text-sm',
            'placeholder': 'Curriculum Types'
        })
    )
    board_of_directors = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-red-500 focus:border-red-500 sm:text-sm',
            'placeholder': 'Board of Directors'
        }),
        required=False
    )

    def __init__(self, admin_instance=None, school_instance=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if admin_instance:
            self.fields['first_name'].initial = admin_instance.first_name
            self.fields['middle_name'].initial = admin_instance.middle_name
            self.fields['last_name'].initial = admin_instance.last_name
            self.fields['email'].initial = admin_instance.email
            self.fields['phone_number'].initial = admin_instance.phone_number
            self.fields['photo'].initial = admin_instance.photo

        if school_instance:
            self.fields['logo'].initial = school_instance.logo
            self.fields['motto'].initial = school_instance.motto
            self.fields['govt_registration_number'].initial = school_instance.govt_registration_number
            self.fields['social_media_links'].initial = school_instance.social_media_links
            self.fields['number_of_teachers'].initial = school_instance.number_of_teachers
            self.fields['number_of_other_staff'].initial = school_instance.number_of_other_staff
            self.fields['number_of_classrooms'].initial = school_instance.number_of_classrooms
            self.fields['curriculum_types'].initial = school_instance.curriculum_types
            self.fields['board_of_directors'].initial = school_instance.board_of_directors

    def save(self, admin_instance, school_instance):
        # Save Admin data
        admin_instance.first_name = self.cleaned_data['first_name']
        admin_instance.middle_name = self.cleaned_data['middle_name']
        admin_instance.last_name = self.cleaned_data['last_name']
        admin_instance.email = self.cleaned_data['email']
        admin_instance.phone_number = self.cleaned_data['phone_number']
        admin_instance.photo = self.cleaned_data['photo']
        admin_instance.save()

        # Save School data
        school_instance.logo = self.cleaned_data['logo']
        school_instance.motto = self.cleaned_data['motto']
        school_instance.govt_registration_number = self.cleaned_data['govt_registration_number']
        school_instance.social_media_links = self.cleaned_data['social_media_links']
        school_instance.number_of_teachers = self.cleaned_data['number_of_teachers']
        school_instance.number_of_other_staff = self.cleaned_data['number_of_other_staff']
        school_instance.number_of_classrooms = self.cleaned_data['number_of_classrooms']
        school_instance.curriculum_types = self.cleaned_data['curriculum_types']
        school_instance.board_of_directors = self.cleaned_data['board_of_directors']
        school_instance.save()

