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

color_maps = {'Lejlighed': '#939BFC', 'Rækkehus': '#F58677',
              'Villa': '#68DBB6', 'Værelse': '#ffd700'}

bolig_type_list = ['Lejlighed', 'Rækkehus', 'Villa', 'Værelse']

########
# Dash setting:
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SPACELAB])


app.title = 'Live bolig dashboard'
server = app.server


def app_layout():

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

    ], style={'backgroundColor': '#CAD2D3', 'padding-left': '20px', 'padding-right': '20px', 'padding-top': '10px', 'padding-bottom': '10px'})


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
                                html.H3('Live bolig Dashboard'),
                                    html.H1([current_date],
                                            style={'font-weight': 'bold', 'margin-top': '-15px'}),
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

    num_listings = len(df_today)

    total_images = df_today['image_count'].sum()

    mean_månedlig_leje = str(int(
        df_today['månedlig_leje'].mean())) + ' kr.'

    mean_depositum = str(int(
        df_today['depositum'].mean())) + ' kr.'

    mean_aconto = str(int(
        df_today['aconto'].mean())) + ' kr.'

    mean_kvadratmeter = str(int(
        df_today['kvadratmeter'].mean())) + ' m2'

    return [dbc.Row([
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

                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.Div([
                                    html.H3([total_images]),
                                    html.P(['Oploaded billeder'])
                                ], style={'textAlign': 'center'})
                            ])
                        ])
                    ], width=2),


                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.Div([
                                    html.H3([mean_månedlig_leje]),
                                    html.P(['Gennemsnit månedlig leje'])
                                ], style={'textAlign': 'center'})
                            ])
                        ])
                    ], width=2),


                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.Div([
                                    html.H3([mean_kvadratmeter]),
                                    html.P(['Gennemsnit kvadratmeter'])
                                ], style={'textAlign': 'center'})
                            ])
                        ])
                    ], width=2),

                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.Div([
                                    html.H3([mean_depositum]),
                                    html.P(['Gennemsnit depositum'])
                                ], style={'textAlign': 'center'})
                            ])
                        ])
                    ], width=2),

                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.Div([
                                    html.H3([mean_aconto]),
                                    html.P(['Gennemsnit aconto'])
                                ], style={'textAlign': 'center'})
                            ])
                        ])
                    ], width=2),

                    ])]


@ app.callback(Output('map_today', 'children'),
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
                                            figure=graph_functions.map_today(df, color_maps), config={'displayModeBar': False}))
                                ], style={'textAlign': 'center'})
                            ])
                            ], width=3),

                    dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.Div(
                                        dcc.Graph(
                                            figure=graph_functions.top5_by(df, color_maps), config={'displayModeBar': False}))
                                ], style={'textAlign': 'center'})
                            ]),

                            html.Div([], style={'padding': '15px'}),

                            dbc.Card([
                                dbc.CardBody([
                                    html.Div(
                                        dcc.Graph(
                                            figure=graph_functions.bar_boligtype(df, color_maps), config={'displayModeBar': False}))
                                ], style={'textAlign': 'center'})
                            ])
                            ], width=3),

                    dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.Div(
                                        dcc.Graph(
                                            figure=graph_functions.scatter_månedlig_leje_kvadratmeter(df, color_maps), config={'displayModeBar': False}))
                                ], style={'textAlign': 'center'})
                            ])
                            ], width=6),
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
                                            figure=graph_functions.total_timeseries(df, color_maps), config={'displayModeBar': False})
                                    )
                                ], style={'textAlign': 'center'})
                            ])
                            ]),
                    ])
            ]


@ app.callback(Output('table_row', 'children'),
               [Input('interval-component', 'n_intervals'),
                Input('bolig_type_value', 'value')])
def info_table(n, bolig_type_value):
    df = get_data_file.get_data(n, bolig_type_value)

    df_today = df[df['oprettelsesdato'] == df['oprettelsesdato'].max()]

    df_table = df.tail(5)
    df_table.sort_values('oprettelsesdato', ascending=False, inplace=True)

    df_table['månedlig_leje'] = df_table['månedlig_leje'].apply(
        lambda x: str(x) + ' kr.')

    df_table = df_table[['titel', 'adresse', 'boligtype',
                         'månedlig_leje']]

    latest_5_table = dbc.Table.from_dataframe(
        df_table, striped=True, responsive=True, borderless=True, size='sm')

    dyreste_bolig = df_today[df_today['månedlig_leje']
                             == df_today['månedlig_leje'].max()][['titel', 'adresse', 'boligtype',
                                                                  'månedlig_leje']]

    dyreste_bolig['månedlig_leje'] = dyreste_bolig['månedlig_leje'].apply(
        lambda x: str(x) + ' kr.')

    dyreste_bolig_table = dbc.Table.from_dataframe(
        dyreste_bolig, striped=False, responsive=True, borderless=True, size='sm')

    billigste_bolig = df_today[df_today['månedlig_leje']
                               == df_today['månedlig_leje'].min()][['titel', 'adresse', 'boligtype',
                                                                    'månedlig_leje']]
    billigste_bolig['månedlig_leje'] = billigste_bolig['månedlig_leje'].apply(
        lambda x: str(x) + ' kr.')

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
                        html.Div(latest_5_table)
                    ])
                ])
            ]),
        ], width=6),

        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        html.H4(['Dyreste månedlig huslige oprettet i dag'], style={
                                'font-weight': 'bold'}),
                    ]),
                    dbc.Row([
                        html.Div(dyreste_bolig_table),
                    ]),

                    html.Div([], style={'padding': '7px'}),

                    dbc.Row([
                        html.H4(['Billigste månedlig huslige oprettet i dag'], style={
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
