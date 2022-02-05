from django.urls import path
from .views import *

urlpatterns = [
    path('weather/', home, name='home_url'),
    path('weather/now/', search_weather_now, name='search_weather_now_url'),
    path('weather/now/<str:city>', radio_button_weather_now, name='radio_button_weather_now_url'),
    path('weather/eightday/<str:city>', weather_8_day, name='weather_8_day_url'),
]
