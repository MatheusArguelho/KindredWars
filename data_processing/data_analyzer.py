import pandas as pd


def analyze_data(df, df_sem_land, tipos):
    """Realiza análises estatísticas sobre os dados."""
    try:
        # Debug: verifica valores únicos nas colunas críticas
        print("\nValores únicos em 'cor':", df['cor'].unique())
        print("Valores únicos em 'comandante':", df['comandante'].unique())

        # Número de decks distintos
        num_decks_distintos = df['deck'].nunique()

        # Comandantes
        comandantes_decks = df[df['comandante'] == 1].groupby('deck').first()

        # Preço por deck
        preco_por_deck = df.groupby('deck')['preco_usd'].sum().sort_values(ascending=False)

        # Cores dos comandantes
        cores_comandantes = comandantes_decks['cor'].value_counts()

        # Cartas mais comuns (sem lands)
        cartas_comuns = df_sem_land.groupby('nome')['deck'].nunique().sort_values(ascending=False)

        # EDHREC Rank por deck
        edhrec_rank_por_deck = df.groupby('deck')['edhrec_rank'].sum() / 100
        edhrec_rank_por_deck = edhrec_rank_por_deck.sort_values(ascending=False)

        # Cartas por tipo
        cartas_por_tipo = {}
        for tipo in tipos:
            tipo_cartas = df[df['tipo'].str.contains(tipo, case=False, na=False)]
            cartas_por_tipo[tipo] = tipo_cartas.groupby('nome')['deck'].nunique().sort_values(ascending=False)

        return {
            'num_decks_distintos': num_decks_distintos,
            'preco_por_deck': preco_por_deck,
            'cores_comandantes': cores_comandantes,
            'cartas_comuns': cartas_comuns,
            'edhrec_rank_por_deck': edhrec_rank_por_deck,
            'cartas_por_tipo': cartas_por_tipo
        }

    except Exception as e:
        print(f"Erro na análise de dados: {str(e)}")
        raise