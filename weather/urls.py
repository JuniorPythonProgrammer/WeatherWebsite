from django.urls import path
from .views import *

urlpatterns = [
    path('', home),
    path('weather/', weather_now, name='weather_now_url'),
    path('weather8/<str:city>', weather_8_day, name='weather_8_day_url'),
]
