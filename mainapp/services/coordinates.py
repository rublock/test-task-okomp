import os

from dadata import Dadata


def get_coordinates(TOKEN, SECRET_KEY, city):
    dadata = Dadata(TOKEN, SECRET_KEY)
    r = dadata.clean(name="address", source=city)
    print(r["geo_lat"], r["geo_lon"])
