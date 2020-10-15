########
# Andre Python files:
import get_data_file
import graph_functions

########
# Dash imports
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output, State

import dash_bootstrap_components as dbc

import pandas as pd
import numpy as np
from datetime import timedelta


########
# Universal lists
color_maps = {'Lejlighed': '#939BFC', 'Rækkehus': '#F58677',
              'Villa': '#68DBB6', 'Værelse': '#ffd700'}

bolig_type_list = ['Lejlighed', 'Rækkehus', 'Villa', 'Værelse']


by_list = ['København', 'Aarhus', 'Odense', 'Aalborg', 'Esbjerg']


########
# Dash setting:
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SPACELAB])
app.title = 'Live bolig dashboard'
server = app.server


def app_layout():
    #----------------------------------------
    # LAYOUT:
    return html.Div([
        html.Div(id='header_row'),

        dbc.Collapse(
            dbc.Card(
                dbc.CardBody([
                    html.H4(['Indstillinger'], style={'textAlign': 'center'}),

                    dbc.Row([
                            dbc.Col([
                                html.Div(['Vælg én eller flere boligtyper:']),
                                    dcc.Dropdown(id='bolig_type_value', options=[{'label': i, 'value': i} for i in bolig_type_list], value=[],
                                                 multi=True, placeholder='Vælg boligtyper her...', style={'width': '300px'})
                                    ], width={"size": 4, "offset": 2}),


                            dbc.Col([
                                html.Div(
                                    ['Vælg én eller flere byer:']),
                                dcc.Dropdown(id='by_value', options=[{'label': i, 'value': i} for i in by_list], value=[],
                                             multi=True, placeholder='Vælg byer her...', style={'width': '300px'})
                            ], width={"size": 4, "offset": 2})
                            ])

                ])),
            id="collapse",
        ),

        html.P([], style={'padding': '5px'}),

        html.Div(id='top_row'),

        html.P([], style={'padding': '5px'}),

        html.Div(id='map_today'),

        html.P([], style={'padding': '5px'}),

        html.Div(id='graph_row'),

        html.P([], style={'padding': '5px'}),

        html.Div(id='table_row'),

        html.P([], style={'padding': '15px'}),

        html.Div(['Created by Mads Jepsen Claussen'],
                 style={'textAlign': 'center'}),

        ################################
        # Interval-Settings:
        dcc.Interval(
            id='interval-component',
            interval=4000,  # 4 sekunder
            n_intervals=200),

        ################################
        # Modal-Settings:
        dbc.Modal([
            dbc.ModalHeader("Bolig-site scrape og analyse"),
            dbc.ModalBody(
                html.Div([
                    html.H4('Om'),
                    html.Div(
                        "Dette dashboard opdateres hvert 4. sekund med flere boliger. Formålet er at illustere hvordan et 'live' dashboard kunne se ud."),
                    html.Br(),
                    html.Div(),
                    html.H4('Indhold'),
                    html.Div(),
                    html.A("Hjem (Github Pages)",
                           href='https://madsjc.github.io/Bolig-site-analyse/', target="_blank"),
                    html.Div(),
                    html.Br(),
                    html.A("1. Webscrape script (Python)",
                           href='https://github.com/MadsJC/Bolig-site-analyse/blob/master/PYTHON%20Bolig-Scraper.py', target="_blank"),
                    html.Br(),
                    html.A("2. Data Clean (Jupyter Notebook)",
                           href='https://nbviewer.jupyter.org/github/MadsJC/Bolig-site-analyse/blob/master/PYTHON%20-%20Data%20Clean.ipynb?flush_cache=true', target="_blank"),
                    html.Br(),
                    html.A("3. Exploratory Data Analysis - EDA (Jupyter Notebook)",
                           href='https://nbviewer.jupyter.org/github/MadsJC/Bolig-site-analyse/blob/master/PYTHON%20-%20Exploratory%20Data%20Analysis%20%28EDA%29.ipynb?flush_cache=true', target="_blank"),
                    html.Br(),
                    html.A("4. Live dashboard (Hosted ved Heroku)",
                           href='https://mc-livebolig.herokuapp.com/', target="_blank", style={'font-weight': 'bold'}),
                    html.Br(),
                    html.A("5. Live dashboard BACKEND (Python)",
                           href='https://github.com/MadsJC/Bolig-site-analyse/tree/master/Bolig_dashboard_live', target="_blank"),
                ])
            ),
            dbc.ModalFooter(
            ),
        ], id="modal", size='l', centered=True),

    ], style={'backgroundColor': '#CAD2D3', 'padding-left': '20px', 'padding-right': '20px', 'padding-top': '10px', 'padding-bottom': '10px'})


app.layout = app_layout


########################################
# MODAL CALL BACK
########################################
@ app.callback(Output("modal", "is_open"),
               [Input("open", "n_clicks")],
               [State("modal", "is_open")])
def toggle_modal(n1, is_open):
    if n1:
        return not is_open
    return is_open


########################################
# COLLAPSE CALL BACK
########################################
@ app.callback(
    Output("collapse", "is_open"),
    [Input("collapse-button", "n_clicks")],
    [State("collapse", "is_open")])
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

########################################
# header_row CALL BACK
########################################


@ app.callback(Output('header_row', 'children'),
               [Input('interval-component', 'n_intervals'),
                Input('bolig_type_value', 'value'),
                Input('by_value', 'value')])
def header_row(n, bolig_type_value, by_value):
    df = get_data_file.get_data(n, bolig_type_value, by_value)

    last_update = (pd.to_datetime('today') + timedelta(hours=2)
                   ).strftime('%d-%m-%Y kl. %H:%M:%S')

    current_date = df['oprettelsesdato'].max().strftime("%d-%m-%Y")

    return dbc.Card([
        dbc.CardBody([
                    dbc.Row([
                            dbc.Col([
                                html.H3(['Live bolig dashboard']),
                                    html.H1([current_date],
                                            style={'font-weight': 'bold', 'margin-top': '-15px', 'font-size': '70px'}),
                                    ], width=7),

                            dbc.Col([
                                    html.Div(last_update,
                                             style={'textAlign': 'right', 'margin-top': '-15px', 'margin-right': '-15px'}),
                                    dbc.Button("About", color='warning', outline=True, style={'float': 'right', 'margin-right': '-10px', 'margin-top': '10px'},
                                               id="open", size="sm"),
                                    dbc.Button("Indstillinger", color='info', outline=True, style={'float': 'right', 'margin-right': '-56px', 'margin-top': '50px'},
                                               id="collapse-button", size="sm"),
                                    ], width=5)
                            ], style={'margin-bottom': '-25px'})
                    ])
    ]),


########################################
# top_row CALL BACK
########################################
@ app.callback(Output('top_row', 'children'),
               [Input('interval-component', 'n_intervals'),
                Input('bolig_type_value', 'value'),
                Input('by_value', 'value')])
def top_row(n, bolig_type_value, by_value):
    df = get_data_file.get_data(n, bolig_type_value, by_value)

    df_today = df[df['oprettelsesdato'] == df['oprettelsesdato'].max()]

    num_listings = '{:,}'.format(len(df_today))

    total_images = '{:,}'.format(df_today['image_count'].sum())

    mean_månedlig_leje = str('{:,}'.format(int(
        df_today['månedlig_leje'].mean()))) + ' kr.'

    mean_depositum = str('{:,}'.format(int(
        df_today['depositum'].mean()))) + ' kr.'

    mean_aconto = str('{:,}'.format(int(
        df_today['aconto'].mean()))) + ' kr.'

    mean_kvadratmeter = str(int(
        df_today['kvadratmeter'].mean())) + ' m2'

    return [dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.Div([
                                    html.H3([num_listings], style={
                                            'margin-bottom': '-4px'}),
                                    html.P(['Oprettede'], style={
                                           'font-size': '12px'}),
                                    html.P(['boliger i dag'], style={
                                           'margin-top': '-20px', 'font-size': '12px'})
                                ], style={'textAlign': 'center', 'margin-bottom': '-20px'})
                            ])
                        ])
                    ], width=2),

                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.Div([
                                    html.H3([total_images], style={
                                            'margin-bottom': '-4px'}),
                                    html.P(['Oploadede'], style={
                                           'font-size': '12px'}),
                                    html.P(['billeder'], style={
                                           'margin-top': '-20px', 'font-size': '12px'})
                                ], style={'textAlign': 'center', 'margin-bottom': '-20px'})
                            ])
                        ])
                    ], width=2),


                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.Div([
                                    html.H3([mean_månedlig_leje], style={
                                            'margin-bottom': '-4px'}),
                                    html.P(['Gennemsnit'], style={
                                           'font-size': '12px'}),
                                    html.P(['månedlig leje'], style={
                                           'margin-top': '-20px', 'font-size': '12px'})
                                ], style={'textAlign': 'center', 'margin-bottom': '-20px'})
                            ])
                        ])
                    ], width=2),


                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.Div([
                                    html.H3([mean_kvadratmeter], style={
                                            'margin-bottom': '-4px'}),
                                    html.P(['Gennemsnit'], style={
                                           'font-size': '12px'}),
                                    html.P(['kvadratmeter'], style={
                                           'margin-top': '-20px', 'font-size': '12px'})
                                ], style={'textAlign': 'center', 'margin-bottom': '-20px'})
                            ])
                        ])
                    ], width=2),

                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.Div([
                                    html.H3([mean_depositum], style={
                                            'margin-bottom': '-4px'}),
                                    html.P(['Gennemsnit'], style={
                                           'font-size': '12px'}),
                                    html.P(['depositum'], style={
                                           'margin-top': '-20px', 'font-size': '12px'})
                                ], style={'textAlign': 'center', 'margin-bottom': '-20px'})
                            ])
                        ])
                    ], width=2),

                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.Div([
                                    html.H3([mean_aconto], style={
                                            'margin-bottom': '-4px'}),
                                    html.P(['Gennemsnit'], style={
                                           'font-size': '12px'}),
                                    html.P(['aconto'], style={
                                           'margin-top': '-20px', 'font-size': '12px'})
                                ], style={'textAlign': 'center', 'margin-bottom': '-20px'})
                            ])
                        ])
                    ], width=2),

                    ])]

########################################
# map_today CALL BACK
########################################


@ app.callback(Output('map_today', 'children'),
               [Input('interval-component', 'n_intervals'),
                Input('bolig_type_value', 'value'),
                Input('by_value', 'value')])
def map_today(n, bolig_type_value, by_value):
    df = get_data_file.get_data(n, bolig_type_value, by_value)

    df = df[df['oprettelsesdato'] == df['oprettelsesdato'].max()]

    return [dbc.Row([
                    dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.Div(
                                        dcc.Graph(
                                            figure=graph_functions.map_today(df, color_maps), config={'displayModeBar': False}))
                                ], style={'textAlign': 'center', 'padding': '5px'})
                            ])
                            ], width=3),

                    dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.Div(
                                        dcc.Graph(
                                            figure=graph_functions.top5_by(df, color_maps), config={'displayModeBar': False}))
                                ], style={'textAlign': 'center', 'padding': '5px'})
                            ]),

                            html.Div([], style={'padding': '12px'}),

                            dbc.Card([
                                dbc.CardBody([
                                    html.Div(
                                        dcc.Graph(
                                            figure=graph_functions.bar_boligtype(df, color_maps), config={'displayModeBar': False}))
                                ], style={'textAlign': 'center', 'padding': '5px'})
                            ])
                            ], width=3),

                    dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.Div(
                                        dcc.Graph(
                                            figure=graph_functions.scatter_månedlig_leje_kvadratmeter(df, color_maps), config={'displayModeBar': False}))
                                ], style={'textAlign': 'center', 'padding-top': '5px'})
                            ])
                            ], width=6),
                    ])

            ]

########################################
# graph_row CALL BACK
########################################


@app.callback(Output('graph_row', 'children'),
              [Input('interval-component', 'n_intervals'),
               Input('bolig_type_value', 'value'),
               Input('by_value', 'value')])
def graph_row(n, bolig_type_value, by_value):
    df = get_data_file.get_data(n, bolig_type_value, by_value)

    return [dbc.Row([
                    dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.Div(
                                        dcc.Graph(
                                            figure=graph_functions.total_timeseries(df, color_maps), config={'displayModeBar': False})
                                    )
                                ], style={'textAlign': 'center'})
                            ])
                            ]),
                    ])
            ]

########################################
# table_row CALL BACK
########################################


@ app.callback(Output('table_row', 'children'),
               [Input('interval-component', 'n_intervals'),
                Input('bolig_type_value', 'value'),
                Input('by_value', 'value')])
def info_table(n, bolig_type_value, by_value):
    df = get_data_file.get_data(n, bolig_type_value, by_value)

    df_today = df[df['oprettelsesdato'] == df['oprettelsesdato'].max()]

    # Latest 5 entities
    df_table = df.tail(5)

    df_table.sort_values('oprettelsesdato', ascending=False, inplace=True)

    df_table['månedlig_leje'] = df_table['månedlig_leje'].apply(
        lambda x: str(x) + ' kr.')

    df_table = df_table[['titel', 'adresse', 'boligtype',
                         'månedlig_leje']]

    latest_5_table = dbc.Table.from_dataframe(
        df_table, striped=True, responsive=True, borderless=False, size='sm')

    # Most expensive entity
    dyreste_bolig = df_today[df_today['månedlig_leje']
                             == df_today['månedlig_leje'].max()][['titel', 'adresse', 'boligtype',
                                                                  'månedlig_leje']]

    dyreste_bolig['månedlig_leje'] = dyreste_bolig['månedlig_leje'].apply(
        lambda x: str('{:,}'.format(x)) + ' kr.')

    dyreste_bolig_table = dbc.Table.from_dataframe(
        dyreste_bolig, striped=False, responsive=True, borderless=True, size='sm')

    # Cheapest entity
    billigste_bolig = df_today[df_today['månedlig_leje']
                               == df_today['månedlig_leje'].min()][['titel', 'adresse', 'boligtype',
                                                                    'månedlig_leje']]
    billigste_bolig['månedlig_leje'] = billigste_bolig['månedlig_leje'].apply(
        lambda x: str('{:,}'.format(x)) + ' kr.')

    billigste_bolig_table = dbc.Table.from_dataframe(
        billigste_bolig, striped=False, responsive=True, borderless=True, size='sm')

    return [dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        html.H3(['Seneste 5 boliger oprettet'],
                                style={'font-weight': 'bold'}),
                    ]),
                    dbc.Row([
                        html.Div([latest_5_table])
                    ])
                ])
            ]),
        ], width=6),

        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        html.H4(['Dyreste  husleje oprettet i dag'], style={
                                'font-weight': 'bold'}),
                    ]),
                    dbc.Row([
                        html.Div(dyreste_bolig_table),
                    ]),

                    html.Div([], style={'padding': '7px'}),

                    dbc.Row([
                        html.H4(['Billigste husleje oprettet i dag'], style={
                                'font-weight': 'bold'}),
                    ]),
                    dbc.Row([
                        html.Div(billigste_bolig_table),
                    ])


                ])
            ]),
        ], width=6),
    ])]


if __name__ == '__main__':
    app.run_server(debug=False)
