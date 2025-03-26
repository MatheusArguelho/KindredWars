import pandas as pd
import plotly.express as px
from flask import Flask, render_template
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# ==============================================
# 1. CARREGAMENTO E PRÉ-PROCESSAMENTO DOS DADOS
# ==============================================

df = pd.read_csv('todos_os_decks.csv')
df = df[~df['Deck'].str.endswith('INVALIDO', na=False)]
df['Custo'] = pd.to_numeric(df['Custo'], errors='coerce')
df['Preco_USD'] = pd.to_numeric(df['Preco_USD'], errors='coerce')
df['EDHREC_Rank'] = pd.to_numeric(df['EDHREC_Rank'], errors='coerce')

# Filtra as cartas que não são do tipo "Land"
df_sem_land = df[df['Tipo'] != 'Basic Land']

# ==============================================
# 2. ANÁLISES ESTATÍSTICAS
# ==============================================

num_decks_distintos = df['Deck'].nunique()
comandantes_decks = df[df['Comandante'] == 1].groupby('Deck').first()
preco_por_deck = df.groupby('Deck')['Preco_USD'].sum().sort_values(ascending=False)
cores_comandantes = comandantes_decks['Cor'].value_counts()

# Cartas mais comuns entre decks (sem contar "Land")
cartas_comuns = df_sem_land.groupby('Nome')['Deck'].nunique().sort_values(ascending=False)

# Filtra os dados com base em tipos de cartas específicos
tipos = ['Land', 'Creature', 'Artifact', 'Enchantment', 'Planeswalker', 'Battle', 'Instant', 'Sorcery']

# Cria gráficos de barras para cada tipo
tipos_graficos = {}
top_x = 50  # Definindo o número de itens a serem mostrados nos gráficos (facilidade de alteração)

for tipo in tipos:
    tipo_cartas = df[df['Tipo'].str.contains(tipo, case=False, na=False)]
    tipo_comum = tipo_cartas.groupby('Nome')['Deck'].nunique().sort_values(ascending=False)

    fig = px.bar(tipo_comum.head(top_x),  # Usando top_x para definir o número de itens
                 x=tipo_comum.head(top_x).index,
                 y=tipo_comum.head(top_x).values,
                 title=f"Top {top_x} Cartas do Tipo {tipo}",
                 labels={'x': 'Carta', 'y': 'Número de Decks'},
                 template='plotly')

    fig.update_layout(
        autosize=True,
        margin=dict(l=10, r=10, t=40, b=40)
    )

    tipos_graficos[tipo] = fig.to_html(full_html=False)

# ==============================================
# 3. CRIAÇÃO DO FLASK COM PLOTLY
# ==============================================

app = Flask(__name__)

# Configuração do Dash integrado com Flask
dash_app = dash.Dash(__name__, server=app, url_base_pathname='/dashboard/')

# Definindo o layout do Dash
dash_app.layout = html.Div([
    # Filtro de tipo
    dcc.Dropdown(
        id='tipo-dropdown',
        options=[{'label': tipo, 'value': tipo} for tipo in tipos],
        value=tipos[0],  # Valor padrão
        style={'width': '50%'}
    ),

    # Filtro de cor (dropdown com WUBRG)
    dcc.Dropdown(
        id='cor-dropdown',
        options=[
            {'label': 'White', 'value': 'W'},
            {'label': 'Blue', 'value': 'U'},
            {'label': 'Black', 'value': 'B'},
            {'label': 'Red', 'value': 'R'},
            {'label': 'Green', 'value': 'G'}
        ],
        multi=True,  # Permite a seleção de múltiplas cores
        value=None,  # Valor padrão (todas as cores)
        style={'width': '50%', 'margin-top': '20px'}
    ),

    # Gráfico
    dcc.Graph(id='graph')
])


# Callback para atualizar o gráfico com base na seleção do dropdown de tipo e cores
@dash_app.callback(
    Output('graph', 'figure'),
    [Input('tipo-dropdown', 'value'),
     Input('cor-dropdown', 'value')]
)
def update_graph(tipo, cores):
    # Filtra os dados com base no tipo
    tipo_comum = df[df['Tipo'].str.contains(tipo, case=False, na=False)]

    # Filtra os dados com base nas cores selecionadas (verifica se a string de cores contém todas as cores selecionadas)
    if cores:
        tipo_comum = tipo_comum[tipo_comum['Cor'].apply(lambda x: all(cor in x for cor in cores))]

    # Recalcula as cartas mais comuns após os filtros
    tipo_comum = tipo_comum.groupby('Nome')['Deck'].nunique().sort_values(ascending=False)

    fig = px.bar(tipo_comum.head(top_x),  # Usando top_x para definir o número de itens
                 x=tipo_comum.head(top_x).index,
                 y=tipo_comum.head(top_x).values,
                 title=f"Top {top_x} Cartas do Tipo {tipo}",
                 labels={'x': 'Carta', 'y': 'Número de Decks'},
                 template='plotly')

    fig.update_layout(
        autosize=True,
        margin=dict(l=10, r=10, t=40, b=40)
    )
    return fig


# Rota para a página principal do Flask
@app.route('/')
def index():
    # Gráfico de barras: Top X Decks Mais Caros
    fig_preco_decks = px.bar(preco_por_deck.head(top_x),  # Usando top_x para definir o número de itens
                             x=preco_por_deck.head(top_x).index,
                             y=preco_por_deck.head(top_x).values,
                             title=f"Top {top_x} Decks Mais Caros",
                             labels={'x': 'Deck', 'y': 'Preço Total (USD)'},
                             template='plotly')

    # Gráfico de pizza: Distribuição de Cores nos Comandantes
    fig_cores_comandantes = px.pie(cores_comandantes,
                                   names=cores_comandantes.index,
                                   values=cores_comandantes.values,
                                   title="Distribuição de Cores nos Comandantes",
                                   template='plotly')

    # Gráfico de barras: Top X Cartas Mais Comuns Entre Decks (Sem 'Land')
    fig_cartas_comuns = px.bar(cartas_comuns.head(top_x),  # Usando top_x para definir o número de itens
                               x=cartas_comuns.head(top_x).index,
                               y=cartas_comuns.head(top_x).values,
                               title=f"Top {top_x} Cartas Mais Comuns Entre Decks (Sem 'Land')",
                               labels={'x': 'Carta', 'y': 'Número de Decks'},
                               template='plotly')

    # Converte os gráficos para HTML
    graph_preco_decks = fig_preco_decks.to_html(full_html=False)
    graph_cores_comandantes = fig_cores_comandantes.to_html(full_html=False)
    graph_cartas_comuns = fig_cartas_comuns.to_html(full_html=False)

    # Criação dos gráficos para os tipos de carta
    tipo_graphs = {tipo: tipos_graficos[tipo] for tipo in tipos}

    # Passa as variáveis para o template HTML
    return render_template('index.html',
                           num_decks_distintos=num_decks_distintos,
                           graph_preco_decks=graph_preco_decks,
                           graph_cores_comandantes=graph_cores_comandantes,
                           graph_cartas_comuns=graph_cartas_comuns,
                           tipo_graphs=tipo_graphs,
                           top_x=top_x)  # Passa a variável top_x para o HTML, se precisar para referência


if __name__ == '__main__':
    app.run(debug=True)
