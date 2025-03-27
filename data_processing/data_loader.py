import pandas as pd


def load_and_preprocess_data(filepath):
    """Carrega e pré-processa os dados do arquivo CSV."""
    try:
        df = pd.read_csv(filepath)

        # Verifica colunas existentes (debug)
        #print("\nColunas disponíveis no CSV:", df.columns.tolist())

        # Padroniza nomes de colunas (case insensitive)
        df.columns = df.columns.str.strip().str.lower()

        # Renomeia colunas para nomes esperados
        column_mapping = {
            'preco_usd': 'preco_usd',
            'edhrec_rank': 'edhrec_rank',
            'deck': 'deck',
            'comandante': 'comandante',
            'cor': 'cor',
            'tipo': 'tipo',
            'nome': 'nome'
        }

        # Aplica o mapeamento de colunas
        for original, new in column_mapping.items():
            if original in df.columns:
                df.rename(columns={original: new}, inplace=True)

        # Filtra decks inválidos
        df = df[~df['deck'].str.endswith('INVALIDO', na=False)]

        # Converte colunas numéricas
        df['preco_usd'] = pd.to_numeric(df['preco_usd'], errors='coerce').fillna(0)
        df['edhrec_rank'] = pd.to_numeric(df['edhrec_rank'], errors='coerce').fillna(0)

        # Debug: mostra amostra dos dados
        #print("\nAmostra dos dados carregados:")
        #print(df[['deck', 'preco_usd', 'edhrec_rank', 'cor']].head())

        # Filtra cartas que não são do tipo "Land"
        df_sem_land = df[~df['tipo'].str.contains('land', case=False, na=False)]

        return df, df_sem_land

    except Exception as e:
        print(f"Erro ao carregar dados: {str(e)}")
        raise