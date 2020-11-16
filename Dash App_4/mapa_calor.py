# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 21:23:38 2020

@author: 28dan
"""

from folium import plugins
from folium.plugins import HeatMap
import pandas as pd
import folium
import branca


def color_map(municipio,latitud,longitud,df):
    """
    Funtion that build heatmap with houses price.

    Parameters
    ----------
    municipio : String
        Name of municipality of interest.
    latitud : Float
        Reference latitude to center the graph
    longitud : Float
        Reference longitude to center the graph
    df : DataFrame
        DataFrame with information from web sources like finca raiz 
        and properti..

    Returns
    -------
    map_hooray : Folium map
        Heatmap with color that describe the values of houses.

    """
    data3=df
    
    map_hooray = folium.Map(
        location=[latitud, longitud],
        #tiles = "Stamen Terrain"
        zoom_start = 13
      ) 
    
    # Ensure you're handing it float
    
    # Filter the DF for rows, then columns, then remove NaNs
    heat_df = data3[data3["municipio"]==municipio][["lat", "lon", "valor2"]]
    heat_df["valor2"]=heat_df["valor2"].astype(int)
    # List comprehension to make out list of lists
    heat_data = [[row['lat'],row['lon'], row['valor2']] for index, row in heat_df.iterrows()]
    
    # Plot it on the map
    HeatMap(
        heat_data, 
        radius=10, 
        blur=20, 
    ).add_to(map_hooray)
    # Display the map
    colormap = branca.colormap.LinearColormap(
    ['blue', 'green', 'yellow', 'red'],
    vmin=0, vmax=max(heat_df["valor2"].astype(int)),
    caption='step'
    )
    colormap.caption = 'Properties values in millions and three decimals'
    colormap.add_to(map_hooray)
    return map_hooray