from django.shortcuts import render, redirect
import requests
from .models import City
from .forms import CityForm
from django.contrib import messages

def home(request):
    url = 'http://api.weatherapi.com/v1/forecast.json?key=c0365a0335364a938f063313240704&q={}&days=7&aqi=no&alerts=no'
    weather_data = []
    city_obj = ''
    cities = City.objects.all()

    form = CityForm()
    if request.method == "POST":
        form = CityForm(request.POST)
        if form.is_valid():
            city_obj = form.cleaned_data['name']
            if City.objects.filter(name=city_obj).exists():
                messages.info(request, 'The city is already in the database')
                return redirect('home')
            else:
                form.save()
                messages.info(request, 'The city has been added the database')
                return redirect('home')

    for city in cities:
        city_weather = requests.get(url.format(city)).json()
        weather = {
            "location": city_weather.get("location")["name"],
            "temp": city_weather.get("current")["temp_c"],
            "condition_text": city_weather.get("current")["condition"]['text'],
            "condition_icon": city_weather.get("current")["condition"]['icon'],
        }
        weather_data.append(weather)

    return render(request, 'weather/home.html', {'weather_data': weather_data, 'form': form})
