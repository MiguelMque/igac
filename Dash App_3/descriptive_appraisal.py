# -*- coding: utf-8 -*-
"""
Created on Sat Nov  7 12:19:45 2020

@author: 28dan
"""

import numpy as np
import pandas as pd
from skimage import io, data, transform
from time import sleep

import dash
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import dash_table
import dash_bootstrap_components as dbc

def instructions():
    return html.P(
        children=[
            """
    Here you will find the descriptive data for the municipality that you have chosen.
    -If you want to calculate the appraisal select "appraisal calculator"
    -You have two options to calculate the appraisal, this can be individual or massive
    -To calculate the individual appraisal enter the variables of the property and click the button "calculate"
    -To calculate the massive appraisal, load the file with the information of the different properties and click on the calculate button
    -Each municipality has a different prediction model, you can change the municipality from the dropdown here below
    """
        ],
        className="instructions-sidebar",
    )

TAB_single =html.Div(children=[html.Br(),
                          html.Br(),
                          dbc.Row([dbc.Col([html.P("Number of rooms",style={'font-weight': 'bold'})],width=3),
                                                  dbc.Col([dbc.Input(id="var1", 
                                                                     type='number',
                                                                     value=1,
                                                                     min=1,
                                                                     max=20,
                                                                     step=1)],width=9)],
                                                 no_gutters=True),
                                         html.Br(),
                         dbc.Row([dbc.Col(html.P("Number of bathrooms",style={'font-weight': 'bold'}),width=3),
                                                  dbc.Col(dbc.Input(id="var2", 
                                                                    type='number',
                                                                    value=1,
                                                                    min=1,
                                                                    max=20,
                                                                    step=1),width=9)],
                                 no_gutters=True),
                         html.Br(),
                         dbc.Row([dbc.Col(html.P("Area in square meters",style={'font-weight': 'bold'}),width=3),
                                                  dbc.Col(dbc.Input(id="var3", 
                                                                    type='number',
                                                                    value=1,
                                                                    min=1),width=9)],
                                                 no_gutters=True),
                             html.Br(),
                             dbc.Row([dbc.Col(html.P("Property type",style={'font-weight': 'bold'}),width=3),
                                                  dbc.Col(dcc.Dropdown(id="var5", 
                                                                    options= [{'label': k, 'value': k} for k in ['Apartamento','Casa']], 
                                                                    clearable=False,
                                                                    value="Apartamento",
                                                                    style={'font-size': "115%", "width":"70%",'margin-left':'5%'}),width=9)],
                                                                             no_gutters=True),
                             html.Br(),
                        dbc.Row([dbc.Col(html.P("Address",style={'font-weight': 'bold'}),width=3),
                                                  dbc.Col(dbc.Input(id="var4", 
                                                                    type='text',
                                                                    placeholder="Address"),width=9)],
                                                 no_gutters=True),
                             html.Br(),
                            dbc.Row([dbc.Col(dbc.Button("Calculate",
                            id="appraisal-calculator-button",color='info',style={'margin-left':'220px'})),
                                     dbc.Col(html.H3(id="individual_value"))])
                            ])

TAB_bulk =html.Div(children=[html.Br(),
                          dbc.Container(id='container2'),
                          html.Br(),
                          dbc.Row([dbc.Col(dcc.Upload(
                            id='upload-data',
                            children=html.Div([
                                'Drag and Drop or ',
                                html.A('Select Files')
                            ]),
                            style={
                                'width': '100%',
                                'height': '60px',
                                'lineHeight': '60px',
                                'borderWidth': '1px',
                                'borderStyle': 'dashed',
                                'borderRadius': '5px',
                                'textAlign': 'center',
                                'margin': '10px'
                            }))]),
                          html.Br(),
                                html.P(id='text-data-upload'),
                                html.Div(id='output-data-upload'),
                            ])

TAB_descriptive =html.Div(children=[html.Br(),
                          dbc.Container(id='container3'),
                            ])

layout_da = html.Div(
    children=[
        html.Div(
            [
                html.Br(),html.Br(),html.Br(),
                html.H1(children="AVALPredict app"),
                instructions(),
                
                html.Div(
                    html.Div(id="demo-explanation", children=[])
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Label("Choose a municipality"),
                                dcc.Dropdown(
                                        id='drop_municipality2', 
                                        options= [{'label': k, 'value': k} for k in ['Manizales','Fusagasugá','Villavicencio']], 
                                        clearable=False,
                                        value="Manizales",
                                        style={'font-size': "115%", "width":"85%",'margin-left':'5%'}
                                        ),
                            ]
                        ),
                    ],
                    className="mobile_forms",
                ),
                html.Br(),
            ],
            className="four columns instruction",
        ),
        html.Div(
            [
                dcc.Tabs(
                    id="stitching-tabs",
                    children=[
                        dcc.Tab(TAB_descriptive,label="DESCRIPTIVE"),
                        dcc.Tab(TAB_single,label="INDIVIDUAL CALCULATOR"),
                        dcc.Tab(TAB_bulk,label="BULK CALCULATOR"),
                    ],
                    className="tabs",
                ),
            ],
            className="eight columns result",
        ),
    ],
    className="row twelve columns",
)

def Descriptivos():
    layout =layout_da
    return layout 
