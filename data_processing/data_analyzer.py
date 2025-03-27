import pandas as pd

def analyze_data(df, df_sem_land, tipos):
    """Realiza análises estatísticas sobre os dados."""
    # Garantir que os dados numéricos estão corretos
    df['Preco_USD'] = pd.to_numeric(df['Preco_USD'], errors='coerce').fillna(0)
    df['EDHREC_Rank'] = pd.to_numeric(df['EDHREC_Rank'], errors='coerce').fillna(0)

    # Número de decks distintos
    num_decks_distintos = df['Deck'].nunique()

    # Comandantes - garantir que temos dados
    comandantes_decks = df[df['Comandante'] == 1].groupby('Deck').first()
    cores_comandantes = comandantes_decks['Cor'].value_counts()

    # Preço por deck - remover zeros e ordenar
    preco_por_deck = df.groupby('Deck')['Preco_USD'].sum()
    preco_por_deck = preco_por_deck[preco_por_deck > 0].sort_values(ascending=False)

    # Cartas mais comuns (sem lands)
    cartas_comuns = df_sem_land.groupby('Nome')['Deck'].nunique().sort_values(ascending=False)

    # EDHREC Rank por deck - remover zeros e ordenar
    edhrec_rank_por_deck = df.groupby('Deck')['EDHREC_Rank'].sum() / 100
    edhrec_rank_por_deck = edhrec_rank_por_deck[edhrec_rank_por_deck > 0].sort_values(ascending=False)

    # Cartas por tipo
    cartas_por_tipo = {}
    for tipo in tipos:
        tipo_cartas = df[df['Tipo'].str.contains(tipo, case=False, na=False)]
        cartas_por_tipo[tipo] = tipo_cartas.groupby('Nome')['Deck'].nunique().sort_values(ascending=False)

    return {
        'num_decks_distintos': num_decks_distintos,
        'preco_por_deck': preco_por_deck,
        'cores_comandantes': cores_comandantes,
        'cartas_comuns': cartas_comuns,
        'edhrec_rank_por_deck': edhrec_rank_por_deck,
        'cartas_por_tipo': cartas_por_tipo
    }