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
# Dash setting:
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.UNITED],
                meta_tags=[
    {"name": "viewport", "content": "width=device-width, initial-scale=1"}])


app.title = 'Live bolig dashboard'
server = app.server


def app_layout():
    bolig_type_list = ['Lejlighed', 'Rækkehus', 'Villa', 'Værelse']

    print()
    print('------------- Running app_layout() ---------------')
    print()
    #----------------------------------------
    # LAYOUT:
    return html.Div([
        html.Div(id='header_row'),

        html.P([], style={'padding': '5px'}),

        html.Div(id='top_row'),

        html.P([], style={'padding': '5px'}),

        dbc.Col([
            html.Div(id='map_today'),
        ], width=3),

        html.P([], style={'padding': '5px'}),

        html.Div(id='graph_row'),

        html.P([], style={'padding': '5px'}),

        dbc.Card([
            dbc.CardBody([
                dbc.Row([
                    html.H3('Seneste 5 boliger oprettet'),
                ]),
                dbc.Row([
                    html.Div(id='info_table')
                ])

            ])
        ]),



        html.P([], style={'padding': '15px'}),

        html.Div(['Created by Mads Jepsen Claussen'],
                 style={'textAlign': 'center'}),


        ################################
        # Interval-Settings:
        dcc.Interval(
            id='interval-component',
            # interval=(1000 * 3600) / 2,  # 0,5 time
            # interval=(1000 * 3600) / 60,  # 1 minut
            interval=2000,  # 2 sekunder
            n_intervals=100),


        ################################
        # Modal-Settings:
        dbc.Modal([
            dbc.ModalHeader("Indstillinger for dashboard"),
            dbc.ModalBody(
                dcc.Dropdown(id='bolig_type_value', options=[{'label': i, 'value': i} for i in bolig_type_list], value=[],
                             multi=True, placeholder='Vælg en eller flere boligtyper her...', style={'width': '300px'})
            ),
            dbc.ModalFooter(
                dbc.Button("Luk", color='primary', id="close",
                           className="ml-auto")
            ),
        ], id="modal", size='l', centered=True),

    ], style={'backgroundColor': '#F7F8FC', 'padding-left': '20px', 'padding-right': '20px', 'padding-top': '10px', 'padding-bottom': '10px'})


app.layout = app_layout


########################################
# MODAL CALL BACK
########################################
@app.callback(Output("modal", "is_open"),
              [Input("open", "n_clicks"),
               Input("close", "n_clicks")],
              [State("modal", "is_open")])
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


@app.callback(Output('header_row', 'children'),
              [Input('interval-component', 'n_intervals'),
               Input('bolig_type_value', 'value')])
def header_row(n, bolig_type_value):
    df = get_data_file.get_data(n, bolig_type_value)

    last_update = (pd.to_datetime('today') + timedelta(hours=2)
                   ).strftime('%d-%m-%Y kl. %H:%M:%S')

    current_date = df['oprettelsesdato'].max().strftime("%d-%m-%Y")

    return dbc.Card([
        dbc.CardBody([
                    dbc.Row([
                            dbc.Col([
                                    html.H1([current_date],
                                            style={'margin-top': '-15px'}),
                                    ], width=7),

                            dbc.Col([
                                    html.Div(last_update,
                                             style={'textAlign': 'right', 'margin-top': '-15px', 'margin-right': '-15px'}),
                                    dbc.Button("Indstillinger", color='primary', outline=True, style={'float': 'right', 'margin-right': '-10px', 'margin-top': '10px'},
                                               id="open", size="sm"),
                                    ], width=5)
                            ])
                    ])
    ]),


@app.callback(Output('top_row', 'children'),
              [Input('interval-component', 'n_intervals'),
               Input('bolig_type_value', 'value')])
def top_row(n, bolig_type_value):
    df = get_data_file.get_data(n, bolig_type_value)

    df_today = df[df['oprettelsesdato'] == df['oprettelsesdato'].max()]

    current_date = df['oprettelsesdato'].max().strftime("%d-%m-%Y")

    num_listings = len(df_today)

    return [dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.Div([
                                    html.H3([current_date]),
                                    html.P(['Dagens dato'])


                                ], style={'textAlign': 'center'})
                            ])
                        ])
                    ], width=2),


                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.Div([
                                    html.H3([num_listings]),
                                    html.P(['Oprettede boliger i dag'])


                                ], style={'textAlign': 'center'})
                            ])
                        ])
                    ], width=2),


                    ])]


@app.callback(Output('map_today', 'children'),
              [Input('interval-component', 'n_intervals'),
               Input('bolig_type_value', 'value')])
def map_today(n, bolig_type_value):
    df = get_data_file.get_data(n, bolig_type_value)

    df = df[df['oprettelsesdato'] == df['oprettelsesdato'].max()]

    return [dbc.Row([
                    dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.Div(
                                        dcc.Graph(
                                            figure=graph_functions.map_today(df), config={'displayModeBar': False})
                                    )

                                ], style={'textAlign': 'center'})
                            ])
                            ])
                    ])

            ]


@app.callback(Output('graph_row', 'children'),
              [Input('interval-component', 'n_intervals'),
               Input('bolig_type_value', 'value')])
def graph_row(n, bolig_type_value):
    df = get_data_file.get_data(n, bolig_type_value)

    return [dbc.Row([
                    dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.Div(
                                        dcc.Graph(
                                            figure=graph_functions.total_timeseries(df), config={'displayModeBar': False})
                                    )

                                ], style={'textAlign': 'center'})
                            ])
                            ])
                    ])

            ]


@ app.callback(Output('info_table', 'children'),
               [Input('interval-component', 'n_intervals'),
                Input('bolig_type_value', 'value')])
def info_table(n, bolig_type_value):
    df = get_data_file.get_data(n, bolig_type_value)
    df = df.tail(5)
    df.sort_values('oprettelsesdato', ascending=False, inplace=True)

    df['oprettelsesdato'] = df['oprettelsesdato'].dt.strftime("%d-%m-%Y")

    df['månedlig_leje'] = df['månedlig_leje'].apply(lambda x: str(x) + ' kr.')

    df = df[['titel', 'adresse', 'boligtype',
             'månedlig_leje', 'oprettelsesdato']]

    table = dbc.Table.from_dataframe(
        df, striped=True, responsive=True, borderless=True, size='sm')

    return table


if __name__ == '__main__':
    app.run_server(debug=False)
