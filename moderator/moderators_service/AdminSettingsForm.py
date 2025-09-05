from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class AdminSettingsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['other_names', 'last_name', 'email', 'phone_number', 'photo']  # Match User model fields

    other_names = forms.CharField(
        max_length=100,
        label='Name',  # Use as first/middle names
        widget=forms.TextInput(attrs={'class': 'border border-gray-300 rounded-md p-2 w-full'}),
        error_messages={'required': 'Name is required.'}
    )

    last_name = forms.CharField(
        max_length=100,
        label='Last Name',
        widget=forms.TextInput(attrs={'class': 'border border-gray-300 rounded-md p-2 w-full'}),
        error_messages={'required': 'Last Name is required.'}
    )

    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'border border-gray-300 rounded-md p-2 w-full'}),
        error_messages={
            'required': 'Email is required.',
            'invalid': 'Enter a valid email address.'
        }
    )

    phone_number = forms.CharField(
        max_length=15,
        label='Phone',
        widget=forms.TextInput(attrs={'class': 'border border-gray-300 rounded-md p-2 w-full'}),
        error_messages={'required': 'Phone number is required.'}
    )

    photo = forms.ImageField(
        label='Profile Picture',
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'border border-gray-300 rounded-md p-2 w-full'})
    )

    def clean_phone_number(self):  # Renamed to match field
        phone = self.cleaned_data.get('phone_number')
        if len(phone) < 10:
            raise forms.ValidationError("Phone number must be at least 10 digits.")
        return phone

    def clean_other_names(self):  # Renamed to match field
        name = self.cleaned_data.get('other_names')
        if not name.replace(" ", "").isalpha():
            raise forms.ValidationError("Name must contain only letters.")
        return name