from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
import datetime

User = get_user_model()

class Crop(models.Model):
    name = models.CharField(max_length=100)
    scientific_name = models.CharField(max_length=100, blank=True)
    category = models.CharField(max_length=50)
    season = models.CharField(max_length=20)
    min_temperature = models.FloatField()
    max_temperature = models.FloatField()
    min_rainfall = models.FloatField()
    max_rainfall = models.FloatField()
    soil_ph_min = models.FloatField()
    soil_ph_max = models.FloatField()
    growing_period_days = models.IntegerField()
    suitable_states = models.TextField()  # Comma-separated states
    yield_per_hectare = models.FloatField(help_text="Average yield in tons per hectare")
    market_price_per_kg = models.FloatField(help_text="Average market price per kg")

    def __str__(self):
        return self.name


class CropRecommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    farm_size = models.FloatField()
    location = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    soil_ph = models.FloatField()
    temperature = models.FloatField()
    rainfall = models.FloatField()
    nitrogen = models.FloatField(null=True, blank=True)
    phosphorus = models.FloatField(null=True, blank=True)
    potassium = models.FloatField(null=True, blank=True)
    humidity = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Recommendation for {self.user.username} - {self.created_at}"


class RecommendedCrop(models.Model):
    recommendation = models.ForeignKey(CropRecommendation, on_delete=models.CASCADE, related_name='recommended_crops')
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    suitability_score = models.FloatField()
    expected_yield = models.FloatField()
    expected_profit = models.FloatField()
    
    class Meta:
        ordering = ['-suitability_score']
    
    def __str__(self):
        return f"{self.crop.name} for {self.recommendation.user.username}"


class CropPriceForecast(models.Model):
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, related_name='price_forecasts')
    month = models.IntegerField(help_text="Month number (1-12)")
    year = models.IntegerField()
    forecasted_price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Forecasted price per kg")
    price_change_percentage = models.DecimalField(max_digits=5, decimal_places=2, help_text="Percentage change from current price", null=True, blank=True)
    climate_impact = models.CharField(max_length=255, help_text="Climate impact on price (positive/negative/neutral)")
    market_trend = models.CharField(max_length=255, help_text="Market trend (rising/falling/stable)")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['year', 'month']
        unique_together = ('crop', 'month', 'year')
    
    def __str__(self):
        return f"{self.crop.name} - {self.month}/{self.year} - ₹{self.forecasted_price}"
