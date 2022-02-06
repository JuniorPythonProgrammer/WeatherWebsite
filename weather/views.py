from django.shortcuts import render
from .config import open_weather_token
import requests
import datetime

def home(request):

    return render(request, 'weather/home.html')

def weather_now(city):
    r = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric&lang=ru")
    data = r.json()

    weather = {
        'city': data["name"],
        'cur_temp': round(data["main"]["temp"]),
        'humidity': data["main"]["humidity"],
        'pressure': data["main"]["pressure"],
        'wind_speed': round(data["wind"]["speed"]),
        'description_weather': data["weather"][0]["description"],
        'weather_icon': data["weather"][0]["icon"],
        'precipitation': 0,
    }
    if 'rain' in data and 'snow' in data:
        weather["precipitation"] = round(data["rain"]["1h"] + data["snow"]["1h"], 1)
    elif 'rain' in data:
        weather["precipitation"] = round(data["rain"]["1h"], 1)
    elif 'snow' in data:
        weather["precipitation"] = round(data["snow"]["1h"], 1)
    else:
        weather["precipitation"] = 0
    
    return weather

def search_weather_now(request):
    city = request.GET.get('search', '')

    if city:
        context = weather_now(city)
    else:
        pass
    return render(request, 'weather/weather_now.html', context)

def radio_button_weather_now(request, city):
    context = weather_now(city)

    return render(request, 'weather/weather_now.html', context)

def weather_8_day(request, city):
    r = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric&lang=ru")
    data = r.json()

    lat = data["coord"]["lat"]
    lon = data["coord"]["lon"]

    r = requests.get(f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=current,minutely,hourly,alerts&appid={open_weather_token}&units=metric&lang=ru")
    data = r.json()

    context = {
        'city': city,
        'weather_8day':[]
    }

    for day in range(8):
        context["weather_8day"].append(dict.fromkeys(['date', 'max_temp', 'min_temp', 'humidity', 'pressure', 'precipitation',
         'wind_speed', 'description_weather', 'weather_icon']))
        context["weather_8day"][day]["date"] = datetime.datetime.fromtimestamp(data["daily"][day]["dt"]).strftime('%d.%m.%Y')
        context["weather_8day"][day]["max_temp"] = round(data["daily"][day]["temp"]["max"])
        context["weather_8day"][day]["min_temp"] = round(data["daily"][day]["temp"]["min"])
        context["weather_8day"][day]["humidity"] = data["daily"][day]["humidity"]
        context["weather_8day"][day]["pressure"] = data["daily"][day]["pressure"]
        context["weather_8day"][day]["wind_speed"] = round(data["daily"][day]["wind_speed"])
        context["weather_8day"][day]["description_weather"] = data["daily"][day]["weather"][0]["description"]
        context["weather_8day"][day]["weather_icon"] = data["daily"][day]["weather"][0]["icon"]

        if 'rain' in data["daily"][day] and 'snow' in data["daily"][day]:
            context["weather_8day"][day]["precipitation"] = round(data["daily"][day]["rain"] + data["daily"][day]["snow"], 1)
        elif 'rain' in data["daily"][day]:
            context["weather_8day"][day]["precipitation"] = round(data["daily"][day]["rain"], 1)
        elif 'snow' in data["daily"][day]:
            context["weather_8day"][day]["precipitation"] = round(data["daily"][day]["snow"], 1)
        else:
            context["weather_8day"][day]["precipitation"] = 0
        
    return render(request, 'weather/weather_8_day.html', context)
