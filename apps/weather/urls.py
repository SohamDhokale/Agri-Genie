from django.urls import path
from . import views

urlpatterns = [
    path('', views.weather_dashboard, name='weather_dashboard'),
    path('get-weather/', views.get_weather_data, name='get_weather'),
    path('get-current-location/', views.get_current_location_weather, name='get_current_location_weather'),
    path('get-forecast/', views.get_forecast_data, name='get_forecast'),
    path('get-history/', views.get_weather_history, name='get_weather_history'),
    path('get-annual-outlook/', views.get_annual_outlook, name='get_annual_outlook'),
]
