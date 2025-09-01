from django.contrib import admin
from .models import Crop, CropRecommendation, RecommendedCrop, CropPriceForecast

@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'season', 'market_price_per_kg')
    list_filter = ('category', 'season')
    search_fields = ('name', 'scientific_name')

@admin.register(CropRecommendation)
class CropRecommendationAdmin(admin.ModelAdmin):
    list_display = ('user', 'state', 'created_at')
    list_filter = ('state',)

@admin.register(RecommendedCrop)
class RecommendedCropAdmin(admin.ModelAdmin):
    list_display = ('crop', 'recommendation', 'suitability_score')
    list_filter = ('crop',)

@admin.register(CropPriceForecast)
class CropPriceForecastAdmin(admin.ModelAdmin):
    list_display = ('crop', 'month', 'year', 'forecasted_price', 'market_trend')
    list_filter = ('crop', 'market_trend', 'year', 'month')
