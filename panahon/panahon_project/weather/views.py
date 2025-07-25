from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import urllib.request
import urllib.parse
import json
from typing import Dict, Optional, Tuple
import logging
import time
from datetime import datetime

# Set up logging
logger = logging.getLogger(__name__)


class WeatherAPI:
	def __init__(self):
		self.api_key = "09a9d72286be6b48b768f4a67fb4312c"
		self.base_url = "http://api.openweathermap.org/data/2.5/weather"
		self.cache = {}
		self.cache_duration = 300  # 5 minutes

	def get_weather_data(self, city: str) -> Tuple[Optional[Dict], Optional[str]]:
		cache_key = city.lower().strip()
		current_time = time.time()

		if cache_key in self.cache:
			cached_data, timestamp = self.cache[cache_key]
			if current_time - timestamp < self.cache_duration:
				return cached_data, None

		try:
			params = {
				'q': city,
				'appid': self.api_key,
				'units': 'metric'
			}

			url_params = urllib.parse.urlencode(params)
			full_url = f"{self.base_url}?{url_params}"

			request = urllib.request.Request(
				full_url,
				headers={'User-Agent': 'Panahon-Weather-App/1.0'}
			)

			with urllib.request.urlopen(request, timeout=10) as response:
				if response.status == 200:
					data = response.read().decode('utf-8')
					weather_data = json.loads(data)
					self.cache[cache_key] = (weather_data, current_time)
					return weather_data, None
				else:
					return None, "Weather service temporarily unavailable"

		except urllib.error.HTTPError as e:
			if e.code == 404:
				return None, f"City '{city}' not found. Please check the spelling."
			elif e.code == 401:
				return None, "API key error. Please check your API key."
			else:
				return None, "Weather service error. Please try again later."

		except Exception as e:
			return None, "An unexpected error occurred. Please try again."

	def parse_weather_data(self, raw_data: Dict) -> Dict:
		try:
			main = raw_data.get('main', {})
			weather = raw_data.get('weather', [{}])[0]
			wind = raw_data.get('wind', {})
			sys = raw_data.get('sys', {})

			return {
				'city': raw_data.get('name', 'Unknown'),
				'country': sys.get('country', 'Unknown'),
				'temperature': round(main.get('temp', 0), 1),
				'feels_like': round(main.get('feels_like', 0), 1),
				'condition': weather.get('main', 'Unknown'),
				'description': weather.get('description', 'Unknown').title(),
				'humidity': main.get('humidity', 0),
				'wind_speed': round(wind.get('speed', 0), 1),
				'pressure': main.get('pressure', 0),
				'icon': weather.get('icon', '01d'),
				'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
			}
		except Exception:
			return {
				'city': 'Unknown',
				'country': 'Unknown',
				'temperature': 0,
				'feels_like': 0,
				'condition': 'Unknown',
				'description': 'Unknown',
				'humidity': 0,
				'wind_speed': 0,
				'pressure': 0,
				'icon': '01d',
				'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
			}


def home(request):
	return render(request, 'weather/index.html')


@csrf_exempt
def get_weather_api(request):
	if request.method == 'POST':
		try:
			data = json.loads(request.body)
			city = data.get('city', '').strip()

			if not city:
				return JsonResponse({
					'success': False,
					'error': 'Please enter a city name',
					'data': None
				})

			weather_api = WeatherAPI()
			raw_data, error_message = weather_api.get_weather_data(city)

			if raw_data and not error_message:
				weather_data = weather_api.parse_weather_data(raw_data)
				return JsonResponse({
					'success': True,
					'error': None,
					'data': weather_data
				})
			else:
				return JsonResponse({
					'success': False,
					'error': error_message or f'Could not get weather data for {city}',
					'data': None
				})

		except Exception as e:
			return JsonResponse({
				'success': False,
				'error': 'Something went wrong on the server',
				'data': None
			})

	return JsonResponse({
		'success': False,
		'error': 'Only POST requests are allowed',
		'data': None
	})