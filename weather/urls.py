from django.urls import path
from .views import *

urlpatterns = [
    path('', home),
    path('weather/', weather_now, name='weather_now_url'),

]
