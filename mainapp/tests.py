import unittest
from django.urls import reverse
from django.test import TestCase, RequestFactory
from mainapp.views import WeatherFormView
from mainapp.models import City  # Подключите вашу модель City, если она не указана


class WeatherFormViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_form_valid(self):
        request = self.factory.post(reverse('mainapp:weather'), {'name': 'Example City'})
        response = WeatherFormView.as_view()(request)
        self.assertTrue(City.objects.filter(name='Example City').exists())
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/weather/')

