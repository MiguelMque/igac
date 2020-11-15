# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 21:19:05 2020
@author: 28dan
"""
import numpy as np
import pandas as pd
import datetime

import dash
import dash_table
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go
from appraisal_app import Appraisal_calculator
from teammembers import Team_members
from descriptivos import Descriptivos_layout
from descriptive_appraisal import Descriptivos
from mapa_calor import color_map
from grafico_lugares import grafico_lugares
from coordenadas import get_coordenadas
from model import predict_price
from read_bulk import parse_contents
from sqlalchemy import create_engine

engine2=create_engine('postgresql://topscorer:topscorer@67.205.164.197:5432/db_resultados');
def build_radar(df,municipality):
    categories,values=grafico_lugares(df,municipality)
    return go.Figure(data=go.Scatterpolar(
                      r=values,
                      theta=categories,
                      fill='toself'
                    )).update_layout(
                  polar=dict(
                    radialaxis=dict(
                      visible=True
                    ),
                  ),
                  showlegend=False,
                  title="Services in the municipality",
                  margin=dict(l=15,r=15,b=30,t=30,pad=4),
                  font=dict(
                    family="Verdana",
                    size=11,
                    color="Black"
                )
                )
                        
def histogram_prices(df,municipality,end=600):
    series=df[df["municipio"]==municipality]["valor2"]
    start = int(series.min())
    size = 50

    # Making a histogram
    largest_value = series.max()
    if largest_value > end:
        hist = np.histogram(series, bins=list(range(start, end+size, size)) + [largest_value])
    else:
        hist = np.histogram(series, bins=list(range(start, end+size, size)) + [end+size])

    # Adding labels to the chart
    labels = []
    for i, j in zip(hist[1][0::1], hist[1][1::1]):
        if j <= end:
            labels.append('{} - {}'.format(int(i), int(j)))
        else:
            labels.append('> {}'.format(int(i)))

    # Plotting the graph
    datos = [go.Bar(x=labels,
                   y=hist[0])]
    return go.Figure(data=datos).update_layout(
                  showlegend=False,
                  title="Appraisal distribution",
                  margin=dict(l=10,r=10,b=10,t=30,pad=4),
                  font=dict(
                    family="Verdana",
                    size=11,
                    color="Black"
                ),xaxis_title="Prices in millions"
                )
                        
                        
#df = pd.read_csv("C:/Users/28dan/Desktop/Mayra/DS4A/Dash App/app/data_for_model_clean_places.csv")
df=pd.read_sql('data_for_model_clean_places',engine2)
df["valor2"]=df["valor"]/1000000
    

from flask import Flask                                                             ####-----
server = Flask(__name__) 
app = dash.Dash(
    __name__,server=server
)
app.config.suppress_callback_exceptions = True
body = html.Div(style={
'background-image': 'url("/assets/background5.png")',
'background-repeat': 'no-repeat',
'background-position': 'center top',
},children = [html.Br(),
html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),
html.Br(),
html.Br(),
dbc.Row([html.H2("In this app you will find descriptive analysis and an appraissal calculator",    
                                       style={'margin-left':'300px','color':'black'})]),
html.Br(),
dbc.Row([
    dbc.Button(
                            "PREDICT AND DESCRIBE",
                            id="go_button", className="button_instruction",style={'text-align':'center', 'margin-left': '620px'},#, color="info",
                            href='appraisal&descriptive' #,outline=True
                        )
    ]),
html.Br(),
html.Br(),
html.Br(),
html.Br(),
html.Br(),
html.Br(),
html.Br(),
html.Br(),
html.Br(),
html.Br(),
html.Br()
])
              
              
index = html.Div(id ='page-content',children=body)
app.layout = html.Div([dcc.Location(id = 'url', refresh = True),index])


        
@app.callback(dash.dependencies.Output('page-content', 'children'),
               [dash.dependencies.Input('url', 'pathname')])
 
def display_page(pathname):
     if pathname == '/teammembers' :
         return Team_members()
     elif pathname == '/appraisal' :
         return Appraisal_calculator()
     elif pathname == '/appraisal&descriptive' :
         return Descriptivos()
     else: 
         return index
     
# #=== sp_dropdown_cliente
@app.callback(
     [dash.dependencies.Output('container3', 'children')],
     [dash.dependencies.Input('drop_municipality2', 'value')])
def show_heatmap(municipality):
    lista_coordenadas=[["Villavicencio",4.15, -73.633],
                   ["Fusagasugá",4.333, -74.35],
                   ["Manizales",5.067,-75.517]]
    texto_municipios1=[["Villavicencio",
                       """Villavicencio is a Colombian municipality, capital of the Meta department and the most important commercial center of the Llanos Orientales.
                       """],
                   ["Fusagasugá","""Fusagasugá is a Colombian municipality, located in the department of Cundinamarca. It is the third most populated municipality in the department after Bogotá and Soacha.
                    """],
                   ["Manizales","""Manizales is a Colombian municipality, capital of the department of Caldas. It is located in the western center of Colombia.
                    """]]
    texto_municipios2=[["Villavicencio",
                       """-Population: 551,212 \n-Weather: 29 ° C \n-Humidity 62% \n-Area: 1,338 km²
                       """],
                   ["Fusagasugá","""-Population: 139,805 \n-Weather: 18 ° C \n-Humidity 74 \n-Area: 239 km²"""],
                   ["Manizales","""-Population: 434,403 \n-Weather: 23 ° C \n-Humidity 72% \n-Area: 571.8 km²"""]]
    df_coordenadas=pd.DataFrame(lista_coordenadas,columns=["Municipio","Latitud","Longitud"])
    df_texto1=pd.DataFrame(texto_municipios1,columns=["Municipio","Descripcion"])
    df_texto2=pd.DataFrame(texto_municipios2,columns=["Municipio","Descripcion"])
    mostrar=df_coordenadas[df_coordenadas["Municipio"]==municipality]
    mostrar2=df_texto1[df_texto1["Municipio"]==municipality]
    mostrar3=df_texto2[df_texto2["Municipio"]==municipality]
    mapa=color_map(list(mostrar["Municipio"])[0],list(mostrar["Latitud"])[0],list(mostrar["Longitud"])[0],df)
    mapa.save('mapa.html')
    visual_map = html.Iframe(id="map",srcDoc=open('mapa.html','r').read(),width='100%',height='250')
    radar=build_radar(df,municipality)
    histograma=histogram_prices(df,municipality)
    retorno=Descriptivos_layout(histograma,radar,visual_map,list(mostrar2["Descripcion"])[0],list(mostrar3["Descripcion"])[0])
    return [retorno]

@app.callback(
      [dash.dependencies.Output('individual_value', 'children')],
      [dash.dependencies.Input('var1', 'value'),
       dash.dependencies.Input('var2', 'value'),
       dash.dependencies.Input('var3', 'value'),
       dash.dependencies.Input('var4', 'value'),
       dash.dependencies.Input('var5', 'value'),
       dash.dependencies.Input('drop_municipality2', 'value'),
       dash.dependencies.Input('appraisal-calculator-button','n_clicks')])
def individual_appraisal(rooms,baths,area,address,tipo,municipality,n_clicks):
    lista_coordenadas=[["Villavicencio","Meta"],
                    ["Fusagasugá","Cundinamarca"],
                    ["Manizales","Caldas"]]
    df_coordenadas=pd.DataFrame(lista_coordenadas,columns=["Municipio","Departamento"])
    mostrar=df_coordenadas[df_coordenadas["Municipio"]==municipality]
    if n_clicks is None:
         return [""]
    else:
        try:
            lat,lon=get_coordenadas(address,municipality,list(mostrar["Departamento"])[0])
            print(lat)
        except:
            return ["Address not found"]
        else:
            dict_var={"habitaciones":rooms,
                      "banios":baths,
                      "area":area,
                      "tipo":tipo,
                      "lat":lat,
                      "lon":lon,
                      "municipio":municipality
                      }
            aval=predict_price(df,dict_var)
            return ["Calculated appraisal is "+str("{:,}".format(aval))+" COP"]
    

@app.callback([dash.dependencies.Output('text-data-upload', 'children'),
               dash.dependencies.Output('output-data-upload', 'children')],
              [dash.dependencies.Input('upload-data', 'contents')],
              [dash.dependencies.State('upload-data', 'filename'),
               dash.dependencies.State('upload-data', 'last_modified')])
def bulk_appraisal(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = parse_contents(list_of_contents, list_of_names, list_of_dates)
        try:
            rooms=children["Rooms"]
            baths=children["Baths"]
            area=children["Area"]
            tipo=children["Type"]
            address=tipo=children["Address"]
            municipality=children["Municipality"]
            department = children["Department"]
        except:
            print_children=html.Div([
            html.H5(list_of_names),
            html.H6(datetime.datetime.fromtimestamp(list_of_dates)),
    
            dash_table.DataTable(
                data=children.to_dict('records'),
                columns=[{'name': i, 'id': i} for i in children.columns]
            ),
    
            html.Hr(),  # horizontal line
    
        ])
            return ["Any column is misspelled or is missing. Column names should be: Rooms, Area, Baths, Type, Address, Municipality and Department", print_children]
        result=[]
        for i in range(len(rooms)):
            try:
                lat,lon=get_coordenadas(address[i],municipality[i],department[i])
            except:
                result.append("Address not found")
            else:
                dict_var={"habitaciones":rooms[i],
                      "banios":baths[i],
                      "area":area[i],
                      "tipo":tipo[i],
                      "lat":lat,
                      "lon":lon,
                      "municipio":municipality[i]
                      }
                aval=predict_price(df,dict_var)
                result.append(str(int(aval)))
        children["Result"]=np.array(result)
        return ["", html.Div([
        html.P("Upload file name: "+list_of_names),

        dash_table.DataTable(
            data=children.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in children.columns]
        ),

        html.Hr(),  # horizontal line
        
            ])]
    else:
        return ["Upload a file",None]

      
if __name__ == '__main__':
    #app.run_server(port = 5000,debug=True)
    app.run_server(host="0.0.0.0", port="8050",debug=False)