# -*- coding: utf-8 -*-
"""
Created on Sat Oct 24 14:52:14 2020
@author: 28dan
"""

import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

nav = html.Div(id       = "app-page-header",
               style    = {'width' : "100%"},
               children = [html.Div([dbc.Row([html.H1("Appraisal Calculator",style={'text-align': 'center','margin-left':'50px','color':'black'})]),
                                     dbc.Row([dbc.Col([dbc.Button(
                            "Back",
                            id="back-button", color="primary",#outline=True,
                            style={'text-align':'center', 'margin-left': '850px'}, href= '/'
                            
                        )], width=9)])
                          ])]
               )

WELCOME = html.Div(children=html.H4("You have two options, to calculate single appraisal or bulk",style={'color':'black'}))

TAB_single =html.Div(children=[html.Br(),
                          dbc.Container(id='container'),
                          html.Br(),
                          dbc.Row([dbc.Col([html.P("Number of rooms",style={'font-weight': 'bold'})],width=3),
                                                  dbc.Col([dbc.Input(id="var1", 
                                                                     type='text',
                                                                     placeholder="Variable1")],width=9)],
                                                 no_gutters=True),
                                         html.Br(),
                         dbc.Row([dbc.Col(html.P("Number of bathrooms",style={'font-weight': 'bold'}),width=3),
                                                  dbc.Col(dbc.Input(id="var2", 
                                                                    type='text',
                                                                    placeholder="Variable2"),width=9)],
                                 no_gutters=True),
                         html.Br(),
                         dbc.Row([dbc.Col(html.P("Square meters",style={'font-weight': 'bold'}),width=3),
                                                  dbc.Col(dbc.Input(id="var3", 
                                                                    type='text',
                                                                    placeholder="Variable3"),width=9)],
                                                 no_gutters=True),
                             html.Br(),
                        dbc.Row([dbc.Col(html.P("Address",style={'font-weight': 'bold'}),width=3),
                                                  dbc.Col(dbc.Input(id="var4", 
                                                                    type='text',
                                                                    placeholder="Variable4"),width=9)],
                                                 no_gutters=True),
                             html.Br(),
                            dbc.Row([dbc.Col(dbc.Button("Calculate",
                            id="appraisal-calculator-button", color="primary",style={'margin-left':'450px'})),
                                     dbc.Col(html.P(id="individual_value"))])
                            ])

TAB_bulk =html.Div(children=[html.Br(),
                          dbc.Container(id='container'),
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
                          dbc.Row([dbc.Col(dbc.Button("Calculate",
                            id="appraisal-bulk-button", color="primary",style={'margin-left':'450px'})),
                                     dbc.Col(html.P(id="bulk_value"))])
                            ])



TABS    = dcc.Tabs([dcc.Tab(TAB_single  , label= "Individual Appraisal"),
                    dcc.Tab(TAB_bulk  , label= "Bulk Upload")],
                                     colors= {"border": "white",
                                              "primary": "DarkBlue",
                                              "background": "white"})

sigma_layout = html.Div([html.Br(),html.Br(),dbc.Row([dbc.Col(nav)]),
                         html.Br(),
                         dbc.Row([dbc.Col(dbc.Card(dbc.CardBody([WELCOME],style={"height": "10rem",'box-shadow': '0 4px 8px 0 rgba(0,0,0,0.2)','color':'success'})), # https://www.w3schools.com/colors/colors_names.asp
                                          width={"size": 2},
                                          style={"margin-left": "40px"}
                                          ),
                                  dbc.Col(dbc.Card(dbc.CardBody([TABS],style={"height": "40rem"})),
                                          width={"size": 9},
                                          style={"margin-left": "40px"})],
                                  no_gutters=True)])

def Appraisal_calculator():
    layout = html.Div(children=[sigma_layout])
    return layout