import requests
import re
from geopy.geocoders import Nominatim

def get_coordenadas(direccion,ciudad,departamento):
    """
    This function gets an address and returns coordinates using Nominatim

    Parameters
    ----------
    direccion : String
        House address
    ciudad : String
        Address municipality
    departamento : String
        Address department

    Returns
    -------
    latitud : Float
        Adress latitude
    longitud : Float
        Address Longitude

    """
    direccion1=direccion+", "+ciudad+", "+departamento
    geolocator = Nominatim(user_agent="avalpredict")
    location = geolocator.geocode(direccion1)
    latitud = location.latitude
    longitud= location.longitude
    return latitud,longitud