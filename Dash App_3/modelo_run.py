# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 21:59:34 2020

@author: Miguel
"""

import os
from joblib import dump, load
import pandas as pd
import numpy as np
import unicodedata
import optuna.integration.lightgbm as lgb

def normalize(text):
    return unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode("utf-8").lower()

def preprocess(data):
    
    data = pd.DataFrame(data, index=[0])
    obj_feat = list(data.loc[:, data.dtypes == 'object'].columns.values)
    for feature in obj_feat:
        data[feature] = pd.Series(data[feature], dtype="category")
        
    return data

def get_models(muni, files):
    models = []
    
    for f in files:
        if muni in f:
            models.append(load(f))
            
    return models

def predict_price(features):
    
    results = [each for each in os.listdir(os.getcwd()) if each.endswith(".sav")]
    models = get_models(normalize(features["municipio"]), results)
    del features["municipio"]
    features = preprocess(features)
    price = np.mean([m.predict(features) for m in models])
    
    return np.exp(price)