import dash
from dash import dcc
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import json
import plotly.graph_objects as go
import warnings
warnings.filterwarnings("ignore")
import locale
import dash_html_components as html



app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )




# Set the locale to Turkish
locale.setlocale(locale.LC_ALL, 'tr_TR.utf8')

access_token = 'pk.eyJ1IjoiYWJkdWxrZXJpbW5lc2UiLCJhIjoiY2s5aThsZWlnMDExcjNkcWFmaWUxcmh3YyJ9.s-4VLvmoPQFPXdu9Mcd6pA'
px.set_mapbox_access_token(access_token)



app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )

layout=dbc.Container([


    dbc.Row([
        dbc.Col([
        html.Div([
            html.Iframe(srcDoc=open('./assets/fig_bar_polar.html', 'r', encoding='utf-8').read())
            ],style={'width':'100%','height':'100%'})
        ],className="bar_polar",xs=12, sm=12, md=6, lg=6, xl=6),
        dbc.Col([
        html.Div([
            html.Iframe(srcDoc=open('./assets/map.html', 'r', encoding='utf-8').read())
            ],style={'width':'100%','height':'100%'})
        ],style={'height': '100%'},xs=12, sm=12, md=6, lg=6, xl=6),


    ],className='g-0'),

    dbc.Row([
        dbc.Col([
            html.Div([
            html.Iframe(srcDoc=open('./assets/bar.html', 'r', encoding='utf-8').read())],style={'width':'100%','height':'100%'})
        ],xs=12, sm=12, md=12, lg=12, xl=12),
        # dbc.Col([dcc.Graph(id='scatter_graph',figure=fig_scatter)],xs=12, sm=12, md=6, lg=6, xl=6)
    ],className='g-0')
],style={'background-color':'#2b2b2b'}, className= 'animasyon-container',fluid=True)








