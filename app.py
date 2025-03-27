from flask import Flask, render_template
from data_processing.data_loader import load_and_preprocess_data
from data_processing.data_analyzer import analyze_data
from visualization.plot_creator import create_plots
from visualization.dashboard import create_dash_app

# Configuração inicial
app = Flask(__name__)
tipos = ['Land', 'Creature', 'Artifact', 'Enchantment', 'Planeswalker', 'Battle', 'Instant', 'Sorcery']
top_x = 50

# Carrega e processa dados
df, df_sem_land = load_and_preprocess_data('todos_os_decks.csv')

# Análise dos dados (agora passando 'tipos' como parâmetro)
analysis_results = analyze_data(df, df_sem_land, tipos)

# Cria gráficos
plots = create_plots(analysis_results, tipos, top_x)

# Configura o Dash
dash_app = create_dash_app(app, df, tipos)


# Rota principal
@app.route('/')
def index():
    # Converte os gráficos para HTML
    graph_html = {
        'preco_decks': plots['preco_decks'].to_html(full_html=False),
        'cores_comandantes': plots['cores_comandantes'].to_html(full_html=False),
        'cartas_comuns': plots['cartas_comuns'].to_html(full_html=False),
        'edhrec_rank_decks': plots['edhrec_rank_decks'].to_html(full_html=False),
        'tipo_graphs': {tipo: plots['tipos'][tipo].to_html(full_html=False) for tipo in tipos}
    }

    return render_template('index.html',
                           num_decks_distintos=analysis_results['num_decks_distintos'],
                           **graph_html,
                           top_x=top_x)


if __name__ == '__main__':
    app.run(debug=True)