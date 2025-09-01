from .models import Crop, CropPriceForecast
from django.utils import timezone
import math
import random
import datetime

class CropRecommendationEngine:
    def __init__(self, recommendation):
        self.recommendation = recommendation
    
    def get_recommendations(self):
        suitable_crops = Crop.objects.filter(
            suitable_states__icontains=self.recommendation.state
        )
        
        recommendations = []
        for crop in suitable_crops:
            score = self.calculate_suitability_score(crop)
            if score > 60:  # Only recommend crops with good suitability
                expected_yield = self.calculate_expected_yield(crop)
                expected_profit = self.calculate_expected_profit(crop, expected_yield)
                
                # Generate price forecasts for this crop
                price_engine = PriceForecastEngine(
                    crop=crop,
                    location=self.recommendation.state,
                    temperature=self.recommendation.temperature,
                    rainfall=self.recommendation.rainfall
                )
                price_forecasts = price_engine.generate_price_forecasts()
                
                recommendations.append({
                    'crop': crop,
                    'score': score,
                    'expected_yield': expected_yield,
                    'expected_profit': expected_profit,
                    'price_forecasts': price_forecasts
                })
        
        # Sort by expected profit
        recommendations.sort(key=lambda x: x['expected_profit'], reverse=True)
        return recommendations[:5]  # Return top 5 recommendations
    
    def calculate_suitability_score(self, crop):
        score = 100
        
        # Temperature suitability
        temp_diff = min(
            abs(self.recommendation.temperature - crop.min_temperature),
            abs(self.recommendation.temperature - crop.max_temperature)
        )
        if crop.min_temperature <= self.recommendation.temperature <= crop.max_temperature:
            temp_score = 100
        else:
            temp_score = max(0, 100 - (temp_diff * 5))
        
        # pH suitability
        ph_diff = min(
            abs(self.recommendation.soil_ph - crop.soil_ph_min),
            abs(self.recommendation.soil_ph - crop.soil_ph_max)
        )
        if crop.soil_ph_min <= self.recommendation.soil_ph <= crop.soil_ph_max:
            ph_score = 100
        else:
            ph_score = max(0, 100 - (ph_diff * 10))
        
        # Rainfall suitability (if available)
        if hasattr(self.recommendation, 'rainfall'):
            if crop.min_rainfall <= self.recommendation.rainfall <= crop.max_rainfall:
                rainfall_score = 100
            else:
                rainfall_diff = min(
                    abs(self.recommendation.rainfall - crop.min_rainfall),
                    abs(self.recommendation.rainfall - crop.max_rainfall)
                )
                rainfall_score = max(0, 100 - (rainfall_diff * 0.1))
        else:
            rainfall_score = 80  # Default score if rainfall data not available
        
        # Calculate weighted average
        final_score = (temp_score * 0.4 + ph_score * 0.3 + rainfall_score * 0.3)
        return round(final_score, 2)
    
    def calculate_expected_yield(self, crop):
        base_yield = crop.yield_per_hectare
        # Adjust based on farm size (efficiency factors)
        if self.recommendation.farm_size < 1:
            efficiency_factor = 0.8
        elif self.recommendation.farm_size < 5:
            efficiency_factor = 0.9
        else:
            efficiency_factor = 1.0
        
        return round(base_yield * efficiency_factor * self.recommendation.farm_size, 2)
    
    def calculate_expected_profit(self, crop, expected_yield):
        revenue = expected_yield * 1000 * crop.market_price_per_kg  # Convert tons to kg
        # Estimate costs (30-40% of revenue typically)
        costs = revenue * 0.35
        profit = revenue - costs
        return round(profit, 2)


class PriceForecastEngine:
    """Engine to forecast crop prices for the next six months based on climate and market trends"""
    
    def __init__(self, crop, location=None, temperature=None, rainfall=None):
        self.crop = crop
        self.location = location
        self.temperature = temperature
        self.rainfall = rainfall
        self.current_price = crop.market_price_per_kg
        self.current_date = timezone.now().date()
    
    def generate_price_forecasts(self):
        """Generate price forecasts for the next six months"""
        # Delete any existing forecasts for this crop
        CropPriceForecast.objects.filter(crop=self.crop).delete()
        
        forecasts = []
        current_month = self.current_date.month
        current_year = self.current_date.year
        
        # Climate impact factors based on crop type and weather conditions
        climate_impacts = self._analyze_climate_impact()
        
        # Market trend analysis
        market_trends = self._analyze_market_trends()
        
        # Generate forecasts for next 6 months
        for i in range(6):
            # Calculate target month and year
            target_month = ((current_month + i) % 12) or 12  # Convert 0 to 12
            target_year = current_year + (current_month + i - 1) // 12
            
            # Get climate impact for this month
            month_climate = climate_impacts[i]
            
            # Get market trend for this month
            initial_market_trend = market_trends[i]
            
            # Calculate forecasted price and get updated market trend
            forecasted_price, price_change_pct, market_trend = self.calculate_forecasted_price(
                i, month_climate, initial_market_trend
            )
            
            # Create forecast object
            forecast = CropPriceForecast(
                crop=self.crop,
                month=target_month,
                year=target_year,
                forecasted_price=round(forecasted_price, 2),
                price_change_percentage=round(price_change_pct, 2),
                climate_impact=month_climate,
                market_trend=market_trend
            )
            forecast.save()
            forecasts.append(forecast)
        
        return forecasts
    
    def _analyze_climate_impact(self):
        """Analyze climate impact on crop prices for next 6 months"""
        # This would ideally use real climate forecast data
        # For now, we'll use a simplified model based on crop type and season
        
        impacts = []
        current_month = self.current_date.month
        
        # Seasonal patterns for different crop categories
        grain_pattern = ['neutral', 'positive', 'positive', 'neutral', 'negative', 'negative']
        vegetable_pattern = ['negative', 'neutral', 'positive', 'positive', 'neutral', 'negative']
        fruit_pattern = ['positive', 'positive', 'neutral', 'negative', 'negative', 'neutral']
        
        # Select pattern based on crop category
        if hasattr(self.crop, 'category'):
            if 'grain' in self.crop.category.lower():
                pattern = grain_pattern
            elif 'vegetable' in self.crop.category.lower():
                pattern = vegetable_pattern
            elif 'fruit' in self.crop.category.lower():
                pattern = fruit_pattern
            else:
                pattern = ['neutral', 'neutral', 'positive', 'positive', 'neutral', 'negative']
        else:
            pattern = ['neutral', 'neutral', 'positive', 'positive', 'neutral', 'negative']
        
        # Adjust pattern based on starting month
        start_idx = (current_month % 6)
        for i in range(6):
            impacts.append(pattern[(start_idx + i) % 6])
        
        return impacts
    
    def _analyze_market_trends(self):
        """Analyze market trends for crop prices for next 6 months"""
        # This would ideally use real market data and economic indicators
        # For now, we'll use a simplified model with some randomization
        
        trends = []
        trend_options = ['rising', 'stable', 'falling']
        weights = [0.4, 0.4, 0.2]  # Slightly biased toward rising/stable
        
        # Generate initial trend
        current_trend = random.choices(trend_options, weights=weights)[0]
        trends.append(current_trend)
        
        # Generate subsequent trends with some continuity
        for i in range(5):
            if current_trend == 'rising':
                weights = [0.5, 0.3, 0.2]  # More likely to continue rising or stabilize
            elif current_trend == 'stable':
                weights = [0.3, 0.4, 0.3]  # More likely to remain stable
            else:  # falling
                weights = [0.2, 0.3, 0.5]  # More likely to continue falling or stabilize
            
            current_trend = random.choices(trend_options, weights=weights)[0]
            trends.append(current_trend)
        
        return trends
    
    def _get_climate_factor(self, climate_impact):
        """Convert climate impact to price change factor"""
        if climate_impact == 'positive':
            return random.uniform(-8, -3)  # Good climate = lower prices
        elif climate_impact == 'negative':
            return random.uniform(3, 10)  # Bad climate = higher prices
        else:  # neutral
            return random.uniform(-2, 2)
    
    def _get_market_factor(self, market_trend):
        """Convert market trend to price change factor"""
        if market_trend == 'rising':
            return random.uniform(2, 8)
        elif market_trend == 'falling':
            return random.uniform(-8, -2)
        else:  # stable
            return random.uniform(-1, 1)
            
    def calculate_forecasted_price(self, month_offset, climate_impact, market_trend):
        """Calculate forecasted price based on climate impact and market trend"""
        current_price = float(self.crop.market_price_per_kg)
        
        # Base monthly fluctuation (random between -5% and +8%)
        base_fluctuation = random.uniform(-0.05, 0.08)
        
        # Climate impact adjustment
        climate_adjustment = 0
        if climate_impact == 'positive':
            climate_adjustment = random.uniform(0.02, 0.05)
        elif climate_impact == 'negative':
            climate_adjustment = random.uniform(-0.05, -0.02)
        
        # Market trend adjustment
        market_adjustment = 0
        if market_trend == 'rising':
            market_adjustment = random.uniform(0.03, 0.07) * month_offset / 6
        elif market_trend == 'falling':
            market_adjustment = random.uniform(-0.07, -0.03) * month_offset / 6
        
        # Calculate total percentage change
        total_change_percentage = base_fluctuation + climate_adjustment + market_adjustment
        
        # Calculate new price
        new_price = current_price * (1 + total_change_percentage)
        
        # Set market trend based on the actual price change percentage
        # This ensures consistency between price_change_percentage and market_trend
        if total_change_percentage > 0:
            market_trend = 'rising'
        elif total_change_percentage < 0:
            market_trend = 'falling'
        else:
            market_trend = 'stable'
        
        return new_price, total_change_percentage * 100, market_trend  # Return price, percentage change, and updated trend
