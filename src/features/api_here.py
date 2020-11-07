# -*- coding: utf-8 -*-

# import modules
import herepy
import numpy as np
import pandas as pd

def _api_places(conn, lat, lon, radius=1000, place="hospital"):
    """Metodo privado para hacer una consulta de lugares cercanos"""
    response = conn.places_in_circle([lat, lon], radius, place)
    return response.as_dict()

def _lista_lugares(conn, df, lat, lon, radius=1000, place="hospital"):
    """Metodo privado para retornar la cantidad de lugares cercanos a
    varios puntos establecidos en un dataframe
    """
    new_df = df[[lat, lon]].values
    fun = lambda x: len(_api_places(conn, x[0], x[1], radius, place)["items"])
    return list(map(fun, new_df))

def near_places(
    api_key, data_path="", file_name="", data=None, lat="lat", lon="lon", 
    places_list=[], return_df=True
):
    """Lectura de la informacion limpia y consulta de la api"""

    # verificar tipos de datos
    if not isinstance(api_key, str):
        raise TypeError("Error, data_path debe ser de tipo string")
    if not isinstance(data_path, str):
        raise TypeError("Error, data_path debe ser de tipo string")
    if not isinstance(file_name, str):
        raise TypeError("Error, file_name debe ser de tipo string")
    if data is not None:
        if not isinstance(data, pd.DataFrame):
            raise TypeError("Error, municipios_prop debe ser de tipo list")
    if not isinstance(lat, str):
        raise TypeError("Error, nombre columna lat debe ser de tipo string")
    if not isinstance(lon, str):
        raise TypeError("Error, nombre columna lon debe ser de tipo string")
    if not isinstance(places_list, list):
        raise TypeError("Error, municipios_prop debe ser de tipo list")
    
    # verificar informacion
    if data is None and file_name == "":
        raise RuntimeError("Debe ingresar un dataframe o un archivo para leer")
    
    # carga de la informacion
    if data is None:
        if not file_name.endswith(".csv"):
            raise RuntimeError("Error, datos deben estar en formato csv")
        data = pd.read_csv(data_path + file_name)

    # verificar que la informacion tenga lat y lon
    if lat not in data.columns:
        raise RuntimeError("Dataframe no contiene columna {}".format(lat))
    if lon not in data.columns:
        raise RuntimeError("Dataframe no contiene columna {}".format(lon))

    # hacer la conexion
    conn = herepy.places_api.PlacesApi(api_key)

    # definir lugares a buscar
    if places_list == []:
        places_list = [
            "healt", "hospital",
            "cafe", "restaurant", "bar", "club",
            "entertainment", "park", "museum", "zoo", "church", "hotel",
            "education", "university", "school",  
            "shopping mall", "shop", "supermarket",
            "transport", "police",
        ]
        # old list
        #places_list = [
        #"hospital", "cafe", "park", "church", "shopping mall", "school", 
        #"univerity", "transport", "police", "shop", "supermarket",
        #"hotel", "education"
        #]
        

    # hacer el request
    for place in places_list:
        data[place] = _lista_lugares(conn, data, lat, lon, place=place)

    # guardar y retornar
    new_file_name = data_path + file_name.replace(".csv", "_places.csv")
    data.to_csv(new_file_name, index=False)
    print("Archivo guardado en {}".format(new_file_name))
    
    if return_df:
        return data

