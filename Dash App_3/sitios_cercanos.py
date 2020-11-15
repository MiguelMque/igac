# -*- coding: utf-8 -*-
"""
Created on Sat Nov 14 21:46:50 2020

@author: 28dan
"""

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

def minimum(df,lon, lat):

    df["km"] = df.apply(haversine, args=(lon, lat), axis=1)
    
    #print(min(df["km"]))
    
    return df[df["km"]==df["km"].min()][['health',
       'hospital', 'cafe', 'restaurant', 'bar', 'club', 'entertainment',
       'park', 'museum', 'zoo', 'church', 'hotel', 'education', 'university',
       'school', 'shopping mall', 'shop', 'supermarket', 'transport', 'police']].to_dict(orient="records")[0]