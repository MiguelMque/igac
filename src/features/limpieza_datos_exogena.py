# -*- coding: utf-8 -*-

# import modules
import numpy as np
import pandas as pd
import glob

def concat_data_exogena(data_path, municipios_prop=[], limpiar=True, dumm=True):
    """
    Concatena la información exógena de fincaraiz y properati
    
    Se cargarán todos los archivos de fincaraiz que estén en el data_path
    Si no especifica municipios a limpiar properati se filtrarán:
        Fusagasugá, Villavicencio y Manizales por defecto.
    limpiar=True si desea limpiar datos nulos y outlieres
    dumm=True si desea generar las variables dummies
    """

    if municipios_prop == []:
        municipios_prop = ["villavicencio", "fusagasuga", "manizales"]

    if not isinstance(data_path, str):
        raise TypeError("Error, data_path debe ser de tipo string")
    if not isinstance(municipios_prop, list):
        raise TypeError("Error, municipios_prop debe ser de tipo list")
    if not isinstance(limpiar, bool):
        raise TypeError("Error, limpiar debe ser de tipo bool")
    if not isinstance(dumm, bool):
        raise TypeError("Error, dumm debe ser de tipo bool")

    data_path += "\\"
    
    ### lectura y unificacion archivos

    ## fincaraiz

    # leer archivos vivienda (v) y comerciales (v)
    fr_files = glob.glob(data_path + "fincaraiz*")
    fr_v_dfs = [pd.read_csv(fr) for fr in fr_files if fr.count("vivienda")>0]
    fr_c_dfs = [pd.read_csv(fr) for fr in fr_files if fr.count("vivienda")==0]
    fincaraiz_v = pd.concat(fr_v_dfs)
    fincaraiz_c = pd.concat(fr_c_dfs)

    # filtrar y unificar
    fr_vars = [
        "Location1", "Location2", "Neighborhood", "Category1", "Title",
        "Description", "Price", "Area", "Rooms", "Baths", "Latitude", 
        "Longitude"
    ]
    fincaraiz2 = pd.concat([fincaraiz_v[fr_vars], fincaraiz_c[fr_vars]])

    # organizar
    fincaraiz2.columns = [
        "fr_departamento", "fr_municipio", "fr_barrio", "fr_tipo", "fr_titulo",
        "fr_descripcion", "fr_valor", "fr_area", "fr_habitaciones", 
        "fr_banios", "fr_lat", "fr_lon"
    ]

    fincaraiz2["fr_dataset"] = "fincaraiz"

    ## properati

    # lectura
    properati = pd.read_csv(data_path + "co_properties.csv")

    # filtrar y unificar
    properati["property_type"] = (
        properati.property_type
        .replace("Local comercial", "Local").replace("Depósito", "Bodega")
    )

    pr_vars = [
        "l2", "l3", "l5", "property_type", "title", "description", "price", 
        "surface_total", "bedrooms", "bathrooms", "lat", "lon"
    ]

    properati2 = (
        properati[
            (
                properati["l3"]
                .str.lower()
                .str.replace("á","a")
                .str.replace("é","e")
                .str.replace("í","i")
                .str.replace("ó","o")
                .str.replace("ú","u")
                .isin(municipios_prop)
            ) &
            (properati["operation_type"]=="Venta")
        ][pr_vars]
    )    

    # organizar
    properati2.columns = [
        "pr_departamento", "pr_municipio", "pr_barrio", "pr_tipo", "pr_titulo", 
        "pr_descripcion", "pr_valor", "pr_area", "pr_habitaciones", 
        "pr_banios", "pr_lat", "pr_lon"
    ]

    properati2["pr_dataset"] = "properati"

    ## concatenar datasets
    # cambiar nombre columnas
    fincaraiz2.columns = [col[3:] for col in fincaraiz2.columns]
    properati2.columns = [col[3:] for col in properati2.columns]

    # concatenar
    data_for_model = pd.concat([fincaraiz2, properati2])

    ### limpieza archivos

    # retornar datos si no se necesitan limpiar
    if not limpiar:
        data_for_model.to_csv(data_path + "data_for_model.csv", index=False)
        return data_for_model
    
    ## limpieza
    
    # lat lon fuera del pais, valores y areas nulas
    dfm2 = data_for_model[
        (~data_for_model["valor"].isna()) & 
        ((data_for_model["lat"] <= 12) & (data_for_model["lat"] >= -2)) &
        ((data_for_model["lon"] <= -65) & (data_for_model["lon"] >= -80)) &
        (~data_for_model["area"].isna())
    ]

    # outliers habitaciones y banios
    dfm3 = dfm2[
        (dfm2["habitaciones"]<=250) & 
        (dfm2["banios"]<=250) & 
        (dfm2["area"]<10000000)
    ]

    ## dummies
    
    # si no quiere dummies
    if not dumm:
        dfm3.to_csv(data_path + "data_for_model_clean.csv", index=False)
        return dfm3
    
    # reemplazar municipio
    dfm3["municipio"].fillna("NA", inplace=True)

    # crear dummies departamento, municipio y tipo
    depts_dum = pd.get_dummies(
        dfm3["departamento"]
        .str.lower()
        .str.replace("á","a")
        .str.replace("é","e")
        .str.replace("í","i")
        .str.replace("ó","o")
        .str.replace("ú","u")
        .str.capitalize()
    )
    muns_dum = pd.get_dummies(
        dfm3["municipio"]
        .str.lower()
        .str.replace("á","a")
        .str.replace("é","e")
        .str.replace("í","i")
        .str.replace("ó","o")
        .str.replace("ú","u")
        .str.replace(" d.c","")
        .str.capitalize()
    )

    types_dum = pd.get_dummies(
        dfm3["tipo"]
        .str.lower()
        .str.replace("á","a")
        .str.replace("é","e")
        .str.replace("í","i")
        .str.replace("ó","o")
        .str.replace("ú","u")
        .str.capitalize()
    )

    dfm4 = pd.concat(
        [
            depts_dum, muns_dum, types_dum, 
            dfm3.drop(columns=["departamento", "municipio", "tipo"])
        ],
        axis=1
    )

    dfm4.to_csv(data_path + "data_for_model_clean_dummies.csv", index=False)
    return dfm4
