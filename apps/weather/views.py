import requests
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import JsonResponse
from .models import WeatherData
import json
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
import time

class LocationWeatherTracker:
    def __init__(self):
        self.geolocator = Nominatim(user_agent="agrigenie_weather")
    
    def get_live_location(self):
        """Get live location using IP-based geolocation"""
        try:
            # Use a free IP geolocation service
            response = requests.get('https://ipapi.co/json/', timeout=15)
            if response.status_code == 200:
                data = response.json()
                latitude = data.get('latitude')
                longitude = data.get('longitude')
                
                if latitude and longitude:
                    return {
                        'latitude': latitude,
                        'longitude': longitude,
                        'city': data.get('city', 'Unknown'),
                        'country': data.get('country_name', 'Unknown')
                    }
                else:
                    print("IP geolocation returned invalid coordinates")
            else:
                print(f"IP geolocation API returned status code: {response.status_code}")
        except requests.exceptions.Timeout:
            print("IP geolocation request timed out")
        except requests.exceptions.RequestException as e:
            print(f"IP geolocation request error: {e}")
        except Exception as e:
            print(f"IP geolocation error: {e}")
        
        return None
    
    def get_weather_data(self, lat, lon):
        """Get weather data using OpenMeteo API"""
        try:
            # OpenMeteo API - no API key required
            url = f"https://api.open-meteo.com/v1/forecast"
            params = {
                'latitude': lat,
                'longitude': lon,
                'current': 'temperature_2m,relative_humidity_2m,apparent_temperature,pressure_msl,wind_speed_10m,weather_code,visibility',
                'timezone': 'auto',
                'forecast_days': 1
            }
            
            response = requests.get(url, params=params, timeout=15)
            if response.status_code == 200:
                data = response.json()
                current = data.get('current', {})
                
                if not current:
                    print("No current weather data in API response")
                    return None
                
                # Convert weather code to description
                weather_descriptions = {
                    0: 'Clear sky',
                    1: 'Mainly clear',
                    2: 'Partly cloudy',
                    3: 'Overcast',
                    45: 'Foggy',
                    48: 'Depositing rime fog',
                    51: 'Light drizzle',
                    53: 'Moderate drizzle',
                    55: 'Dense drizzle',
                    61: 'Slight rain',
                    63: 'Moderate rain',
                    65: 'Heavy rain',
                    71: 'Slight snow',
                    73: 'Moderate snow',
                    75: 'Heavy snow',
                    77: 'Snow grains',
                    80: 'Slight rain showers',
                    81: 'Moderate rain showers',
                    82: 'Violent rain showers',
                    85: 'Slight snow showers',
                    86: 'Heavy snow showers',
                    95: 'Thunderstorm',
                    96: 'Thunderstorm with slight hail',
                    99: 'Thunderstorm with heavy hail'
                }
                
                weather_code = current.get('weather_code', 0)
                weather_description = weather_descriptions.get(weather_code, 'Unknown')
                
                return {
                    'temperature': current.get('temperature_2m'),
                    'feels_like': current.get('apparent_temperature'),
                    'humidity': current.get('relative_humidity_2m'),
                    'pressure': current.get('pressure_msl'),
                    'wind_speed': current.get('wind_speed_10m'),
                    'visibility': current.get('visibility'),
                    'weather_main': weather_description.split()[0].title(),
                    'description': weather_description,
                    'weather_code': weather_code
                }
            else:
                print(f"OpenMeteo API returned status code: {response.status_code}")
                print(f"Response content: {response.text}")
        except requests.exceptions.Timeout:
            print("OpenMeteo API request timed out")
        except requests.exceptions.RequestException as e:
            print(f"OpenMeteo API request error: {e}")
        except Exception as e:
            print(f"OpenMeteo API error: {e}")
        
        return None
    
    def get_location_name(self, lat, lon):
        """Get location name from coordinates"""
        try:
            location = self.geolocator.reverse(f"{lat}, {lon}")
            if location:
                return location.address
        except (GeocoderTimedOut, GeocoderUnavailable) as e:
            print(f"Geocoding error: {e}")
        
        return "Unknown Location"
    
    def get_current_location_weather(self):
        """Get weather for current location"""
        location_info = self.get_live_location()
        if not location_info:
            return None
        
        weather_data = self.get_weather_data(location_info['latitude'], location_info['longitude'])
        if not weather_data:
            return None
        
        # Add location info to weather data
        weather_data.update({
            'lat': location_info['latitude'],
            'lon': location_info['longitude'],
            'city': location_info['city']
        })
        
        return {
            'weather': weather_data,
            'location_info': location_info
        }

@login_required
def weather_dashboard(request):
    """Weather dashboard view"""
    return render(request, 'weather/dashboard.html')

@login_required
def get_weather_data(request):
    """Get weather data for a specific location"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            lat = data.get('latitude')
            lon = data.get('longitude')
            
            if not lat or not lon:
                return JsonResponse({'error': 'Latitude and longitude are required'}, status=400)
            
            tracker = LocationWeatherTracker()
            weather_data = tracker.get_weather_data(lat, lon)
            
            if not weather_data:
                return JsonResponse({'error': 'Unable to fetch weather data'}, status=404)
            
            # Get location name
            location_name = tracker.get_location_name(lat, lon)
            
            # Save to database
            try:
                weather_obj = WeatherData.objects.create(
                    user=request.user,
                    location=location_name,
                    latitude=lat,
                    longitude=lon,
                    temperature=weather_data['temperature'],
                    feels_like=weather_data['feels_like'],
                    humidity=weather_data['humidity'],
                    pressure=weather_data['pressure'],
                    wind_speed=weather_data['wind_speed'],
                    visibility=weather_data['visibility'],
                    weather_main=weather_data['weather_main'],
                    description=weather_data['description']
                )
            except Exception as db_error:
                print(f"Database error: {db_error}")
            
            return JsonResponse({
                'temperature': weather_data['temperature'],
                'feels_like': weather_data['feels_like'],
                'humidity': weather_data['humidity'],
                'pressure': weather_data['pressure'],
                'wind_speed': weather_data['wind_speed'],
                'visibility': weather_data['visibility'],
                'weather_main': weather_data['weather_main'],
                'description': weather_data['description'],
                'location': location_name,
                'lat': lat,
                'lon': lon
            })
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'Server error: {str(e)}'}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@login_required
def get_current_location_weather(request):
    """Get weather for user's current location automatically"""
    if request.method == 'POST':
        try:
            # Check if coordinates are provided in request body
            data = json.loads(request.body)
            lat = data.get('latitude')
            lon = data.get('longitude')
            
            if lat and lon:
                # Use provided coordinates
                tracker = LocationWeatherTracker()
                weather_data = tracker.get_weather_data(lat, lon)
                location_name = tracker.get_location_name(lat, lon)
                
                if not weather_data:
                    return JsonResponse({'error': 'Unable to fetch weather data from OpenMeteo API. Please try again.'}, status=404)
                
                # Save to database
                try:
                    weather_obj = WeatherData.objects.create(
                        user=request.user,
                        location=location_name,
                        latitude=lat,
                        longitude=lon,
                        temperature=weather_data['temperature'],
                        feels_like=weather_data['feels_like'],
                        humidity=weather_data['humidity'],
                        pressure=weather_data['pressure'],
                        wind_speed=weather_data['wind_speed'],
                        visibility=weather_data['visibility'],
                        weather_main=weather_data['weather_main'],
                        description=weather_data['description']
                    )
                except Exception as db_error:
                    print(f"Database error: {db_error}")
                    # Continue even if database save fails
                
                return JsonResponse({
                    'temperature': weather_data['temperature'],
                    'feels_like': weather_data['feels_like'],
                    'humidity': weather_data['humidity'],
                    'pressure': weather_data['pressure'],
                    'wind_speed': weather_data['wind_speed'],
                    'visibility': weather_data['visibility'],
                    'weather_main': weather_data['weather_main'],
                    'description': weather_data['description'],
                    'location': location_name,
                    'lat': lat,
                    'lon': lon
                })
            else:
                # Use IP-based location detection
                tracker = LocationWeatherTracker()
                result = tracker.get_current_location_weather()
                
                if not result:
                    return JsonResponse({'error': 'Unable to detect current location. Please allow location access or try again.'}, status=404)
                
                weather_data = result['weather']
                location_info = result['location_info']
                
                # Save to database
                try:
                    weather_obj = WeatherData.objects.create(
                        user=request.user,
                        location=weather_data['city'],
                        latitude=weather_data['lat'],
                        longitude=weather_data['lon'],
                        temperature=weather_data['temperature'],
                        feels_like=weather_data['feels_like'],
                        humidity=weather_data['humidity'],
                        pressure=weather_data['pressure'],
                        wind_speed=weather_data['wind_speed'],
                        visibility=weather_data['visibility'],
                        weather_main=weather_data['weather_main'],
                        description=weather_data['description']
                    )
                except Exception as db_error:
                    print(f"Database error: {db_error}")
                    # Continue even if database save fails
                
                return JsonResponse({
                    'temperature': weather_data['temperature'],
                    'feels_like': weather_data['feels_like'],
                    'humidity': weather_data['humidity'],
                    'pressure': weather_data['pressure'],
                    'wind_speed': weather_data['wind_speed'],
                    'visibility': weather_data['visibility'],
                    'weather_main': weather_data['weather_main'],
                    'description': weather_data['description'],
                    'location': weather_data['city'],
                    'lat': weather_data['lat'],
                    'lon': weather_data['lon']
                })
                
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data in request'}, status=400)
        except Exception as e:
            print(f"Error in get_current_location_weather: {e}")
            return JsonResponse({'error': 'Server error occurred while fetching weather data. Please try again.'}, status=500)
    
    return JsonResponse({'error': 'Invalid request method. Use POST.'}, status=405)

@login_required
def get_forecast_data(request):
    """Get 5-day weather forecast using OpenMeteo API"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            lat = data.get('latitude')
            lon = data.get('longitude')
            
            if not lat or not lon:
                return JsonResponse({'error': 'Latitude and longitude are required'}, status=400)
            
            # Use OpenMeteo API for consistency
            url = f"https://api.open-meteo.com/v1/forecast"
            params = {
                'latitude': lat,
                'longitude': lon,
                'hourly': 'temperature_2m,relative_humidity_2m,weather_code',
                'daily': 'temperature_2m_max,temperature_2m_min,precipitation_probability_max',
                'timezone': 'auto',
                'forecast_days': 5
            }
            
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                
                # Convert weather codes to descriptions
                weather_descriptions = {
                    0: 'Clear sky', 1: 'Mainly clear', 2: 'Partly cloudy', 3: 'Overcast',
                    45: 'Foggy', 48: 'Depositing rime fog', 51: 'Light drizzle',
                    53: 'Moderate drizzle', 55: 'Dense drizzle', 61: 'Slight rain',
                    63: 'Moderate rain', 65: 'Heavy rain', 71: 'Slight snow',
                    73: 'Moderate snow', 75: 'Heavy snow', 77: 'Snow grains',
                    80: 'Slight rain showers', 81: 'Moderate rain showers',
                    82: 'Violent rain showers', 85: 'Slight snow showers',
                    86: 'Heavy snow showers', 95: 'Thunderstorm',
                    96: 'Thunderstorm with slight hail', 99: 'Thunderstorm with heavy hail'
                }
                
                forecast_list = []
                for i in range(5):  # 5-day forecast
                    if i < len(data['daily']['time']):
                        weather_code = data['hourly']['weather_code'][i * 24] if i * 24 < len(data['hourly']['weather_code']) else 0
                        forecast_list.append({
                            'date': data['daily']['time'][i],
                            'max_temp': data['daily']['temperature_2m_max'][i],
                            'min_temp': data['daily']['temperature_2m_min'][i],
                            'humidity': data['hourly']['relative_humidity_2m'][i * 12] if i * 12 < len(data['hourly']['relative_humidity_2m']) else 0,
                            'description': weather_descriptions.get(weather_code, 'Unknown'),
                            'precipitation_probability': data['daily']['precipitation_probability_max'][i]
                        })
                
                return JsonResponse({'forecast': forecast_list})
            else:
                return JsonResponse({'error': 'Unable to fetch forecast data'}, status=404)
                
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'Server error: {str(e)}'}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@login_required
def get_weather_history(request):
    """Get user's weather history"""
    if request.method == 'GET':
        try:
            # Get the last 10 weather records for the user
            weather_history = WeatherData.objects.filter(user=request.user).order_by('-timestamp')[:10]
            
            history_list = []
            for record in weather_history:
                history_list.append({
                    'location': record.location,
                    'temperature': record.temperature,
                    'humidity': record.humidity,
                    'description': record.description,
                    'timestamp': record.timestamp.strftime('%Y-%m-%d %H:%M'),
                    'coordinates': f"{record.latitude:.4f}, {record.longitude:.4f}" if record.latitude and record.longitude else 'N/A'
                })
            
            return JsonResponse({'history': history_list})
            
        except Exception as e:
            return JsonResponse({'error': f'Server error: {str(e)}'}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)
