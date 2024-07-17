from django.urls import path

from mainapp.apps import MainappConfig
from mainapp.views import HomePage, WeatherFormView, autocomplete_cities, CatListView

app_name = MainappConfig.name

urlpatterns = [
    path("", HomePage.as_view(), name="home"),
    path("weather/", CatListView.as_view(), name="weather"),
    path("weather_form/", WeatherFormView.as_view(), name="weather_form"),
    path('autocomplete/cities/', autocomplete_cities, name='autocomplete_cities'),
]
