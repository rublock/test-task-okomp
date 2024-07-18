import logging
import os

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, TemplateView, FormView

from .forms import CityForm
from .models import Session, City, Temperature
from .services.coordinates import get_coordinates

logger = logging.getLogger(__name__)

TOKEN = os.environ.get("TOKEN")
SECRET_KEY = os.environ.get("SECRET_KEY")


class HomePage(TemplateView):
    """Home page"""

    template_name = "mainapp/index.html"
    context_object_name = "cats"

    def get(self, request, *args, **kwargs):
        """
        Метод проверяет есть ли ключ сессии в браузере (Application - Cookie),
        если его нет, то ключ устанавливается.
        Устанавливается на какой срок действует ключ.
        Проверяется есть ли уже такой ключ, если нет то
        ключ сохраняется в таблицу Session.
        Проверяется есть ли в БД записи с погодой согласно
        ключу сессии. Если есть-то редирект на weather/.
        Если нет-то открывается главная страница.
        """
        if not request.session.session_key:
            request.session.create()
            request.session.set_expiry(settings.SESSION_COOKIE_AGE)

        sessionid = request.session.session_key

        if not Session.objects.filter(key=sessionid).exists():
            data = Session.objects.create(key=sessionid)
            data.save()

        key = Session.objects.get(key=sessionid)
        id = key.id
        if Temperature.objects.filter(session=id).exists():
            return redirect("weather/")
        else:
            return super().get(request, *args, **kwargs)


class WeatherFormView(FormView):
    """Форма запроса погоды по городу"""

    template_name = "mainapp/weather_form.html"
    form_class = CityForm
    success_url = reverse_lazy('mainapp:weather')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class CityAutocompleteView(View):
    """Всплывающие подсказки городов"""
    def get(self, request, *args, **kwargs):
        city_name = request.GET.get('city', '')
        cities = City.objects.filter(name__istartswith=city_name)
        data = [{'name': city.name} for city in cities[:10]]
        return JsonResponse(data, safe=False)

    def post(self, request, *args, **kwargs):
        return redirect(reverse('mainapp:weather'))


class WeatherListView(ListView):
    """Страница с погодой"""

    template_name = "mainapp/weather.html"
    context_object_name = "weather"

    def get_queryset(self):
        """
        Метод проверяет есть ли погода по ключу сесссии.
        Если есть-то отправляет в браузер content с погодой.
        Если нет-то запрашивает сервис API get_weather() и добавляет погоду в БД.
        Отправляет в браузер content с погодой из БД.
        """
        sessionid = self.request.session.session_key
        date = []
        temp = []
        key = Session.objects.get(key=sessionid)
        session_key_id = key.id

        if Temperature.objects.filter(session=session_key_id).exists():
            sql_data = Temperature.objects.filter(session=session_key_id)

            for i in sql_data:
                date.append(i.time)
                temp.append(i.temperature)

            content = dict(zip(date, temp))
            return content

        else:
            city = self.request.GET.get("city")
            city_name = City.objects.get(name=city)
            city_id = city_name.id
            content = get_coordinates(TOKEN, SECRET_KEY, city)
            logger.info(f"LOG MESSAGE: {content}")
            if not Temperature.objects.filter(session=session_key_id).exists():
                for key, value in content.items():
                    temperature = Temperature(time=key, temperature=value, city_id=city_id, session_id=session_key_id)
                    temperature.save()
            return content
