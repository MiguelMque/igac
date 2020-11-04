import numpy as np
import pandas as pd
import tensorflow as tf
import glob
import os
from sklearn.model_selection import train_test_split

#from src.data.make_dataset import leer_csv_fr,leer_csv_datosigac
#from src.features.limpieza_de_datos_igac import limpieza_datos
from src.features.limpieza_datos_exogena import concat_data_exogena
from src.data.fincaraiz_webscrapping import webscrapping

if __name__ == "__main__":
    DATA_PATH = os.path.join(os.getcwd(), "data")
    MODELS_PATH = os.path.join(os.getcwd(), "models")
    #model_path = os.path.join(MODELS_PATH, model_name + "_" + model_version)
    IMAGES_PATH=os.path.join(os.getcwd(),'reports','figures')
    lista_municipios=["villavicencio", "fusagasuga", "manizales"]
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
    datos_descargados = 1  #para no hacer el scrapping
    if datos_descargados==0:
        for weblink in weblinks:
            webscrapping(DATA_PATH,weblink)
            print(weblink,' creado') 
   
    datos_modelo=concat_data_exogena(DATA_PATH,lista_municipios)#leer los datos del webscapping, los concatena, los limpia y agrega dummies
    

    
    