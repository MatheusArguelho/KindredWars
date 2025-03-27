import plotly.express as px
import plotly.graph_objects as go


def create_empty_plot(mensagem):
    """
    Cria um gráfico vazio com uma mensagem explicativa.

    Parâmetros:
        mensagem (str): Texto a ser exibido no gráfico vazio

    Retorna:
        go.Figure: Objeto de figura Plotly com a mensagem
    """
    fig = go.Figure()
    fig.add_annotation(
        text=mensagem,
        xref="paper", yref="paper",
        x=0.5, y=0.5,
        showarrow=False,
        font=dict(size=16)
    )
    fig.update_layout(
        xaxis={"visible": False},
        yaxis={"visible": False},
        plot_bgcolor="white"
    )
    return fig


def create_plots(analysis_results, tipos, top_x=50):
    """
    Cria todos os gráficos Plotly a partir dos dados analisados.

    Parâmetros:
        analysis_results (dict): Dicionário com os resultados das análises
        tipos (list): Lista de tipos de cartas a serem analisados
        top_x (int): Número de itens a mostrar em cada gráfico

    Retorna:
        dict: Dicionário com todos os gráficos gerados
    """
    plots = {
        'tipos': {}  # Dicionário para armazenar gráficos por tipo
    }

    # Configurações de layout comuns para todos os gráficos
    config_layout = {
        'margin': {'l': 50, 'r': 50, 'b': 150, 't': 50, 'pad': 4},
        'xaxis': {
            'tickangle': -45,
            'automargin': True,
            'tickfont': {'size': 10},
            'title': {'standoff': 15}
        },
        'yaxis': {
            'automargin': True,
            'title': {'standoff': 15}
        },
        'autosize': True,
        'hovermode': 'x unified'
    }

    # ==============================================
    # 1. GRÁFICO: TOP DECKS MAIS CAROS
    # ==============================================
    if not analysis_results['preco_por_deck'].empty:
        plots['preco_decks'] = px.bar(
            x=analysis_results['preco_por_deck'].head(top_x).index,
            y=analysis_results['preco_por_deck'].head(top_x).values,
            title=f"Top {top_x} Decks Mais Caros (Preço Total)",
            labels={'x': 'Deck', 'y': 'Preço (USD)'},
            template='plotly_white'
        )
        plots['preco_decks'].update_layout(config_layout)
    else:
        plots['preco_decks'] = create_empty_plot("Dados de preço não disponíveis")

    # ==============================================
    # 2. GRÁFICO: DISTRIBUIÇÃO DE CORES
    # ==============================================
    if not analysis_results['cores_comandantes'].empty:
        # Mapeamento de cores para as identidades de cor do Magic
        color_map = {
            'W': '#FFF9A6',  # Branco
            'U': '#7EB5FF',  # Azul
            'B': '#000000',  # Preto
            'R': '#FF5757',  # Vermelho
            'G': '#4CAF50',  # Verde
            # Combinações de cores:
            'WU': '#B3E5FC', 'WB': '#9E9E9E', 'WR': '#FFAB91',
            'WG': '#C8E6C9', 'UB': '#7986CB', 'UR': '#B39DDB',
            'UG': '#80CBC4', 'BR': '#8D6E63', 'BG': '#689F38',
            'RG': '#FBC02D', 'GW': '#DCEDC8', 'GU': '#B2EBF2',
            'GR': '#FFCC80', 'RW': '#FFCDD2', 'RU': '#90CAF9',
            'BG': '#8BC34A', 'BUG': '#009688', 'BRG': '#795548',
            'GRW': '#FFA000', 'RWU': '#E91E63', 'WUB': '#3F51B5',
            'BGR': '#4E342E', 'GUW': '#4DB6AC', 'WUR': '#F06292',
            'BGRUW': '#5D4037'  # 5 cores
        }

        plots['cores_comandantes'] = px.pie(
            names=analysis_results['cores_comandantes'].index,
            values=analysis_results['cores_comandantes'].values,
            title="Distribuição de Cores nos Comandantes",
            template='plotly_white',
            color=analysis_results['cores_comandantes'].index,
            color_discrete_map=color_map
        )
        plots['cores_comandantes'].update_traces(
            textposition='inside',
            textinfo='percent+label',
            marker={'line': {'color': '#ffffff', 'width': 1}}
        )
    else:
        plots['cores_comandantes'] = create_empty_plot("Dados de cores não disponíveis")

    # ==============================================
    # 3. GRÁFICO: POPULARIDADE DOS DECKS (EDHREC RANK)
    # ==============================================
    if not analysis_results['edhrec_rank_por_deck'].empty:
        plots['edhrec_rank_decks'] = px.bar(
            x=analysis_results['edhrec_rank_por_deck'].head(top_x).index,
            y=analysis_results['edhrec_rank_por_deck'].head(top_x).values,
            title=f"Top {top_x} Decks por Popularidade (EDHREC Rank)",
            labels={'x': 'Deck', 'y': 'Pontuação (Rank/100)'},
            template='plotly_white'
        )
        plots['edhrec_rank_decks'].update_layout(config_layout)
    else:
        plots['edhrec_rank_decks'] = create_empty_plot("Dados de rank não disponíveis")

    # ==============================================
    # 4. GRÁFICO: CARTAS MAIS COMUNS (EXCETO LANDS)
    # ==============================================
    if not analysis_results['cartas_comuns'].empty:
        plots['cartas_comuns'] = px.bar(
            x=analysis_results['cartas_comuns'].head(top_x).index,
            y=analysis_results['cartas_comuns'].head(top_x).values,
            title=f"Top {top_x} Cartas Mais Comuns (Exceto Lands)",
            labels={'x': 'Carta', 'y': 'Número de Decks'},
            template='plotly_white'
        )
        plots['cartas_comuns'].update_layout(config_layout)
    else:
        plots['cartas_comuns'] = create_empty_plot("Dados de cartas comuns não disponíveis")

    # ==============================================
    # 5. GRÁFICOS POR TIPO DE CARTA
    # ==============================================
    if 'cartas_por_tipo' in analysis_results:
        for tipo in tipos:
            if tipo in analysis_results['cartas_por_tipo']:
                tipo_data = analysis_results['cartas_por_tipo'][tipo]
                if not tipo_data.empty:
                    fig = px.bar(
                        x=tipo_data.head(top_x).index,
                        y=tipo_data.head(top_x).values,
                        title=f"Top {top_x} Cartas do Tipo {tipo}",
                        labels={'x': 'Carta', 'y': 'Número de Decks'},
                        template='plotly_white'
                    )

                    # Configurações específicas para gráficos por tipo
                    fig.update_layout(config_layout)
                    fig.update_traces(width=0.7)  # Largura das barras

                    plots['tipos'][tipo] = fig
                else:
                    plots['tipos'][tipo] = create_empty_plot(f"Nenhum dado disponível para {tipo}")
            else:
                plots['tipos'][tipo] = create_empty_plot(f"Tipo {tipo} não encontrado nos dados")

    return plots