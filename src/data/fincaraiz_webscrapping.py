# -*- coding: utf-8 -*-
"""
#-------------------------------------------------------------------------
# Author: Juan Pablo Trujillo Alviz 
# github: juapatral
# CD: 2020-09-24 
# LUD: 2020-09-24
# Description: webscrapping of fincaraiz website
#
#
# example of use:
#>>>medellin = webscrapping(
#               "path_of_directory", 
#               "www.fincaraiz.com.co/Vivienda/venta/medellin"
#)
#-------------------------------------------------------------------------
"""

### webscrapping fincaraiz

## importar librerias

import numpy as np
import pandas as pd
import re
import datetime as dt
import requests
from bs4 import BeautifulSoup
import urllib3
import time
import os

## crear funciones propias

def diccionario(nuevo_texto):
    """Crea un diccionario con una lista de tuplas llave valor, 
    si no tiene valor queda nulo
    """

    if not isinstance(nuevo_texto, list):
        raise RuntimeError("Error, nuevo_texto debe ser de tipo lista")
    
    # crear diciconario vacio
    dicc = {}

    # iterar sobre la lista
    for tupla in nuevo_texto:
        # crear variable
        tupla2 = tupla[1] if tupla[1]!="" else None
        dicc[tupla[0]] = tupla2
    return dicc

## parametros fijos

def webscrapping(data_path, weblink, max_number_page=7000):
    """
    Webscrapping del sitio fincaraiz. Cada inmueble se demora ~1 seg.
    
    Debe proporcionar un data_path donde guardar la información
    Debe proporcionar weblink de la url a extraer la información tipo
        www.fincaraiz.com.co/Vivienda/venta/medellin
    Puede indicar el número máximo de páginas a extraer con max_number_page
    """

    if not isinstance(data_path, str):
        raise TypeError("Error, data_path debe ser de tipo string")
    if not isinstance(weblink, str):
        raise TypeError("Error, weblink debe ser de tipo string")
    if not isinstance(max_number_page, int):
        raise TypeError("Error, max_number_page debe ser de tipo int")
    
    # date time
    now = dt.datetime.now()

    # conteo de paginas y maximo numero de paginas a buscar
    number_page = 1

    # listas vacias de url y diccionario de datos
    urls, lista_dicc = [], []

    # nombrar el weblink
    ubicacion = weblink.split("/")[5].lower()
    tipo_inmueble = weblink.split("/")[3].lower()
    tipo_negocio = weblink.split("/")[4].lower()
    fecha = now.year * 10000 + now.month * 100 + now.day
    file_name = (
        "fincaraiz-{}-{}_{}-{}.csv"
        .format(ubicacion, tipo_inmueble, tipo_negocio, fecha)
    )

    # desahilitar advertencias
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    ### ejecucion

    ## parte 1 extraer urls de las paginas

    # crear loop que vaya por cada pagina solicitada
    while number_page <= max_number_page:
        number_page += 1

        # hacer el request
        r = requests.get(weblink, verify=False)
        content = r.content
        soup = BeautifulSoup(content, "html.parser")


        # encontrar pagina siguiente
        weblink = soup.find("link", {"rel":"next"})["href"]    

        # encontrar bloques de ventas
        divAdverts = soup.find("div", {"id":"divAdverts"})

        # encontrar cada bloque de venta
        ul = divAdverts.find_all("ul")

        # extraer las urls de cada bloque
        for u in ul:
            ads = u.find("div", {"class":"AdvertisingContainer"})

            # si es un anuncio se omite
            if ads is not None:
                continue
            
            # extraer las url
            try:
                url = u.find_all("a", href=True)
                full_url = "https://www.fincaraiz.com.co" + str(url[0]['href'])

            except:
                full_url = None
            
            # adicionar al listado de urls
            full_url = full_url if full_url.count("http") <= 1 else None
            urls.append(full_url)

    ## parte 2 extraer informacion de las urls
    
    # limpiar urls nulas 
    urls = [url for url in urls if url is not None]

    # request por cada url
    for i, url in enumerate(urls):

        # mostrar avance
        texto = (
            "\rProcesado: " + str(i+1) + "/" + str(len(urls)) + " " + 
            str(round(100*(i+1)/len(urls), 2)) + "%"
        )
        if i + 1 == len(urls):
            texto += "\r"
        print(texto, end="")    
        time.sleep(0.5)
        
        # hacer el request
        inm_r = requests.get(url, verify=False)
        inm_content = inm_r.content
        inm_soup = BeautifulSoup(inm_content, "html.parser")    

        # encontrar json con informacion
        scripts = inm_soup.find_all("script", {"type":"text/javascript"})
        texto = []

        # si el request falla
        if scripts == []:
            continue

        # extraer el json
        for s in scripts:
            texto = re.findall("var sfAdvert = {(.*)}", s.text)
            if texto != []:
                break
        
        # si no encuentra informacion del inmueble
        if texto == []:
            continue

        # convertir el json en un diccionario
        nuevo_texto = texto[0].split("\", ")
        nuevo_texto2 = [t.replace("\"","").split(" : ") for t in nuevo_texto]
        dicc = diccionario(nuevo_texto2)

        # adicionar a la lista de diccionarios
        lista_dicc.append(dicc)

    ## parte 3 creacion del dataframe

    # convertir cada diccionario en una lista de dataframe
    lista_df = [pd.DataFrame(dic, index=[0]) for dic in lista_dicc]

    # concatenar dataframe
    df = pd.concat(lista_df).reset_index(drop=True)

    # crear columnas faltantes
    df["extraction_year"] = now.year
    df["extraction_month"] = now.month
    df["extraction_day"] = now.day

    # eliminar duplicados
    df.drop_duplicates(inplace=True)

    # tiempo
    print("Se demoró (HH:MM:SS): ", dt.datetime.now()-now)

    # guardar dataframe
    df.to_csv(data_path + file_name, index=False)
    return df

