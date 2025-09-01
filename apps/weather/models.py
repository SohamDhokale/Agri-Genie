from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class WeatherData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=100)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    temperature = models.FloatField()
    feels_like = models.FloatField(null=True, blank=True)
    humidity = models.FloatField()
    pressure = models.FloatField()
    wind_speed = models.FloatField()
    visibility = models.IntegerField(null=True, blank=True)
    weather_main = models.CharField(max_length=50, null=True, blank=True)
    description = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.location} - {self.timestamp}"

class WeatherForecast(models.Model):
    location = models.CharField(max_length=100)
    date = models.DateField()
    min_temp = models.FloatField()
    max_temp = models.FloatField()
    humidity = models.FloatField()
    description = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.location} - {self.date}"
