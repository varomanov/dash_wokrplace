from dash import Dash, html, callback, dcc, Input, Output, State, no_update
import dash_bootstrap_components as dbc
from views.booking import booking_layout

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(
    id='main-container',
    className='main-container', 
    children=[
        dcc.Location(id='loc'),
        dcc.Store(id='store'),
        booking_layout()
    ]
)


if __name__ == '__main__':
    app.run(debug=True)