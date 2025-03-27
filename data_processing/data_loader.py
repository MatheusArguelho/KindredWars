import pandas as pd


def load_and_preprocess_data(filepath):
    """Carrega e pré-processa os dados do arquivo CSV."""
    df = pd.read_csv(filepath)

    # Filtra decks inválidos
    df = df[~df['Deck'].str.endswith('INVALIDO', na=False)]

    # Converte colunas numéricas
    df['Custo'] = pd.to_numeric(df['Custo'], errors='coerce')
    df['Preco_USD'] = pd.to_numeric(df['Preco_USD'], errors='coerce')
    df['EDHREC_Rank'] = pd.to_numeric(df['EDHREC_Rank'], errors='coerce')

    # Filtra cartas que não são do tipo "Land"
    df_sem_land = df[df['Tipo'] != 'Basic Land']

    return df, df_sem_land