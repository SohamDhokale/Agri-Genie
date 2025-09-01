from django import forms

class CropRecommendationForm(forms.Form):
    # Indian States and Union Territories
    STATE_CHOICES = [
        ('', 'Select a State'),
        ('Andhra Pradesh', 'Andhra Pradesh'),
        ('Arunachal Pradesh', 'Arunachal Pradesh'),
        ('Assam', 'Assam'),
        ('Bihar', 'Bihar'),
        ('Chhattisgarh', 'Chhattisgarh'),
        ('Goa', 'Goa'),
        ('Gujarat', 'Gujarat'),
        ('Haryana', 'Haryana'),
        ('Himachal Pradesh', 'Himachal Pradesh'),
        ('Jharkhand', 'Jharkhand'),
        ('Karnataka', 'Karnataka'),
        ('Kerala', 'Kerala'),
        ('Madhya Pradesh', 'Madhya Pradesh'),
        ('Maharashtra', 'Maharashtra'),
        ('Manipur', 'Manipur'),
        ('Meghalaya', 'Meghalaya'),
        ('Mizoram', 'Mizoram'),
        ('Nagaland', 'Nagaland'),
        ('Odisha', 'Odisha'),
        ('Punjab', 'Punjab'),
        ('Rajasthan', 'Rajasthan'),
        ('Sikkim', 'Sikkim'),
        ('Tamil Nadu', 'Tamil Nadu'),
        ('Telangana', 'Telangana'),
        ('Tripura', 'Tripura'),
        ('Uttar Pradesh', 'Uttar Pradesh'),
        ('Uttarakhand', 'Uttarakhand'),
        ('West Bengal', 'West Bengal'),
        # Union Territories
        ('Andaman and Nicobar Islands', 'Andaman and Nicobar Islands'),
        ('Chandigarh', 'Chandigarh'),
        ('Dadra and Nagar Haveli and Daman and Diu', 'Dadra and Nagar Haveli and Daman and Diu'),
        ('Delhi', 'Delhi'),
        ('Jammu and Kashmir', 'Jammu and Kashmir'),
        ('Ladakh', 'Ladakh'),
        ('Lakshadweep', 'Lakshadweep'),
        ('Puducherry', 'Puducherry'),
    ]

    nitrogen = forms.FloatField(
        label='Nitrogen Content (N)', 
        min_value=0, 
        max_value=140,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter nitrogen content (0-140 kg/ha)',
            'step': '0.1'
        })
    )
    phosphorus = forms.FloatField(
        label='Phosphorus Content (P)', 
        min_value=0, 
        max_value=140,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter phosphorus content (0-140 kg/ha)',
            'step': '0.1'
        })
    )
    potassium = forms.FloatField(
        label='Potassium Content (K)', 
        min_value=0, 
        max_value=200,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter potassium content (0-200 kg/ha)',
            'step': '0.1'
        })
    )
    temperature = forms.FloatField(
        label='Temperature (°C)', 
        min_value=-20, 
        max_value=60,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter temperature (-20 to 60°C)',
            'step': '0.1'
        })
    )
    humidity = forms.FloatField(
        label='Humidity (%)', 
        min_value=0, 
        max_value=100,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter humidity (0-100%)',
            'step': '0.1'
        })
    )
    ph = forms.FloatField(
        label='pH', 
        min_value=0, 
        max_value=14,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter soil pH (0-14)',
            'step': '0.1'
        })
    )
    rainfall = forms.FloatField(
        label='Rainfall (mm)', 
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter rainfall in mm',
            'step': '0.1'
        })
    )
    state = forms.ChoiceField(
        label='State',
        choices=STATE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'state-select'
        })
    )
