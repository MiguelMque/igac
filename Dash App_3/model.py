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
    models = []
    
    for f in files:
        if muni in f and f.endswith(".sav"):
            print(f)
            loaded_model = pickle.load(open(f, 'rb'))
            models.append(loaded_model)
            
    return models


from math import radians, cos, sin, asin, sqrt
def haversine(x, lon2, lat2):
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

    df["km"] = df.apply(haversine, args=(lon, lat), axis=1)
    
    #print(min(df["km"]))
    
    return df[df["km"]==df["km"].min()][['health',
       'hospital', 'cafe', 'restaurant', 'bar', 'club', 'entertainment',
       'park', 'museum', 'zoo', 'church', 'hotel', 'education', 'university',
       'school', 'shopping mall', 'shop', 'supermarket', 'transport', 'police']].to_dict(orient="records")[0]

def predict_price(df, features):
    
    features = merge_two_dicts(minimum(df, features["lon"], features["lat"]), features)
    
    results = [each for each in os.listdir(os.getcwd()) if each.endswith(".sav")]
    models = get_models(normalize(features["municipio"]), results)
    features = preprocess(features)
    features = pd.get_dummies(features)
    price = [m.predict(features) for m in models]
    
    return int(np.mean(price))