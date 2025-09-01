from django.core.wsgi import get_wsgi_application
import os
import sys
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agrigenie.settings')
application = get_wsgi_application()
django.setup()

# Import models after Django setup
from apps.crops.models import Crop

# Define 10 new crops to add
new_crops = [
    {
        'name': 'Broccoli',
        'scientific_name': 'Brassica oleracea var. italica',
        'category': 'Vegetable',
        'season': 'Rabi',
        'min_temperature': 15.0,
        'max_temperature': 25.0,
        'min_rainfall': 40.0,
        'max_rainfall': 80.0,
        'soil_ph_min': 6.0,
        'soil_ph_max': 7.0,
        'growing_period_days': 70,
        'suitable_states': 'Himachal Pradesh, Uttarakhand, Punjab, Haryana, Uttar Pradesh, Maharashtra',
        'yield_per_hectare': 15.0,
        'market_price_per_kg': 40.0
    },
    {
        'name': 'Cauliflower',
        'scientific_name': 'Brassica oleracea var. botrytis',
        'category': 'Vegetable',
        'season': 'Rabi',
        'min_temperature': 14.0,
        'max_temperature': 24.0,
        'min_rainfall': 35.0,
        'max_rainfall': 75.0,
        'soil_ph_min': 5.5,
        'soil_ph_max': 7.5,
        'growing_period_days': 90,
        'suitable_states': 'Punjab, Haryana, Uttar Pradesh, Bihar, West Bengal, Assam',
        'yield_per_hectare': 18.0,
        'market_price_per_kg': 30.0
    },
    {
        'name': 'Carrot',
        'scientific_name': 'Daucus carota subsp. sativus',
        'category': 'Vegetable',
        'season': 'Rabi',
        'min_temperature': 10.0,
        'max_temperature': 25.0,
        'min_rainfall': 30.0,
        'max_rainfall': 70.0,
        'soil_ph_min': 6.0,
        'soil_ph_max': 7.0,
        'growing_period_days': 80,
        'suitable_states': 'Punjab, Haryana, Uttar Pradesh, Karnataka, Tamil Nadu, Andhra Pradesh',
        'yield_per_hectare': 25.0,
        'market_price_per_kg': 25.0
    },
    {
        'name': 'Spinach',
        'scientific_name': 'Spinacia oleracea',
        'category': 'Vegetable',
        'season': 'Rabi',
        'min_temperature': 10.0,
        'max_temperature': 24.0,
        'min_rainfall': 30.0,
        'max_rainfall': 60.0,
        'soil_ph_min': 6.0,
        'soil_ph_max': 7.5,
        'growing_period_days': 45,
        'suitable_states': 'Punjab, Haryana, Uttar Pradesh, Bihar, West Bengal, Maharashtra',
        'yield_per_hectare': 12.0,
        'market_price_per_kg': 30.0
    },
    {
        'name': 'Sunflower',
        'scientific_name': 'Helianthus annuus',
        'category': 'Oilseed',
        'season': 'Rabi',
        'min_temperature': 18.0,
        'max_temperature': 32.0,
        'min_rainfall': 50.0,
        'max_rainfall': 100.0,
        'soil_ph_min': 6.0,
        'soil_ph_max': 7.5,
        'growing_period_days': 110,
        'suitable_states': 'Karnataka, Andhra Pradesh, Maharashtra, Tamil Nadu, Punjab',
        'yield_per_hectare': 1.8,
        'market_price_per_kg': 45.0
    },
    {
        'name': 'Mango',
        'scientific_name': 'Mangifera indica',
        'category': 'Fruit',
        'season': 'Perennial',
        'min_temperature': 24.0,
        'max_temperature': 35.0,
        'min_rainfall': 75.0,
        'max_rainfall': 250.0,
        'soil_ph_min': 5.5,
        'soil_ph_max': 7.5,
        'growing_period_days': 365,  # Perennial
        'suitable_states': 'Uttar Pradesh, Andhra Pradesh, Karnataka, Bihar, Gujarat, Maharashtra, Tamil Nadu',
        'yield_per_hectare': 10.0,
        'market_price_per_kg': 60.0
    },
    {
        'name': 'Banana',
        'scientific_name': 'Musa acuminata',
        'category': 'Fruit',
        'season': 'Perennial',
        'min_temperature': 20.0,
        'max_temperature': 35.0,
        'min_rainfall': 120.0,
        'max_rainfall': 220.0,
        'soil_ph_min': 5.5,
        'soil_ph_max': 7.0,
        'growing_period_days': 300,
        'suitable_states': 'Tamil Nadu, Maharashtra, Gujarat, Andhra Pradesh, Karnataka, Kerala',
        'yield_per_hectare': 35.0,
        'market_price_per_kg': 25.0
    },
    {
        'name': 'Sugarcane',
        'scientific_name': 'Saccharum officinarum',
        'category': 'Cash Crop',
        'season': 'Kharif',
        'min_temperature': 20.0,
        'max_temperature': 35.0,
        'min_rainfall': 75.0,
        'max_rainfall': 150.0,
        'soil_ph_min': 6.0,
        'soil_ph_max': 8.0,
        'growing_period_days': 365,
        'suitable_states': 'Uttar Pradesh, Maharashtra, Karnataka, Tamil Nadu, Bihar, Punjab, Haryana',
        'yield_per_hectare': 80.0,
        'market_price_per_kg': 3.0
    },
    {
        'name': 'Turmeric',
        'scientific_name': 'Curcuma longa',
        'category': 'Spice',
        'season': 'Kharif',
        'min_temperature': 20.0,
        'max_temperature': 30.0,
        'min_rainfall': 150.0,
        'max_rainfall': 200.0,
        'soil_ph_min': 5.0,
        'soil_ph_max': 7.5,
        'growing_period_days': 270,
        'suitable_states': 'Andhra Pradesh, Tamil Nadu, Odisha, West Bengal, Maharashtra, Kerala',
        'yield_per_hectare': 6.0,
        'market_price_per_kg': 70.0
    },
    {
        'name': 'Ginger',
        'scientific_name': 'Zingiber officinale',
        'category': 'Spice',
        'season': 'Kharif',
        'min_temperature': 22.0,
        'max_temperature': 30.0,
        'min_rainfall': 150.0,
        'max_rainfall': 300.0,
        'soil_ph_min': 5.5,
        'soil_ph_max': 7.0,
        'growing_period_days': 240,
        'suitable_states': 'Kerala, Meghalaya, Arunachal Pradesh, Sikkim, Himachal Pradesh, Karnataka',
        'yield_per_hectare': 8.0,
        'market_price_per_kg': 80.0
    },
]

# Add crops to database
for crop_data in new_crops:
    # Check if crop already exists
    if not Crop.objects.filter(name=crop_data['name']).exists():
        crop = Crop(**crop_data)
        crop.save()
        print(f"Added {crop_data['name']}")
    else:
        print(f"{crop_data['name']} already exists, skipping")

print(f"\nTotal crops in database: {Crop.objects.count()}")