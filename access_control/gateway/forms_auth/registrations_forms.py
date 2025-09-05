from django import forms
from django.utils.translation import gettext_lazy as _
from ..models import School, FacilitiesChoice
import re


class InitialSchoolRegistrationForm(forms.ModelForm):
    """Form for initial school registration, limited to essential fields."""
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
        fields = ['school_name', 'school_type', 'physical_address', 'digital_address', 'official_telephone_number', 'email']

        widgets = {
            'school_name': forms.TextInput(attrs={
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
                'placeholder': 'Official Telephone Number',
                'required': 'required'  # Explicitly mark as required in HTML
            }),
            'email': forms.EmailInput(attrs={
                'id': 'email',
                'class': 'mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-red-500 focus:border-red-500 sm:text-sm',
                'placeholder': 'Email'
            }),
        }

    def clean_school_name(self):
        """Validate school name."""
        school_name = self.cleaned_data.get('school_name').lower()
        if not school_name or not re.match(r'^[a-zA-Z\s]*$', school_name):
            raise forms.ValidationError(_("Enter a valid school name (letters and spaces only)."))
        if School.objects.filter(school_name__iexact=school_name).exists():
            raise forms.ValidationError(_("A school with this name already exists."))
        return school_name

    def clean_email(self):
        """Validate email."""
        email = self.cleaned_data.get('email').lower()
        if not email:
            raise forms.ValidationError(_("Email address cannot be empty."))
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            raise forms.ValidationError(_("Enter a valid email address."))
        if School.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(_("A school with this email already exists."))
        return email

    def clean_physical_address(self):
        """Validate physical address."""
        physical_address = self.cleaned_data.get('physical_address').lower()
        if not physical_address:
            raise forms.ValidationError(_("Physical address cannot be empty."))
        if School.objects.filter(physical_address__iexact=physical_address).exists():
            raise forms.ValidationError(_("A school with this physical address already exists."))
        return physical_address

    def clean_digital_address(self):
        """Validate digital address."""
        digital_address = self.cleaned_data.get('digital_address').lower()
        if not digital_address:
            raise forms.ValidationError(_("Digital address cannot be empty."))
        if School.objects.filter(digital_address__iexact=digital_address).exists():
            raise forms.ValidationError(_("A school with this digital address already exists."))
        return digital_address

    def clean_official_telephone_number(self):
        """Validate official telephone number."""
        official_telephone_number = self.cleaned_data.get('official_telephone_number')
        if not official_telephone_number:
            raise forms.ValidationError(_("Official telephone number cannot be empty."))
        if not re.match(r'^\+?1?\d{9,15}$', official_telephone_number):
            raise forms.ValidationError(_("Enter a valid official telephone number (e.g., +1234567890 or 1234567890, 9-15 digits)."))
        if School.objects.filter(official_telephone_number=official_telephone_number).exists():
            raise forms.ValidationError(_("A school with this telephone number already exists."))
        return official_telephone_number

    def clean(self):
        """Validate password matching and overall form data."""
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', _("The two password fields must match."))
        return cleaned_data

# ... rest of the file (SchoolRegistrationForm, PrincipalDetailsForm, SchoolInfoForm) remains unchanged ...

class SchoolRegistrationForm(forms.ModelForm):
    """Full form for complete school registration, used in setup wizard."""
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
            'school_name', 'school_type', 'physical_address', 'digital_address',
            'official_telephone_number', 'email', 'registration_number', 'levels',
            'population', 'facilities', 'year_established', 'number_of_teachers',
            'number_of_classrooms', 'logo', 'board_of_directors', 'motto',
            'extra_curricular_activities'
        ]

        widgets = {
            'school_name': forms.TextInput(attrs={
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
            # Add widgets for other fields as needed for the setup wizard
        }

    def clean_school_name(self):
        school_name = self.cleaned_data.get('school_name').lower()
        if not school_name or not re.match(r'^[a-zA-Z\s]*$', school_name):
            raise forms.ValidationError(_("Enter a valid school name (letters and spaces only)."))
        return school_name

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

        school_name = cleaned_data.get('school_name')
        email = cleaned_data.get('email')
        official_telephone_number = cleaned_data.get('official_telephone_number')
        digital_address = cleaned_data.get('digital_address')
        physical_address = cleaned_data.get('physical_address')

        if school_name and School.objects.filter(school_name__iexact=school_name).exists():
            self.add_error('school_name', _("A school with this name already exists."))

        if email and School.objects.filter(email__iexact=email).exists():
            self.add_error('email', _("A school with this email already exists."))

        if official_telephone_number and School.objects.filter(official_telephone_number=official_telephone_number).exists():
            self.add_error('official_telephone_number', _("A school with this telephone number already exists."))

        if digital_address and School.objects.filter(digital_address__iexact=digital_address).exists():
            self.add_error('digital_address', _("A school with this digital address already exists."))

        if physical_address and School.objects.filter(physical_address__iexact=physical_address).exists():
            self.add_error('physical_address', _("A school with this physical address already exists."))

        return cleaned_data


from django.contrib.auth import get_user_model

User = get_user_model()

class PrincipalDetailsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['other_names', 'last_name', 'email', 'phone_number', 'photo']

    other_names = forms.CharField(max_length=255, required=False, label="Other Names")
    last_name = forms.CharField(max_length=255, required=True, label="Last Name")
    email = forms.EmailField(required=True, label="Email")
    phone_number = forms.CharField(max_length=15, required=True, label="Phone Number")
    photo = forms.ImageField(required=False, label="Profile Photo")

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(email__iexact=email).exclude(username__iexact=email).exists():
            raise forms.ValidationError("This email is already in use by another account.")
        return email
    


class SchoolInfoForm(forms.ModelForm):
    class Meta:
        model = School
        fields = ['registration_number', 'population', 'year_established', 'number_of_teachers', 'number_of_classrooms', 'levels', 'facilities']
        widgets = {
            'facilities': forms.CheckboxSelectMultiple,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['facilities'].queryset = FacilitiesChoice.objects.all()
        for field in self.fields:
            self.fields[field].required = False  # Make all fields optional for now, adjust as needed