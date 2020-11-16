# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 19:58:19 2020

@author: laurgrhe
"""

import pandas as pd

import numpy as np
import pandas as pd
from skimage import io, data, transform
from time import sleep
from datetime import datetime,timedelta

import dash
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go


descriptivos = dash.Dash(__name__)

###############################################
#Layout of descriptive tab

def layout_descriptivos(fig1,fig2,fig3,texto1,texto2):
    
    charts = html.Div(style = {"display":'flex'}, children=[html.Br(),
                            dcc.Graph(id = 'grafico1', figure=fig1,  style={"height" : "200px", "width" : "50%"}),
                              html.Br(),
                              
                              dcc.Graph(id = 'grafico2', figure=fig2,  style={"height" : "200px", "width" : "50%", "margin-top": '1px'}),
                              html.Br(),
    
                                             ])

    
    
    layout_descriptivos = html.Div([charts])
    
    
    
    #layout_graph = html.Div(dcc.Graph(id = 'municipality_map', figure=fig3,  style={"height" : "20%", "width" : "100%"}))
    layout_graph=html.Div(fig3,  style={"height" : "100px", "width" : "100%"})#dcc.Graph(id = 'municipality_map', figure=fig3,  style={"height" : "20%", "width" : "100%"}))
    
    
    message = html.Div(children=[html.H5("About Municipality choosen",style={'color':'black','font':'Verdana'}),html.H6(texto1),html.H6(texto2,style={"white-space": "pre"})])

    layout_info =html.Div(children = [dbc.Card(dbc.CardBody([message],style={"height": "60rem",'box-shadow': '0 4px 8px 0 rgba(0,0,0,0.2)','color':'success'}))])

    
    
    Descriptivos_layout = html.Div(
                                  children = [html.Div([
                                          dbc.Card(dbc.CardBody(children = [layout_descriptivos,layout_graph],style={"height": "60rem"})),
                                        
                                 ],className="eight columns result"),
                                      html.Div([
                                          layout_info
                            
                                 ],className="four columns result")
                                      ],style={"margin-top":"0"})
                                      
                                      
    return Descriptivos_layout



def Descriptivos_layout(fig1,fig2,fig3,texto1,texto2):
    layout =layout_descriptivos(fig1,fig2,fig3,texto1,texto2)
    return layout 