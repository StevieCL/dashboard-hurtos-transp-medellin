from dash import html, dcc
from pandas import DataFrame
import plotly.express as px
import plotly.graph_objects as go

class graph:
    def __init__(self, id, title, df, tipo, nombre_columna_filtro):
        self.id = id
        self.title = title
        self.tipo = tipo
        self.df = df
        self.filtro = nombre_columna_filtro
    
    
    # def make_series(self):
    #     serie = self.df[self.filtro].value_counts().head(3)
    #     return serie
    
    @staticmethod
    def figure_graph(self):
        serie = self.df[self.filtro].value_counts().head(3)
        index, values = serie.index.to_list(), list(serie.values)
        if self.tipo == 'pie':
            pie = px.pie(values=values, names=index, hole=.3)
            pie.update_traces(textposition='inside', textinfo='percent+label')
            fig = go.Figure(data=pie)
            return fig
        
        elif self.tipo == 'bar':
            bar = px.bar(x=index, y=values,
                         labels={
                             'x':self.filtro,
                             'y':'Total'
                         }
                         )
            fig = go.Figure(data=bar)
            return fig
        
        elif self.tipo == 'histogram':
            fig = go.Figure()
            fig.add_trace(go.Histogram(x=self.df[self.df.sexo == 'Hombre']['edad'], name='Hombre'))
            fig.add_trace(go.Histogram(x=self.df[self.df.sexo == 'Mujer']['edad'], name='Mujer'))
            fig.update_layout(barmode='overlay')
            fig.update_traces(opacity=0.75)
            return fig
        
        else:
            historical = self.df.fecha_hecho.value_counts()
            historical = DataFrame(historical).sort_index()
            line_plot = px.line(x=historical.index, y=historical.fecha_hecho,
                          labels={
                              'x':'Fecha',
                              'y':'Total'
                          }
                          )
            fig = go.Figure(data=line_plot)
            return fig
    
            
        
        
    def display(self):
        layout = html.Div(
            [
                html.H4([self.title]),
                html.Div([
                    dcc.Graph(figure=graph.figure_graph(self), id=self.id)
                ])
            ]
        )
        return layout