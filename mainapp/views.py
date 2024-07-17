import logging
import os

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, FormView

from .forms import CityForm
from .models import Session, SessionUrl, City
from .services.coordinates import get_coordinates

logger = logging.getLogger(__name__)

TOKEN = os.environ.get("TOKEN")
SECRET_KEY = os.environ.get("SECRET_KEY")


class HomePage(TemplateView):
    """Home page"""

    template_name = "mainapp/index.html"
    context_object_name = "cats"
    paginate_by = 2

    def get(self, request, *args, **kwargs):
        """
        Метод проверяет есть ли ключ сессии в браузере (Application - Cookie),
        если его нет, то ключ устанавливается.
        Устанавливается на какой срок действует ключ.
        Проверяется есть ли уже такой ключ, если нет то
        ключ сохраняется в таблицу Session.
        Проверяется есть ли в БД записи с url изображений котов согласно
        ключу сессии. Если есть-то редирект на weather/.
        Если нет-то открывается главная страница
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
        if SessionUrl.objects.filter(session_key_id=id).exists():
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


def autocomplete_cities(request):
    city_name = request.GET.get('city')
    cities = City.objects.filter(name__istartswith=city_name)
    if cities.exists():  # Проверяем, есть ли города, удовлетворяющие условию
        data = [{'name': city.name} for city in cities]
        return JsonResponse(data[:10], safe=False)
    else:
        return JsonResponse([], safe=False)








class CatListView(ListView):
    """Страница с котами"""

    template_name = "mainapp/weather.html"
    context_object_name = "weather"
    paginate_by = 2

    def get_queryset(self):
        """
        Метод проверяет есть ли uls котов в БД по ключу сесссии.
        Если есть-то отправляет в браузер content со списком url котов.
        Если нет-то запрашивает сервис API get_weather() и добавляет url в БД.
        Отправляет в браузер content со списком url котов из БД.
        """
        sessionid = self.request.session.session_key
        session = Session.objects.get(key=sessionid)
        content = []
        key = Session.objects.get(key=sessionid)
        id = key.id

        if SessionUrl.objects.filter(session_key_id=id).exists():
            urls = SessionUrl.objects.filter(session_key_id=id)
            for i in urls:
                content.append(i.url)
            return content

        else:
            city = self.request.GET.get("city")
            content = get_coordinates(TOKEN, SECRET_KEY, city)
            logger.info(f"LOG MESSAGE: {content}")
            for i in content:
                if not SessionUrl.objects.filter(session_key=session, url=i).exists():
                    url = SessionUrl(session_key=session, url=i)
                    url.save()
            return content
