from django import forms
from .models import SchemeApplication

class SchemeApplicationForm(forms.ModelForm):
    class Meta:
        model = SchemeApplication
        fields = [
            'full_name', 'phone_number', 'email', 'address', 
            'farm_size', 'crop_type', 'annual_income', 'notes'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your full name'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your phone number'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email address'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter your complete address'
            }),
            'farm_size': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Farm size in hectares',
                'step': '0.01'
            }),
            'crop_type': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Type of crops you grow'
            }),
            'annual_income': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Annual income in INR',
                'step': '1000'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Any additional information or special circumstances'
            })
        }
        labels = {
            'full_name': 'Full Name',
            'phone_number': 'Phone Number',
            'email': 'Email Address',
            'address': 'Address',
            'farm_size': 'Farm Size (Hectares)',
            'crop_type': 'Crop Type',
            'annual_income': 'Annual Income (INR)',
            'notes': 'Additional Notes'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make some fields optional
        self.fields['farm_size'].required = False
        self.fields['crop_type'].required = False
        self.fields['annual_income'].required = False
        self.fields['notes'].required = False

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if phone:
            # Remove any non-digit characters
            phone = ''.join(filter(str.isdigit, phone))
            if len(phone) < 10:
                raise forms.ValidationError("Phone number must be at least 10 digits long.")
        return phone

    def clean_farm_size(self):
        farm_size = self.cleaned_data.get('farm_size')
        if farm_size and farm_size <= 0:
            raise forms.ValidationError("Farm size must be greater than 0.")
        return farm_size

    def clean_annual_income(self):
        income = self.cleaned_data.get('annual_income')
        if income and income < 0:
            raise forms.ValidationError("Annual income cannot be negative.")
        return income
