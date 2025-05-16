from flask import Flask, render_template
from flask_caching import Cache
import pandas as pd
from data_processing.data_loader import load_and_preprocess_data
from data_processing.data_analyzer import analyze_data
from visualization.plot_creator import create_plots, create_empty_plot
from visualization.dashboard import create_dash_app
import logging
from logging.handlers import RotatingFileHandler

# Configuração inicial
app = Flask(__name__)
app.config['CACHE_TYPE'] = 'simple'
cache = Cache(app)

# Configuração de logging
handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)

tipos = ['Land', 'Creature', 'Artifact', 'Enchantment', 'Planeswalker', 'Battle', 'Instant', 'Sorcery']
top_x = 50

try:
    # Carrega e processa dados
    df, df_sem_land = load_and_preprocess_data('todos_os_decks.csv')
    
    # Análise dos dados
    analysis_results = analyze_data(df, df_sem_land, tipos)
    
    # Cria gráficos
    plots = create_plots(analysis_results, tipos, top_x)
    
    # Configura o Dash
    dash_app = create_dash_app(app, df, tipos)
except Exception as e:
    app.logger.error(f"Erro na inicialização: {str(e)}")
    df = pd.DataFrame()
    df_sem_land = pd.DataFrame()
    analysis_results = {'num_decks_distintos': 0}
    plots = {}

@cache.cached(timeout=300)  # Cache por 5 minutos
@app.route('/')
def index():
    try:
        if df.empty:
            return render_template('error.html', 
                                 error_message="Erro ao carregar dados. Por favor, tente novamente mais tarde.")
        
        # Converte os gráficos para HTML
        graph_html = {
            'graph_preco_decks': plots['preco_decks'].to_html(full_html=False, include_plotlyjs='cdn'),
            'graph_cores_comandantes': plots['cores_comandantes'].to_html(full_html=False, include_plotlyjs='cdn'),
            'graph_edhrec_rank_decks': plots['edhrec_rank_decks'].to_html(full_html=False, include_plotlyjs='cdn'),
            'graph_cartas_comuns': plots['cartas_comuns'].to_html(full_html=False, include_plotlyjs='cdn'),
        }

        # Adiciona gráficos por tipo se existirem
        if 'tipos' in plots:
            graph_html['tipo_graphs'] = {
                tipo: plots['tipos'][tipo].to_html(full_html=False, include_plotlyjs='cdn')
                for tipo in tipos if tipo in plots['tipos']
            }
        else:
            graph_html['tipo_graphs'] = {
                tipo: create_empty_plot(f"Dados não disponíveis para {tipo}").to_html(full_html=False,
                                                                                      include_plotlyjs='cdn')
                for tipo in tipos
            }

        return render_template('index.html',
                               num_decks_distintos=analysis_results['num_decks_distintos'],
                               **graph_html,
                               top_x=top_x)
    except Exception as e:
        app.logger.error(f"Erro na rota index: {str(e)}")
        return render_template('error.html', 
                             error_message="Ocorreu um erro ao processar sua solicitação.")

if __name__ == '__main__':
    app.run(debug=True)