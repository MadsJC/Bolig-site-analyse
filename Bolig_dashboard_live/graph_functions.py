import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import dash_core_components as dcc
from datetime import timedelta


########################################
# total_timeseries function
########################################
def total_timeseries(df, color_maps):
    df_grouped = df.groupby(['boligtype', 'oprettelsesdato'],
                            as_index=False)['ids'].count()
    last_20_days = df_grouped['oprettelsesdato'].max() - timedelta(days=20)
    df_grouped = df_grouped[df_grouped['oprettelsesdato'] > last_20_days]

    df_grouped_mean = df_grouped.groupby(
        'oprettelsesdato', as_index=False)['ids'].mean()

    traces = []

    for i in df['boligtype'].unique():
        x = df_grouped[df_grouped['boligtype']
                       == i]['oprettelsesdato']
        y = df_grouped[df_grouped['boligtype'] == i]['ids']
        traces.append(go.Bar(x=x, y=y, name=i, marker_color=color_maps[i],
                             marker_line_color='rgb(8,48,107)',
                             marker_line_width=0.6, opacity=0.7))

    traces.append(go.Scatter(x=df_grouped_mean['oprettelsesdato'], y=df_grouped_mean['ids'], name='Mean',
                             opacity=0.70, mode='lines', marker_color='black',
                             line=dict(color='firebrick', width=2,
                                       dash='dash')))

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
                barmode='stack',
                title='Antal oprettede boliger (seneste 20 dage)',
                transition={
                    'duration': 500,
                    'easing': 'cubic-in-out'},
                margin={'l': 30, 'r': 1, 't': 30, 'b': 30})}

########################################
# top5_by function
########################################


def top5_by(df, color_maps):
    df_grouped = df[df['oprettelsesdato'] == df['oprettelsesdato'].max()]

    df_grouped = df_grouped.groupby([
        'navn'], as_index=False)['ids'].count().sort_values('ids', ascending=True).tail(5)
    df_grouped['navn'] = df_grouped['navn'].apply(lambda x: x + ' ')

    traces = []

    y = df_grouped['navn']
    x = df_grouped['ids']
    traces.append(go.Bar(x=x, y=y, text=x, textposition='inside',
                         orientation='h', marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                         marker_line_width=0.6, opacity=0.7))

    return {'data': traces,
            'layout': dict(
                yaxis=dict(
                    showgrid=False,
                    zeroline=False,
                    showticklabels=True),
                xaxis=dict(
                    showgrid=False,
                    zeroline=False,
                    showticklabels=True,
                    nticks=20),
                autosize=True,
                height=180,
                title='Top 5 byer',
                margin={'l': 75, 'r': 1, 't': 30, 'b': 1})}

########################################
# bar_boligtype function
########################################


def bar_boligtype(df, color_maps):
    df_valuecounts_boligtyper = df['boligtype'].value_counts(normalize=True).reset_index(
    ).rename(columns={'index': 'boligtype', 'boligtype': 'antal'}).sort_values('antal', ascending=True)

    df_valuecounts_boligtyper['antal'] = (
        df_valuecounts_boligtyper['antal'] * 100).astype(int)
    df_valuecounts_boligtyper['text_val'] = df_valuecounts_boligtyper['antal'].apply(
        lambda x: str(x) + ' %')

    traces = []
    for i in df_valuecounts_boligtyper['boligtype'].unique():
        y = df_valuecounts_boligtyper[df_valuecounts_boligtyper['boligtype']
                                      == i]['boligtype']
        x = df_valuecounts_boligtyper[df_valuecounts_boligtyper['boligtype'] == i]['antal']
        text_val = df_valuecounts_boligtyper[df_valuecounts_boligtyper['boligtype']
                                             == i]['text_val']
        traces.append(go.Bar(x=x, y=y, text=text_val, textposition='auto',
                             orientation='h', marker_color=color_maps[i],
                             marker_line_color='rgb(8,48,107)',
                             marker_line_width=0.6, opacity=0.7))

    return {'data': traces,
            'layout': dict(
                yaxis=dict(
                    showgrid=False,
                    zeroline=False,
                    showticklabels=True),
                xaxis=dict(
                    showgrid=False,
                    zeroline=False,
                    showticklabels=True,
                    nticks=20),
                autosize=True,
                barmode='stack',
                showlegend=False,
                height=180,
                title='Boligtyper',
                margin={'l': 75, 'r': 1, 't': 30, 'b': 1})}

########################################
# scatter_månedlig_leje_kvadratmeter function
########################################


def scatter_månedlig_leje_kvadratmeter(df, color_maps):
    df_grouped = df[df['oprettelsesdato'] == df['oprettelsesdato'].max()]

    traces = []

    for i in df['boligtype'].unique():
        x = df_grouped[df_grouped['boligtype']
                       == i]['kvadratmeter']
        y = df_grouped[df_grouped['boligtype'] == i]['månedlig_leje']
        traces.append(go.Scatter(x=x, y=y, name=i, marker_color=color_maps[i], marker_size=10,
                                 opacity=0.70, mode='markers'))

    return {'data': traces,
            'layout': dict(
                yaxis=dict(
                    showgrid=True,
                    zeroline=False,
                    title='Månedlig leje (dkk)',
                    showticklabels=True),
                xaxis=dict(
                    showgrid=True,
                    zeroline=False,
                    showticklabels=True,
                    title='Kvadratmeter',
                    nticks=20),
                showlegend=True,
                autosize=True,
                height=380,
                transition={
                    'duration': 500,
                    'easing': 'cubic-in-out'},
                margin={'l': 50, 'r': 1, 't': 5, 'b': 40})}

########################################
# map_today function
########################################


def map_today(df_map, color_maps):
    mapbox_access_token = 'pk.eyJ1IjoibWFkc2pjIiwiYSI6ImNrZWN3YzF6bjAwcDUyc3Q1OWc1amJhaDEifQ.MTO6xHwzu-9FJopzujIHlw'
    px.set_mapbox_access_token(mapbox_access_token)

    df_map['navn'] = df_map['navn'].apply(lambda x: x.split(' ')[0])

    df_map = df_map.groupby(['navn', 'boligtype'], as_index=False).agg(
        {'Latitude': 'mean', 'Longitude': 'mean', 'adresse': 'count'})
    df_map = df_map.rename(columns={'adresse': 'Antal'})

    fig_mapbox = go.Figure()

    for i in df_map['boligtype'].unique():
        site_lat = df_map[df_map['boligtype'] == i]['Latitude']
        site_lon = df_map[df_map['boligtype'] == i]['Longitude']
        fig_mapbox.add_trace(go.Scattermapbox(
            lat=site_lat,
            lon=site_lon,
            mode='markers',
            name=i,
            marker=go.scattermapbox.Marker(
                size=df_map['Antal'] + 4,
                color=color_maps[i],
                opacity=0.9
            ),
            text=i,
            hoverinfo='text'
        ))

    fig_mapbox.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        autosize=True,
        height=400,
        hovermode='closest',
        showlegend=False,
        mapbox=dict(
            accesstoken=mapbox_access_token,
            center=dict(
                lat=56.263,
                lon=10.501
            ),
            zoom=5.5,
            style='light',
        ),
    )

    return fig_mapbox
