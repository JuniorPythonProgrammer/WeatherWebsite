from django.shortcuts import render
from .config import open_weather_token
import requests
import datetime

def home(request):

    return render(request, 'weather/home.html')

def weather_now(request):
    city = request.GET.get('search', '')

    if city:
        r = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric&lang=ru")
        data = r.json()

        context = {
            'city': data["name"],
            'cur_temp': round(data["main"]["temp"]),
            'humidity': data["main"]["humidity"],
            'pressure': data["main"]["pressure"],
            'wind_speed': round(data["wind"]["speed"]),
            'description_weather': data["weather"][0]["description"],
            'weathon_icon': data["weather"][0]["icon"],
            'precipitation': 0,
        }
        if 'rain' in data and 'snow' in data:
            context["precipitation"] = round(data["rain"]["1h"] + data["snow"]["1h"], 1)
        elif 'rain' in data:
            context["precipitation"] = round(data["rain"]["1h"], 1)
        elif 'snow' in data:
            context["precipitation"] = round(data["snow"]["1h"], 1)
        else:
            context["precipitation"] = 0
    else:
        pass
    return render(request, 'weather/weather_now.html', context)
