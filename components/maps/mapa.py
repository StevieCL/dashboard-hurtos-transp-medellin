from dash import html, dcc
import pandas as pd
import plotly.graph_objects as go

df = pd.read_csv('data/data_to_map.csv')
df['color'] = df.sexo.replace(to_replace={'Hombre':'blue', 'Mujer':'red'})
df.fecha_hecho = pd.to_datetime(df.fecha_hecho)
df.fecha_hecho = df.fecha_hecho.dt.date
df.fecha_hecho = pd.to_datetime(df.fecha_hecho)

class mapita:
    def __init__(self, map_title:str, id:str, df, coord=[6.217, -75.567]):
        self.title = map_title
        self.id = id
        self.df = df
        self.coord = coord

    @staticmethod
    def figure_map(self):
        mapbox_token = 'pk.eyJ1Ijoic3RldmllY2wiLCJhIjoiY2w3OWgwaGgzMGRkdzNwbzQxb2IwY2N6dyJ9.Ws3kDqCyqYZ4k3LI-ah1pA'
        fig = go.Figure(go.Scattermapbox(
            lat=self.df['latitud'],
            lon=self.df['longitud'],
            mode='markers',
            text=self.df[['sexo', 'medio_transporte', 'modalidad']],
            marker=go.scattermapbox.Marker(size=9,
                                        opacity=0.5,
                                        color=self.df['color']
                                        )
        ))

        fig.update_layout(
            mapbox_style='open-street-map',
            autosize=True,
            hovermode='closest',
            mapbox=dict(
                accesstoken=mapbox_token,
                bearing=0,
                center=dict(
                    lat=self.coord[0],
                    lon=self.coord[1],
                ),
                zoom=10
            )
            
            )

        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        
        return fig
       

    def display(self):
        
        layout = html.Div(
            [
                html.H4([self.title]),
                html.Div([
                    dcc.Graph(figure=mapita.figure_map(self), id=self.id)
                ])
            ]
        )
        return layout