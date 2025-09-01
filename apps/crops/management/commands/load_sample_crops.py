from django.core.management.base import BaseCommand
from apps.crops.models import Crop

class Command(BaseCommand):
    help = 'Load sample crop data for testing'

    def handle(self, *args, **options):
        crops_data = [
            {
                'name': 'Rice',
                'scientific_name': 'Oryza sativa',
                'category': 'Cereal',
                'season': 'Kharif',
                'min_temperature': 20.0,
                'max_temperature': 35.0,
                'min_rainfall': 100.0,
                'max_rainfall': 200.0,
                'soil_ph_min': 5.5,
                'soil_ph_max': 7.5,
                'growing_period_days': 120,
                'suitable_states': 'Punjab, Haryana, Uttar Pradesh, Bihar, West Bengal, Tamil Nadu, Andhra Pradesh, Telangana, Karnataka, Kerala',
                'yield_per_hectare': 3.5,
                'market_price_per_kg': 25.0
            },
            {
                'name': 'Wheat',
                'scientific_name': 'Triticum aestivum',
                'category': 'Cereal',
                'season': 'Rabi',
                'min_temperature': 15.0,
                'max_temperature': 25.0,
                'min_rainfall': 50.0,
                'max_rainfall': 100.0,
                'soil_ph_min': 6.0,
                'soil_ph_max': 8.0,
                'growing_period_days': 140,
                'suitable_states': 'Punjab, Haryana, Uttar Pradesh, Madhya Pradesh, Rajasthan, Bihar, Gujarat, Maharashtra',
                'yield_per_hectare': 4.0,
                'market_price_per_kg': 22.0
            },
            {
                'name': 'Maize',
                'scientific_name': 'Zea mays',
                'category': 'Cereal',
                'season': 'Kharif',
                'min_temperature': 18.0,
                'max_temperature': 32.0,
                'min_rainfall': 80.0,
                'max_rainfall': 150.0,
                'soil_ph_min': 5.5,
                'soil_ph_max': 7.5,
                'growing_period_days': 100,
                'suitable_states': 'Karnataka, Andhra Pradesh, Telangana, Maharashtra, Madhya Pradesh, Bihar, Uttar Pradesh',
                'yield_per_hectare': 3.0,
                'market_price_per_kg': 18.0
            },
            {
                'name': 'Cotton',
                'scientific_name': 'Gossypium hirsutum',
                'category': 'Fiber',
                'season': 'Kharif',
                'min_temperature': 20.0,
                'max_temperature': 35.0,
                'min_rainfall': 60.0,
                'max_rainfall': 120.0,
                'soil_ph_min': 6.0,
                'soil_ph_max': 8.5,
                'growing_period_days': 180,
                'suitable_states': 'Gujarat, Maharashtra, Madhya Pradesh, Karnataka, Andhra Pradesh, Telangana, Punjab, Haryana',
                'yield_per_hectare': 2.5,
                'market_price_per_kg': 45.0
            },
            {
                'name': 'Sugarcane',
                'scientific_name': 'Saccharum officinarum',
                'category': 'Commercial',
                'season': 'Kharif',
                'min_temperature': 20.0,
                'max_temperature': 38.0,
                'min_rainfall': 100.0,
                'max_rainfall': 200.0,
                'soil_ph_min': 6.0,
                'soil_ph_max': 8.0,
                'growing_period_days': 365,
                'suitable_states': 'Uttar Pradesh, Maharashtra, Karnataka, Tamil Nadu, Andhra Pradesh, Telangana, Gujarat, Bihar',
                'yield_per_hectare': 70.0,
                'market_price_per_kg': 3.5
            },
            {
                'name': 'Potato',
                'scientific_name': 'Solanum tuberosum',
                'category': 'Vegetable',
                'season': 'Rabi',
                'min_temperature': 15.0,
                'max_temperature': 25.0,
                'min_rainfall': 40.0,
                'max_rainfall': 80.0,
                'soil_ph_min': 5.5,
                'soil_ph_max': 7.0,
                'growing_period_days': 90,
                'suitable_states': 'Uttar Pradesh, West Bengal, Bihar, Punjab, Gujarat, Madhya Pradesh, Karnataka',
                'yield_per_hectare': 25.0,
                'market_price_per_kg': 15.0
            },
            {
                'name': 'Tomato',
                'scientific_name': 'Solanum lycopersicum',
                'category': 'Vegetable',
                'season': 'Rabi',
                'min_temperature': 18.0,
                'max_temperature': 30.0,
                'min_rainfall': 30.0,
                'max_rainfall': 70.0,
                'soil_ph_min': 6.0,
                'soil_ph_max': 7.5,
                'growing_period_days': 90,
                'suitable_states': 'Andhra Pradesh, Telangana, Karnataka, Maharashtra, Tamil Nadu, Gujarat, Madhya Pradesh',
                'yield_per_hectare': 35.0,
                'market_price_per_kg': 20.0
            },
            {
                'name': 'Onion',
                'scientific_name': 'Allium cepa',
                'category': 'Vegetable',
                'season': 'Rabi',
                'min_temperature': 15.0,
                'max_temperature': 28.0,
                'min_rainfall': 30.0,
                'max_rainfall': 60.0,
                'soil_ph_min': 6.0,
                'soil_ph_max': 7.5,
                'growing_period_days': 120,
                'suitable_states': 'Maharashtra, Karnataka, Andhra Pradesh, Telangana, Gujarat, Madhya Pradesh, Rajasthan',
                'yield_per_hectare': 20.0,
                'market_price_per_kg': 25.0
            },
            {
                'name': 'Groundnut',
                'scientific_name': 'Arachis hypogaea',
                'category': 'Oilseed',
                'season': 'Kharif',
                'min_temperature': 20.0,
                'max_temperature': 35.0,
                'min_rainfall': 60.0,
                'max_rainfall': 120.0,
                'soil_ph_min': 6.0,
                'soil_ph_max': 7.5,
                'growing_period_days': 120,
                'suitable_states': 'Gujarat, Andhra Pradesh, Telangana, Tamil Nadu, Karnataka, Maharashtra, Madhya Pradesh',
                'yield_per_hectare': 2.5,
                'market_price_per_kg': 60.0
            },
            {
                'name': 'Soybean',
                'scientific_name': 'Glycine max',
                'category': 'Oilseed',
                'season': 'Kharif',
                'min_temperature': 18.0,
                'max_temperature': 32.0,
                'min_rainfall': 70.0,
                'max_rainfall': 140.0,
                'soil_ph_min': 6.0,
                'soil_ph_max': 7.5,
                'growing_period_days': 100,
                'suitable_states': 'Madhya Pradesh, Maharashtra, Rajasthan, Karnataka, Andhra Pradesh, Telangana',
                'yield_per_hectare': 2.0,
                'market_price_per_kg': 35.0
            }
        ]

        created_count = 0
        for crop_data in crops_data:
            crop, created = Crop.objects.get_or_create(
                name=crop_data['name'],
                defaults=crop_data
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created crop: {crop.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Crop already exists: {crop.name}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully loaded {created_count} new crops')
        )
