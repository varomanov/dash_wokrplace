from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc

def booking_layout(user):
    layout = html.Div([
        html.Div([
            html.Div(html.Img(src='assets/logo_servier_180x36.png', width=80))
        ], className='align-self-start'),
        html.H1(f'Hello! {user}'),
    ])

    return layout