import dash_bootstrap_components as dbc
from dash import html, dcc, callback, Input, Output, State
from dash_labs.plugins.pages import register_page
import pandas as pd

register_page(__name__, path="/dashboard")


from components.graphs.interactive_graphs import graph
from components.maps.mapa import mapita, df

dfd = pd.read_csv('data/data_dash.csv')
dfd['color'] = dfd.sexo.replace(to_replace={'Hombre':'blue', 'Mujer':'red'})
mapa1 = mapita('Mapa hurtos med', id='unique_map', df=df)
pie1 = graph('pie_trans', 'Medios de transporte', dfd, 'pie', 'medio_transporte')
bar1 = graph('bar_mod', 'Top 3 modalidad de robo', dfd, 'bar', 'modalidad')
hist1 = graph('hist_edad', 'Distribución de edades', dfd, 'histogram', 'edad')
line1 = graph('line_total', 'Hurtos en el tiempo', dfd, 'line', 'fecha_hecho')

layout = html.Div([
    dbc.Row([
        dbc.Col([
            html.Div([
                html.Div(['Fecha'], className="mb-2  selector-label"),
                dcc.DatePickerRange(
                    id="id_selector_fecha",
                    min_date_allowed=df.fecha_hecho.min().date(),
                    max_date_allowed=df.fecha_hecho.max().date(),
                    start_date=df.fecha_hecho.min().date(),
                    end_date=df.fecha_hecho.max().date(),
                    
                )
            ])
        ]),
        dbc.Col(
            html.Div([
                html.Div(['Sexo'], className="mb-2  selector-label"),
                dcc.Dropdown(
                    id="id_selector_sexo",
                    options=[
                        {"label":"Hombre", "value":"Hombre"},
                        {"label":"Mujer", "value":"Mujer"}
                    ],
                    value=["Hombre", "Mujer"],
                    multi=True
                )
            ])
        ),
        dbc.Col(
            html.Div([
                html.Div(['Medio de transporte'], className="mb-2  selector-label"),
                dcc.Dropdown(
                    id="id_selector_transp",
                    options=[
                        {"label":"Bus", "value":"Autobus"},
                        {"label":"Taxi", "value":"Taxi"},
                        {"label":"Metro", "value":"Metro"}
                    ],
                    value=["Autobus", "Taxi", "Metro"],
                    multi=True
                )
            ])
        )
        
    ]),
    dbc.Row(
            html.Div([
                html.Div(['Lugar'], className="mb-2  selector-label"),
                dcc.Dropdown(
                    id="id_selector_comuna",
                    options=[
                        {"label":"Aranjuez", "value":"Aranjuez"},
                        {"label":"Belén", "value":"Belén"},
                        {"label":"Villa Hermosa", "value":"Villa Hermosa"},
                        {"label":"Castilla", "value":"Castilla"},
                        {"label":"Poblado", "value":"Poblado"},
                        {"label":"Candelaria", "value":"Candelaria"},
                        {"label":"Buenos Aires", "value":"Buenos Aires"},
                        {"label":"Santa Cruz", "value":"Santa Cruz"},
                        {"label":"Laureles", "value":"Laureles"},
                        {"label":"Doce de Octubre", "value":"Doce de Octubre"},
                        {"label":"Manrique", "value":"Manrique"},
                        {"label":"San Javier", "value":"San Javier"},
                        {"label":"San Antonio de Prado", "value":"San Antonio de Prado"},
                        {"label":"Popular", "value":"Popular"},
                        {"label":"Itagüí", "value":"Itagüí"},
                        {"label":"Sabaneta", "value":"Sabaneta"},
                        {"label":"Bello", "value":"Bello"},
                        {"label":"Envigado", "value":"Envigado"}
                    ],
                    value=['Aranjuez', 'Belén', 'Villa Hermosa', 'Castilla', 'Poblado',
                           'Candelaria','Buenos Aires', 'Santa Cruz', 'Laureles',
                           'Doce de Octubre', 'Manrique', 'San Javier', 'San Antonio de Prado',
                           'Popular', 'Itagüí', 'Sabaneta', 'Bello', 'Envigado'],
                    multi=True
                )
            ])
        ),
    dbc.Row(
        dbc.Col([
            dbc.Button([
                "Filtrar"
            ], id="id_filtrar")
        ], class_name="d-flex justify-content-end mt-2")
    ),
    dbc.Row([
        dbc.Col([
            html.Div([
                mapa1.display()
            ], id="mapa_hurtos")
        ]),
        dbc.Col([
            dbc.Row([
                    html.Div([
                pie1.display()
            ], id='pie_chart1'),
                ]),
            dbc.Row([
                html.Div([
                bar1.display()
            ], id='bar_chart1')
            ])
                
            ]),
        dbc.Col([
            dbc.Row([
                html.Div([
                    hist1.display()
                ], id='hist_chart1')
            ]),
            dbc.Row([
                html.Div([
                    line1.display()
                ], id='line_chart1')
            ])
        ])
            
        ]),
        

    ])


@callback(
    [Output("mapa_hurtos", "children"),
     Output("pie_chart1", "children"),
     Output("bar_chart1", "children"),
     Output("hist_chart1", "children"),
     Output("line_chart1", "children")],
    [State("id_selector_fecha", "start_date"),
     State("id_selector_fecha", "end_date"),
     State("id_selector_sexo", "value"),
     State("id_selector_transp", "value"),
     State("id_selector_comuna", "value"),
     Input("id_filtrar", "n_clicks")
    ], prevent_initial_call=True
)

def update_charts(start_date, end_date, sexo_, medio_transporte_, comuna_, n_clicks):
    mask_dfd = (
        (dfd.sexo.isin(list(sexo_))) &
        (dfd.medio_transporte.isin(list(medio_transporte_))) &
        (dfd.sede_receptora.isin(list(comuna_))) &
        (dfd.fecha_hecho >= start_date) &
        (dfd.fecha_hecho <= end_date) 
    )
    new_dfd = dfd.loc[mask_dfd, :]
    mapa1.df = new_dfd
    new_map = mapa1.display()
    pie1.df = new_dfd
    new_pie = pie1.display()
    bar1.df = new_dfd
    new_bar = bar1.display()
    hist1.df = new_dfd
    new_hist = hist1.display()
    line1.df = new_dfd
    new_line = line1.display()
    
    return [new_map, new_pie, new_bar, new_hist, new_line]