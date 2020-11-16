# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 20:56:03 2020

@author: 28dan
"""

# Libraries
import matplotlib.pyplot as plt
import pandas as pd
from math import pi
 
# Set data

def grafico_lugares(df,municipality):
    """
    

    Parameters
    ----------
    df : DataFrame
        DataFrame with information from web sources like finca raiz 
        and properti.
    municipality : String
        Name of municipality of interest.

    Returns
    -------
    categories : List
        Categories to show in radar chart
    values : List
        Values to plot radar chart

    """
    radar_df_prev = (
        df[[
            "municipio","restaurant","entertainment","shop","education" 
        ]]
        .groupby("municipio", as_index=False)
        .mean()
    ) 
    radar_df_num=radar_df_prev[["restaurant","entertainment","shop","education" ]]*5
    radar_df=radar_df_num
    radar_df["municipio"]=radar_df_prev["municipio"]

     
    # number of variable
    categories=list(radar_df)[0:4]
    
    # Values of proportion
    values=radar_df[radar_df["municipio"]==municipality].values.flatten().tolist()[0:4]
    return categories, values