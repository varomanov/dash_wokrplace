from dash import html
import dash_bootstrap_components as dbc

def booking_layout():
    layout = html.Div([
        html.Div([
            html.Div(html.Img(src='assets/logo_servier_180x36.png')),
            html.P('Choose your name below:'),
            html.Div(dbc.Select(options=[12,3]))
        ])
    ], className='container-login w-75 border-1')

    return layout