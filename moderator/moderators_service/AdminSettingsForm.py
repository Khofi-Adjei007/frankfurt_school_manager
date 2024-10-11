# moderators_service/AdminSettingsForm.py

from django import forms

class AdminSettingsForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        label='Name',
        widget=forms.TextInput(attrs={'class': 'border border-gray-300 rounded-clea p-2 w-full'}),
        error_messages={'required': 'Name is required.'}
    )
    
    position = forms.CharField(
        max_length=100,
        label='Position in School',
        widget=forms.TextInput(attrs={'class': 'border border-gray-300 rounded-md p-2 w-full'}),
        error_messages={'required': 'Position is required.'}
    )
    
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'border border-gray-300 rounded-md p-2 w-full'}),
        error_messages={
            'required': 'Email is required.',
            'invalid': 'Enter a valid email address.'
        }
    )
    
    phone = forms.CharField(
        max_length=15,
        label='Phone',
        widget=forms.TextInput(attrs={'class': 'border border-gray-300 rounded-md p-2 w-full'}),
        error_messages={'required': 'Phone number is required.'}
    )
    
    address = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'border border-gray-300 rounded-md p-2 w-full', 'rows': 3}),
        label='Address',
        error_messages={'required': 'Address is required.'}
    )
    
    profile_picture = forms.ImageField(
        label='Profile Picture',
        required=False
    )

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if len(phone) < 10:
            raise forms.ValidationError("Phone number must be at least 10 digits.")
        return phone

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name.replace(" ", "").isalpha():
            raise forms.ValidationError("Name must contain only letters.")
        return name
