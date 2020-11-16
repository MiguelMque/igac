# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pickle
import os
import pandas as pd
import unicodedata
import numpy as np
import optuna.integration.lightgbm as lgb


def merge_two_dicts(x, y):
    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return z

def normalize(text):
    return unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode("utf-8").lower()

def preprocess(data):
    """
    Function that process the input data to have the format than train data

    Parameters
    ----------
    data : Dictionary
        Dictionary with input features for the model.

    Returns
    -------
    data : Dictionary
        Dictionary with the same format than train data.

    """
    
    tipos = ["tipo_Apartaestudio",   
    "tipo_Apartamento",        
    "tipo_Bodega",              
    "tipo_Casa",               
    "tipo_Consultorio",      
    "tipo_Edificio",      
    "tipo_Finca",               
    "tipo_Habitacion",          
    "tipo_Local",              
    "tipo_Lote",                
    "tipo_Oficina",             
    "tipo_Otro",               
    "tipo_Proyecto"]
    
    for t in tipos:
        if data["tipo"] in t:
            data[t] = 1
        
        if data.get(t, 0) == 0:
            data[t] = 0
            
    data.pop("municipio")
    data.pop("tipo")
    
    data = pd.DataFrame(data, index=[0])
    obj_feat = list(data.loc[:, data.dtypes == 'object'].columns.values)
    for feature in obj_feat:
        data[feature] = pd.Series(data[feature], dtype="category")
        
    return data

def get_models(muni, files):
    """
    Function that load the save models to predict values

    Parameters
    ----------
    muni : String
        Name of municipality of interest.
    files : .sav
        Files with model saved.

    Returns
    -------
    models : Model
        Loaded models.

    """
    models = []
    
    for f in files:
        if muni in f and f.endswith(".sav"):
            print(f)
            loaded_model = pickle.load(open(f, 'rb'))
            models.append(loaded_model)
            
    return models


from math import radians, cos, sin, asin, sqrt
def haversine(x, lon2, lat2):
    """
    Function that calculates distance between two points

    Parameters
    ----------
    x : Tuple
        Point 1 with latitude and longitude.
    lon2 : Float
        Point 2 longitude.
    lat2 : Float
        Point 2 latitude.

    Returns
    -------
    km : Float
        Distance in km between point 1 and 2.

    """
    lat1 = x.lat
    lon1 = x.lon
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    # Radius of earth in kilometers is 6371
    km = 6371* c
    return km


def minimum(df, lon, lat):
    """
    Function that get the distance between the address of the house we
    want to calculate the appraisal and all houses in our train data
    to keep the variables from here api of the house with minimum distance

    Parameters
    ----------
    df : DataFrame
        DataFrame with information from web sources like finca raiz 
        and properti.
    lon : Float
        Longitude of the address we want to calculate the appraisal
    lat : Float
        Latitude of the address we want to calculate the appraisal

    Returns
    -------
    Dictionary
        Dictionary with here api of the closest house of the interest one.

    """

    df["km"] = df.apply(haversine, args=(lon, lat), axis=1)
    
    #print(min(df["km"]))
    
    return df[df["km"]==df["km"].min()][['health',
       'hospital', 'cafe', 'restaurant', 'bar', 'club', 'entertainment',
       'park', 'museum', 'zoo', 'church', 'hotel', 'education', 'university',
       'school', 'shopping mall', 'shop', 'supermarket', 'transport', 'police']].to_dict(orient="records")[0]

def predict_price(df, features):
    """
    Function that preprocess the input data to calculate the appraisal

    Parameters
    ----------
    df : DataFrame
        DataFrame with information from web sources like finca raiz 
        and properti..
    features : Dictionary
        Dictionary with input features for the model..

    Returns
    -------
    Float
        Calculated price of the house.

    """
    
    features = merge_two_dicts(minimum(df, features["lon"], features["lat"]), features)
    
    results = [each for each in os.listdir(os.getcwd()) if each.endswith(".sav")]
    models = get_models(normalize(features["municipio"]), results)
    features = preprocess(features)
    features = pd.get_dummies(features)
    price = [m.predict(features) for m in models]
    
    return int(np.mean(price))