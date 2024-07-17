from django.urls import path

from mainapp.apps import MainappConfig
from mainapp.views import CatListView, FloatFormView, HomePage

app_name = MainappConfig.name

urlpatterns = [
    path("", HomePage.as_view(), name="home"),
    path("weather/", CatListView.as_view(), name="weather"),
    path("float_form/", FloatFormView.as_view(), name="float_form"),
]
