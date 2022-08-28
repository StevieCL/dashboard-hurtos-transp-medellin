import dash
from dash import Dash, html, dcc, dash_table, Input, Output, State, MATCH, ALL
import dash_labs as dl
from dash_labs.plugins import register_page
import dash_bootstrap_components as dbc
from callbacks import register_callbacks


app = Dash(__name__, plugins=[dl.plugins.pages], external_stylesheets=[dbc.themes.LUX])
app.config.suppress_callback_exceptions=True

navbar = dbc.NavbarSimple([
    dbc.NavItem(dbc.NavLink('Dashboard', href='dashboard')),
    dbc.NavItem(dbc.NavLink('Resumen', href='#'))],
    brand="Hurtos en Medellín",
    color='primary',
    dark=True,
    className='mb-2'
    )

app.layout = dbc.Container(
    [
        navbar,
        dl.plugins.page_container
    ],
    className='dbc',
    fluid=True
)

register_callbacks(app)
server = app.server

if __name__ == "__main__":
    app.run_server(port=8050, debug=True)