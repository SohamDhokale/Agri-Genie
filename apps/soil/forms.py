from django import forms
from .models import SoilTest

class SoilTestForm(forms.ModelForm):
    class Meta:
        model = SoilTest
        fields = ['ph_value', 'nitrogen', 'phosphorus', 'potassium', 'moisture', 'humidity', 'organic_matter']
        widgets = {
            'ph_value': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'min': '0',
                'max': '14',
                'placeholder': 'Enter pH value (0-14)'
            }),
            'nitrogen': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'min': '0',
                'placeholder': 'Nitrogen content (kg/ha)'
            }),
            'phosphorus': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'min': '0',
                'placeholder': 'Phosphorus content (kg/ha)'
            }),
            'potassium': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'min': '0',
                'placeholder': 'Potassium content (kg/ha)'
            }),
            'moisture': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'min': '0',
                'max': '100',
                'placeholder': 'Moisture content (%)'
            }),
            'humidity': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'min': '0',
                'max': '100',
                'placeholder': 'Humidity (%)'
            }),
            'organic_matter': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'min': '0',
                'placeholder': 'Organic matter content (%)'
            }),
        }
        help_texts = {
            'ph_value': 'Enter the pH value of the soil (0-14).',
            'nitrogen': 'Enter the nitrogen content in kg/ha.',
            'phosphorus': 'Enter the phosphorus content in kg/ha.',
            'potassium': 'Enter the potassium content in kg/ha.',
            'moisture': 'Enter the moisture content in percentage.',
            'humidity': 'Enter the humidity in percentage.',
            'organic_matter': 'Enter the organic matter content in percentage.'
        }