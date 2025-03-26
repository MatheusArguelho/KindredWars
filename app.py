import pandas as pd
import plotly.express as px
from flask import Flask, render_template

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
for tipo in tipos:
    tipo_cartas = df[df['Tipo'].str.contains(tipo, case=False, na=False)]
    tipo_comum = tipo_cartas.groupby('Nome')['Deck'].nunique().sort_values(ascending=False)

    fig = px.bar(tipo_comum.head(10),
                 x=tipo_comum.head(10).index,
                 y=tipo_comum.head(10).values,
                 title=f"Top 10 Cartas do Tipo {tipo}",
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


@app.route('/')
def index():
    # Gráfico de barras: Top 10 Decks Mais Caros
    fig_preco_decks = px.bar(preco_por_deck.head(10),
                             x=preco_por_deck.head(10).index,
                             y=preco_por_deck.head(10).values,
                             title="Top 10 Decks Mais Caros",
                             labels={'x': 'Deck', 'y': 'Preço Total (USD)'},
                             template='plotly')

    # Gráfico de pizza: Distribuição de Cores nos Comandantes
    fig_cores_comandantes = px.pie(cores_comandantes,
                                   names=cores_comandantes.index,
                                   values=cores_comandantes.values,
                                   title="Distribuição de Cores nos Comandantes",
                                   template='plotly')

    # Gráfico de barras: Top 10 Cartas Mais Comuns Entre Decks (Sem 'Land')
    fig_cartas_comuns = px.bar(cartas_comuns.head(10),
                               x=cartas_comuns.head(10).index,
                               y=cartas_comuns.head(10).values,
                               title="Top 10 Cartas Mais Comuns Entre Decks (Sem 'Land')",
                               labels={'x': 'Carta', 'y': 'Número de Decks'},
                               template='plotly')

    # Converte os gráficos para HTML
    graph_preco_decks = fig_preco_decks.to_html(full_html=False)
    graph_cores_comandantes = fig_cores_comandantes.to_html(full_html=False)
    graph_cartas_comuns = fig_cartas_comuns.to_html(full_html=False)

    # Criação dos gráficos para os tipos de carta
    tipo_graphs = {tipo: tipos_graficos[tipo] for tipo in tipos}

    return render_template('index.html',
                           num_decks_distintos=num_decks_distintos,
                           graph_preco_decks=graph_preco_decks,
                           graph_cores_comandantes=graph_cores_comandantes,
                           graph_cartas_comuns=graph_cartas_comuns,
                           tipo_graphs=tipo_graphs)


if __name__ == '__main__':
    app.run(debug=True)
