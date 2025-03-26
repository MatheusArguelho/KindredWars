import pandas as pd
import plotly.express as px
from flask import Flask, render_template

# ==============================================
# 1. CARREGAMENTO E PRÉ-PROCESSAMENTO DOS DADOS
# ==============================================

# Carrega o arquivo CSV contendo os dados dos decks
df = pd.read_csv('todos_os_decks.csv')

# Remove linhas onde a coluna 'Deck' termina com "INVALIDO"
df = df[~df['Deck'].str.endswith('INVALIDO', na=False)]

# Converte colunas numéricas, tratando erros como NaN
df['Custo'] = pd.to_numeric(df['Custo'], errors='coerce')
df['Preco_USD'] = pd.to_numeric(df['Preco_USD'], errors='coerce')
df['EDHREC_Rank'] = pd.to_numeric(df['EDHREC_Rank'], errors='coerce')

# ==============================================
# 2. ANÁLISES ESTATÍSTICAS
# ==============================================

# Número de decks distintos
num_decks_distintos = df['Deck'].nunique()

# Número médio de cartas por deck
media_cartas_por_deck = df.groupby('Deck')['Nome'].count().mean()

# Comandantes de cada deck
comandantes_decks = df[df['Comandante'] == 1].groupby('Deck').first()

# Preço total de cada deck
preco_por_deck = df.groupby('Deck')['Preco_USD'].sum().sort_values(ascending=False)

# Cores mais populares nos comandantes
cores_comandantes = comandantes_decks['Cor'].value_counts()

# Cartas que aparecem no maior número de decks diferentes
cartas_comuns = df.groupby('Nome')['Deck'].nunique().sort_values(ascending=False)

# ==============================================
# 3. CRIAÇÃO DO FLASK COM PLOTLY
# ==============================================

# Inicializa o aplicativo Flask
app = Flask(__name__)

# Rota principal
@app.route('/')
def index():
    # Criação dos gráficos
    fig_preco_decks = px.bar(preco_por_deck.head(10),
                             x=preco_por_deck.head(10).index,
                             y=preco_por_deck.head(10).values,
                             title="Top 10 Decks Mais Caros",
                             labels={'x': 'Deck', 'y': 'Preço Total (USD)'},
                             template='plotly_dark')

    fig_cores_comandantes = px.pie(cores_comandantes,
                                   names=cores_comandantes.index,
                                   values=cores_comandantes.values,
                                   title="Distribuição de Cores nos Comandantes",
                                   template='plotly_dark')

    fig_cartas_comuns = px.bar(cartas_comuns.head(10),
                               x=cartas_comuns.head(10).index,
                               y=cartas_comuns.head(10).values,
                               title="Top 10 Cartas Mais Comuns Entre Decks",
                               labels={'x': 'Carta', 'y': 'Número de Decks'},
                               template='plotly_dark')

    # Converte os gráficos para HTML
    graph_preco_decks = fig_preco_decks.to_html(full_html=False)
    graph_cores_comandantes = fig_cores_comandantes.to_html(full_html=False)
    graph_cartas_comuns = fig_cartas_comuns.to_html(full_html=False)

    # Renderiza o template HTML com os gráficos
    return render_template('index.html',
                           num_decks_distintos=num_decks_distintos,
                           media_cartas_por_deck="{:.2f}".format(media_cartas_por_deck),
                           graph_preco_decks=graph_preco_decks,
                           graph_cores_comandantes=graph_cores_comandantes,
                           graph_cartas_comuns=graph_cartas_comuns)

# Executa o servidor
if __name__ == '__main__':
    app.run(debug=True)
