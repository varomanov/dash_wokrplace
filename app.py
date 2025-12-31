from dash import Dash, html, callback, dcc, Input, Output, State, no_update
import dash_bootstrap_components as dbc
from models.models import get_users
from views import booking 

app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

app.layout = html.Div([
    dcc.Store(id='username', data={}),
    dcc.Location(id='loc'),
    html.Div(
        id='content', 
        children=[
            html.Div([
                html.Div(html.Img(src='assets/logo_servier_180x36.png')),
                html.H4('Workplace booking system', className='mb-5 mt-2 pb-5', style={'fontFamily': 'fantasy'}),
                html.H5('Select your name:', className='text-start pb-3'),
                html.Div(
                    dbc.Select(id='username_input', 
                               options=[{'label': '👤 ' + person.upper(), 'value': person} for person in get_users()]),
                    className='p-2 rounded-3',
                    style={'backgroundColor': 'orangered'}
                ),
                dbc.Button(id='btn-enter', children='Enter', className='px-5 py-2', style={'marginTop': '100px'}, disabled=True),
            ], className='login-container')
        ], className='vh-100',
    )
], className='container')

# Наполнение при входе
@callback(
    Output('btn-enter', 'disabled'),
    Output('username', 'data'),
    Input('username_input', 'value'),
    prevent_initial_call=True
)
def activate_button(value):
    if not value is None:
        return False, {'username': value}

@callback(
    Output('content', 'children'),
    State('username', 'data'),
    Input('btn-enter', 'n_clicks'),
    prevent_initial_call=True
)
def start_page(username, clicks):
    if clicks is None:
        no_update
    if clicks > 0:
        return booking.booking_layout(username['username'])

if __name__ == '__main__':
    app.run(debug=True)