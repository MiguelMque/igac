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
from appraisal_app import Appraisal_calculator
 
teammember = dash.Dash(__name__)

nav = html.Div(id       = "app-page-header",
               style    = {'width' : "100%"},
               children = [html.Div([dbc.Row([html.H1("Team members",style={'text-align': 'center','margin-left':'50px','color':'black'}) ]), 
                                     dbc.Row([dbc.Col([dbc.Button(
                            "Back",
                            id="back-button", color="primary",#outline=True,
                            style={'text-align':'center', 'margin-left': '850px'}, href= '/'
                            
                        )], width=9)])
                                     
                                     
                                     ])])
  


integrantes =html.Div(children=[html.Br(),
                          dbc.Container(id='container'),
                          html.Br(),
                          dbc.Row(([html.Img(src="/assets/users.jpg", style={'width':'100px'}), html.Label("Team member description", style={'margin-left':'50px'})])),
                          dbc.Row([dbc.Col([html.P("Member1",style={'font-weight': 'bold'})],width=3)],
                                                 no_gutters=True),
                                         html.Br(),
                         html.Br(),
                          dbc.Row(([html.Img(src="/assets/users.jpg", style={'width':'100px'}), html.Label("Team member description", style={'margin-left':'50px'})])),
                          dbc.Row([dbc.Col([html.P("Member2",style={'font-weight': 'bold'})],width=3)],
                                                 no_gutters=True),
                                         html.Br(),
                        
                          html.Br(),
                          dbc.Row(([html.Img(src="/assets/users.jpg", style={'width':'100px'}), html.Label("Team member description", style={'margin-left':'50px'})])),
                          dbc.Row([dbc.Col([html.P("Member3",style={'font-weight': 'bold'})],width=3)],
                                                 no_gutters=True),
                                         html.Br(),
                                         
                        html.Br(),
                          dbc.Row(([html.Img(src="/assets/users.jpg", style={'width':'100px'}), html.Label("Team member description", style={'margin-left':'50px'})])),
                          dbc.Row([dbc.Col([html.P("Member4",style={'font-weight': 'bold'})],width=3)],
                                                 no_gutters=True),
                                         html.Br(),
                        html.Br(),
                          dbc.Row(([html.Img(src="/assets/users.jpg", style={'width':'100px'}), html.Label("Team member description", style={'margin-left':'50px'})])),
                          dbc.Row([dbc.Col([html.P("Member5",style={'font-weight': 'bold'})],width=3)],
                                                 no_gutters=True),
                                         html.Br(),
                        html.Br(),
                          dbc.Row(([html.Img(src="/assets/users.jpg", style={'width':'100px'}), html.Label("Team member description", style={'margin-left':'50px'})])),
                          dbc.Row([dbc.Col([html.P("Member6",style={'font-weight': 'bold'})],width=3)],
                                                 no_gutters=True),
                                         html.Br(),
                    
                        html.Br(),
                          dbc.Row(([html.Img(src="/assets/users.jpg", style={'width':'100px'}), html.Label("Team member description", style={'margin-left':'50px'})])),
                          dbc.Row([dbc.Col([html.P("Member7",style={'font-weight': 'bold'})],width=3)],
                                                 no_gutters=True),
                                         html.Br(),
                            ])

Team_layout = html.Div([html.Br(),html.Br(),dbc.Row([dbc.Col(nav)]),
                         html.Br(),
                        
                                  dbc.Col(dbc.Card(dbc.CardBody([integrantes],style={"height": "80rem"})),
                                          width={"size": 9},
                                          style={"margin-left": "40px"})])


def Team_members():
    layout = html.Div(children=[Team_layout])
    return layout