import requests
import re
from geopy.geocoders import Nominatim

def get_coordenadas(direccion,ciudad,departamento):
    direccion1=direccion+", "+ciudad+", "+departamento
    geolocator = Nominatim(user_agent="avalpredict")
    location = geolocator.geocode(direccion1)
    latitud = location.latitude
    longitud= location.longitude
    return latitud,longitud