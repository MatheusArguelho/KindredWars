from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import dash
import pandas as pd


def create_dash_app(server, df, tipos):
    """Cria e configura a aplicação Dash."""
    dash_app = dash.Dash(__name__, server=server, url_base_pathname='/dashboard/')

    dash_app.layout = html.Div([
        dcc.Dropdown(
            id='tipo-dropdown',
            options=[{'label': tipo, 'value': tipo} for tipo in tipos],
            value=tipos[0],
            style={'width': '50%'}
        ),
        dcc.Dropdown(
            id='cor-dropdown',
            options=[
                {'label': 'White', 'value': 'W'},
                {'label': 'Blue', 'value': 'U'},
                {'label': 'Black', 'value': 'B'},
                {'label': 'Red', 'value': 'R'},
                {'label': 'Green', 'value': 'G'}
            ],
            multi=True,
            value=None,
            style={'width': '50%', 'margin-top': '20px'}
        ),
        dcc.Graph(id='graph')
    ])

    @dash_app.callback(
        Output('graph', 'figure'),
        [Input('tipo-dropdown', 'value'),
         Input('cor-dropdown', 'value')]
    )
    def update_graph(tipo, cores):
        tipo_comum = df[df['Tipo'].str.contains(tipo, case=False, na=False)]

        if cores:
            tipo_comum = tipo_comum[tipo_comum['Cor'].apply(lambda x: all(cor in x for cor in cores))]

        tipo_comum = tipo_comum.groupby('Nome')['Deck'].nunique().sort_values(ascending=False)

        fig = px.bar(
            tipo_comum.head(50),
            x=tipo_comum.head(50).index,
            y=tipo_comum.head(50).values,
            title=f"Top 50 Cartas do Tipo {tipo}",
            labels={'x': 'Carta', 'y': 'Número de Decks'},
            template='plotly'
        )

        fig.update_layout(
            autosize=True,
            margin=dict(l=10, r=10, t=40, b=40)
        )

        return fig

    return dash_app