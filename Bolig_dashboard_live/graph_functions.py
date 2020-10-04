import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import dash_core_components as dcc


def total_timeseries(df):
    df_grouped = df.groupby(['boligtype', 'oprettelsesdato'],
                            as_index=False)['månedlig_leje'].mean()

    df_grouped['oprettelsesdato'] = df_grouped['oprettelsesdato'].dt.strftime(
        "%d-%m-%Y")

    traces = []

    for i in df['boligtype'].unique():
        x = df_grouped[df_grouped['boligtype']
                       == i]['oprettelsesdato'].tail(20)
        y = df_grouped[df_grouped['boligtype'] == i]['månedlig_leje'].tail(20)
        traces.append(go.Scatter(x=x, y=y, mode='lines', name=i,
                                 opacity=0.70))

    return {'data': traces,
            'layout': dict(
                yaxis=dict(
                    showgrid=True,
                    zeroline=True,
                    showticklabels=True),
                xaxis=dict(
                    showgrid=False,
                    zeroline=False,
                    showticklabels=True,
                    nticks=20),
                showlegend=True,
                autosize=True,
                height=250,
                title='Gennemsnit månedlig husleje',
                transition={
                    'duration': 500,
                    'easing': 'cubic-in-out'},
                margin={'l': 35, 'r': 1, 't': 40, 'b': 50})}


def map_today(df_map):

    mapbox_access_token = 'pk.eyJ1IjoibWFkc2pjIiwiYSI6ImNrZWN3YzF6bjAwcDUyc3Q1OWc1amJhaDEifQ.MTO6xHwzu-9FJopzujIHlw'
    px.set_mapbox_access_token(mapbox_access_token)

    df_map['navn'] = df_map['navn'].apply(lambda x: x.split(' ')[0])

    df_map = df_map.groupby(['navn', 'boligtype'], as_index=False).agg(
        {'Latitude': 'mean', 'Longitude': 'mean', 'adresse': 'count'})
    df_map = df_map.rename(columns={'adresse': 'Antal'})

    fig_mapbox = px.scatter_mapbox(df_map, lat="Latitude", lon="Longitude",
                                   color="boligtype", size='Antal',
                                   color_continuous_scale=px.colors.cyclical.IceFire, size_max=30, zoom=5.2)

    fig_mapbox.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        legend_orientation='h'
    )

    return fig_mapbox
