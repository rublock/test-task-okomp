from django.urls import path

from mainapp.apps import MainappConfig
from mainapp.views import HomePage, WeatherFormView, CityAutocompleteView, WeatherListView

app_name = MainappConfig.name

urlpatterns = [
    path("", HomePage.as_view(), name="home"),
    path("weather/", WeatherListView.as_view(), name="weather"),
    path("weather_form/", WeatherFormView.as_view(), name="weather_form"),
    path('autocomplete/cities/', CityAutocompleteView.as_view(), name='autocomplete_cities'),
]
