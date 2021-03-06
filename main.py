import numpy as np
import pandas as pd
import tensorflow as tf
import glob
import os
from getpass import getpass
from sklearn.model_selection import train_test_split
from sqlalchemy import create_engine

#from src.data.make_dataset import leer_csv_fr,leer_csv_datosigac
#from src.features.limpieza_de_datos_igac import limpieza_datos
from src.features.limpieza_datos_exogena import concat_data_exogena
from src.data.fincaraiz_webscrapping import webscrapping
from src.features.api_here import near_places
from src.visualization.eda_exogena import eda_exogena

if __name__ == "__main__":
    
    # conectar a base de datos
    engine1 = create_engine('postgresql://topscorer:topscorer@67.205.164.197:5432/db_crudos')
    engine2 = create_engine('postgresql://topscorer:topscorer@67.205.164.197:5432/db_resultados')

    # read files
    DATA_PATH = os.path.join(os.getcwd(), "data")
    MODELS_PATH = os.path.join(os.getcwd(), "models")
    # model_path = os.path.join(MODELS_PATH, model_name + "_" + model_version)
    IMAGE_PATH=os.path.join(os.getcwd(),'reports','figures')
    
    # parametros fijos
    lista_municipios = ["villavicencio", "fusagasuga", "manizales"]
    weblinks = [
        "https://www.fincaraiz.com.co/Inmuebles_Comerciales/venta/villavicencio/",
        "https://www.fincaraiz.com.co/Inmuebles_Comerciales/venta/fusagasuga/",
        "https://www.fincaraiz.com.co/Inmuebles_Comerciales/venta/manizales/",
        "https://www.fincaraiz.com.co/Vivienda/venta/villavicencio/",
        "https://www.fincaraiz.com.co/Vivienda/venta/fusagasuga/",
        "https://www.fincaraiz.com.co/Vivienda/venta/manizales/",
    ]
    
    #carga y limpieza de datos igac
    #avaluo,general_asp,detail_asp,dest=leer_csv_datosigac(DATA_PATH)
    #limpieza_datos(DATA_PATH,avaluo,general_asp,detail_asp)
    
    #lectura de datos
    datos_descargados = 1  # para no hacer el scrapping
    if datos_descargados == 0:
        for weblink in weblinks:
            webscrapping(DATA_PATH, weblink, engine1)
            print(weblink, 'ha sido creado') 
   
    # leer los datos del webscapping, los concatena, los limpia
    datos_modelo = concat_data_exogena(
        DATA_PATH, engine=engine1, engine2=engine2, 
        municipios_prop=lista_municipios
    ) 
    
    # preguntar por la key api de here
    api_key = getpass("Introduzca la KEY de la API de HERE:")
    datos_lugares = near_places(api_key, data=datos_modelo, engine=engine2)
    eda_exogena(DATA_PATH, IMAGE_PATH, engine2)

    # despues de finalizar todo cerrar conexion
    engine1.close()
    engine2.close()
    