# Django Weather App - views.py
# This is my Django backend that handles web requests

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import urllib.request
import urllib.parse
import json
from typing import Dict, Optional
import logging

# Set up logging so I can see what's happening
logger = logging.getLogger(__name__)


class WeatherAPI:
	"""
	My Weather API class for Django web app
	I'm using Python's built-in urllib (no extra packages needed!)
	"""

	def __init__(self):
		# My OpenWeatherMap API key
		self.api_key = "09a9d72286be6b48b768f4a67fb4312c"
		self.base_url = "http://api.openweathermap.org/data/2.5/weather"

	def get_weather_data(self, city: str) -> Optional[Dict]:
		"""
		I fetch weather data using Python's built-in urllib

		Args:
			city (str): The city name I want weather for

		Returns:
			dict: Weather data or None if there's an error
		"""
		try:
			# I build my URL with parameters
			params = {
				'q': city,
				'appid': self.api_key,
				'units': 'metric'  # I want Celsius
			}

			url_params = urllib.parse.urlencode(params)
			full_url = f"{self.base_url}?{url_params}"

			logger.info(f"Making API request for {city}")

			# I make the request
			with urllib.request.urlopen(full_url, timeout=10) as response:
				if response.status == 200:
					data = response.read().decode('utf-8')
					return json.loads(data)
				else:
					logger.error(f"API request failed with status: {response.status}")
					return None

		except urllib.error.HTTPError as e:
			logger.error(f"HTTP Error {e.code} for city: {city}")
			return None
		except urllib.error.URLError as e:
			logger.error(f"URL Error: {e.reason}")
			return None
		except Exception as e:
			logger.error(f"Unexpected error: {e}")
			return None

	def parse_weather_data(self, raw_data: Dict) -> Dict:
		"""
		I convert raw API data into clean format for my web app
		"""
		try:
			weather_info = {
				'city': raw_data['name'],
				'country': raw_data['sys']['country'],
				'temperature': round(raw_data['main']['temp'], 1),
				'feels_like': round(raw_data['main']['feels_like'], 1),
				'condition': raw_data['weather'][0]['main'],
				'description': raw_data['weather'][0]['description'].title(),
				'humidity': raw_data['main']['humidity'],
				'wind_speed': raw_data['wind']['speed'],
				'pressure': raw_data['main']['pressure'],
				'icon': raw_data['weather'][0]['icon']
			}
			return weather_info
		except KeyError as e:
			logger.error(f"Missing data in API response: {e}")
			return {}


# My Django Views (these handle web requests)

def home(request):
	"""
	My main page view - this shows the weather app homepage
	"""
	return render(request, 'weather/index.html')


@csrf_exempt
def get_weather_api(request):
	"""
	My API endpoint that my JavaScript calls to get weather data
	This returns JSON data that my frontend can use
	"""
	if request.method == 'POST':
		try:
			# I get the city name from the request
			data = json.loads(request.body)
			city = data.get('city', '').strip()

			if not city:
				return JsonResponse({
					'success': False,
					'error': 'I need a city name',
					'data': None
				})

			# I get weather data using my API class
			weather_api = WeatherAPI()
			raw_data = weather_api.get_weather_data(city)

			if raw_data:
				weather_data = weather_api.parse_weather_data(raw_data)
				return JsonResponse({
					'success': True,
					'error': None,
					'data': weather_data
				})
			else:
				return JsonResponse({
					'success': False,
					'error': f'I could not find weather data for {city}',
					'data': None
				})

		except json.JSONDecodeError:
			return JsonResponse({
				'success': False,
				'error': 'Invalid request format',
				'data': None
			})
		except Exception as e:
			logger.error(f"Error in get_weather_api: {e}")
			return JsonResponse({
				'success': False,
				'error': 'Something went wrong on my server',
				'data': None
			})

	return JsonResponse({
		'success': False,
		'error': 'I only accept POST requests',
		'data': None
	})


# My URL configuration (urls.py)
"""
This is what goes in my urls.py file:

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('api/weather/', views.get_weather_api, name='get_weather'),
]
"""

# My Django settings configuration (settings.py additions)
"""
Add this to my INSTALLED_APPS in settings.py:

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'weather',  # My weather app
]

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
"""