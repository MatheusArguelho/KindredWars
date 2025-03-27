import plotly.express as px
import plotly.graph_objects as go


def create_empty_plot(message):
    """Cria um gráfico vazio com uma mensagem."""
    fig = go.Figure()
    fig.update_layout(
        xaxis={'visible': False},
        yaxis={'visible': False},
        annotations=[{
            'text': message,
            'xref': 'paper',
            'yref': 'paper',
            'showarrow': False,
            'font': {'size': 16}
        }]
    )
    return fig


def create_plots(analysis_results, tipos, top_x=50):
    """Cria gráficos Plotly a partir dos resultados das análises."""
    plots = {}

    # 1. Gráfico de preço por deck
    if not analysis_results['preco_por_deck'].empty:
        plots['preco_decks'] = px.bar(
            analysis_results['preco_por_deck'].head(top_x),
            x=analysis_results['preco_por_deck'].head(top_x).index,
            y=analysis_results['preco_por_deck'].head(top_x).values,
            title=f"Top {top_x} Decks Mais Caros (Preço Total)",
            labels={'x': 'Deck', 'y': 'Preço (USD)'},
            template='plotly_white',
            color=analysis_results['preco_por_deck'].head(top_x).values,
            color_continuous_scale='Viridis'
        )
        plots['preco_decks'].update_layout(
            hovermode='closest',
            showlegend=False,
            coloraxis_showscale=False
        )
    else:
        plots['preco_decks'] = create_empty_plot("Nenhum dado de preço disponível")

    # 2. Gráfico de distribuição de cores
    if not analysis_results['cores_comandantes'].empty:
        color_map = {
            'W': '#FFF9A6',  # White
            'U': '#7EB5FF',  # Blue
            'B': '#000000',  # Black
            'R': '#FF5757',  # Red
            'G': '#4CAF50'  # Green
        }

        plots['cores_comandantes'] = px.pie(
            analysis_results['cores_comandantes'],
            names=analysis_results['cores_comandantes'].index,
            values=analysis_results['cores_comandantes'].values,
            title="Distribuição de Cores nos Comandantes",
            template='plotly_white',
            color=analysis_results['cores_comandantes'].index,
            color_discrete_map=color_map
        )
        plots['cores_comandantes'].update_traces(
            textposition='inside',
            textinfo='percent+label'
        )
    else:
        plots['cores_comandantes'] = create_empty_plot("Nenhum dado de cores disponível")

    # 3. Gráfico de EDHREC Rank
    if not analysis_results['edhrec_rank_por_deck'].empty:
        plots['edhrec_rank_decks'] = px.bar(
            analysis_results['edhrec_rank_por_deck'].head(top_x),
            x=analysis_results['edhrec_rank_por_deck'].head(top_x).index,
            y=analysis_results['edhrec_rank_por_deck'].head(top_x).values,
            title=f"Top {top_x} Decks por Popularidade (EDHREC Rank)",
            labels={'x': 'Deck', 'y': 'Pontuação (Rank/100)'},
            template='plotly_white',
            color=analysis_results['edhrec_rank_por_deck'].head(top_x).values,
            color_continuous_scale='Plasma'
        )
        plots['edhrec_rank_decks'].update_layout(
            hovermode='closest',
            showlegend=False,
            coloraxis_showscale=False
        )
    else:
        plots['edhrec_rank_decks'] = create_empty_plot("Nenhum dado de rank disponível")

    # 4. Gráfico de cartas mais comuns
    if not analysis_results['cartas_comuns'].empty:
        plots['cartas_comuns'] = px.bar(
            analysis_results['cartas_comuns'].head(top_x),
            x=analysis_results['cartas_comuns'].head(top_x).index,
            y=analysis_results['cartas_comuns'].head(top_x).values,
            title=f"Top {top_x} Cartas Mais Comuns (Exceto Lands)",
            labels={'x': 'Carta', 'y': 'Número de Decks'},
            template='plotly_white',
            color=analysis_results['cartas_comuns'].head(top_x).values,
            color_continuous_scale='Turbo'
        )
        plots['cartas_comuns'].update_layout(
            hovermode='closest',
            showlegend=False,
            coloraxis_showscale=False,
            xaxis_tickangle=-45
        )
    else:
        plots['cartas_comuns'] = create_empty_plot("Nenhum dado de cartas comuns disponível")

    # 5. Gráficos por tipo de carta
    plots['tipos'] = {}
    for tipo in tipos:
        if tipo in analysis_results['cartas_por_tipo'] and not analysis_results['cartas_por_tipo'][tipo].empty:
            plots['tipos'][tipo] = px.bar(
                analysis_results['cartas_por_tipo'][tipo].head(top_x),
                x=analysis_results['cartas_por_tipo'][tipo].head(top_x).index,
                y=analysis_results['cartas_por_tipo'][tipo].head(top_x).values,
                title=f"Top {top_x} Cartas do Tipo {tipo}",
                labels={'x': 'Carta', 'y': 'Número de Decks'},
                template='plotly_white',
                color=analysis_results['cartas_por_tipo'][tipo].head(top_x).values,
                color_continuous_scale='Rainbow'
            )
            plots['tipos'][tipo].update_layout(
                hovermode='closest',
                showlegend=False,
                coloraxis_showscale=False,
                xaxis_tickangle=-90
            )
        else:
            plots['tipos'][tipo] = create_empty_plot(f"Nenhum dado disponível para {tipo}")

    return plots