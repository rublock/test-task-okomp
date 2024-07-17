from dadata import Dadata
from .weather_api import get_weather


def get_coordinates(TOKEN, SECRET_KEY, city):
    coordinates = {}
    dadata = Dadata(TOKEN, SECRET_KEY)
    r = dadata.clean(name="address", source=city)
    coordinates['geo_lat'] = r["geo_lat"]
    coordinates['geo_lon'] = r["geo_lon"]
    result = get_weather(coordinates)
    return result
