import os
import json
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from config.settings import BASE_DIR
from mainapp.models import City


with open(BASE_DIR / "var/cities.json", 'r') as file:
    cities_data = json.load(file)

for city_data in cities_data["city"]:
    city = City(
        name=city_data["name"]
    )
    city.save()
