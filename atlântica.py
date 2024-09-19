import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from fpdf import FPDF

def carregar_dados(caminho_arquivo):
    dados = pd.read_csv(caminho_arquivo)
    dados.fillna(method='ffill', inplace=True)
    return dados

def gerar_relatorio(dados, caminho_saida):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Relatório de Dados Socioeconômicos", ln=True, align='C')

    resumo = dados.describe().to_string()
    pdf.multi_cell(0, 10, resumo)

    pdf.output(caminho_saida)
    print(f"Relatório gerado: {caminho_saida}")

def criar_visualizacoes(dados):
    plt.figure(figsize=(10, 6))
    sns.histplot(dados['renda'], bins=30, kde=True)
    plt.title('Distribuição de Renda')
    plt.xlabel('Renda')
    plt.ylabel('Frequência')
    plt.grid()
    plt.savefig('distribuicao_renda.png')
    plt.close()

    plt.figure(figsize=(10, 6))
    sns.lineplot(data=dados, x='ano', y='desmatamento', marker='o')
    plt.title('Desmatamento ao Longo dos Anos')
    plt.xlabel('Ano')
    plt.ylabel('Área Desmatada (ha)')
    plt.grid()
    plt.savefig('desmatamento_anos.png')
    plt.close()

def criar_dashboard(dados):
    app = Dash(__name__)

    app.layout = html.Div([
        html.H1("Análise Socioeconômica"),
        dcc.Dropdown(
            id='atividade-dropdown',
            options=[{'label': atividade, 'value': atividade} for atividade in dados['atividade'].unique()],
            value=dados['atividade'].unique()[0]
        ),
        dcc.Graph(id='grafico-atividade'),
        dcc.Graph(figure=criar_grafico_desmatamento(dados))
    ])

    @app.callback(
        Output('grafico-atividade', 'figure'),
        Input('atividade-dropdown', 'value')
    )
    def atualizar_grafico(atividade_selecionada):
        df_filtrado = dados[dados['atividade'] == atividade_selecionada]
        fig = sns.barplot(x='ano', y='area_agropecuaria', data=df_filtrado)
        return fig

    app.run_server(debug=True)

def criar_grafico_desmatamento(dados):
    fig, ax = plt.subplots()
    sns.lineplot(data=dados, x='ano', y='desmatamento', marker='o', ax=ax)
    ax.set_title('Desmatamento ao Longo dos Anos')
    ax.set_xlabel('Ano')
    ax.set_ylabel('Área Desmatada (ha)')
    plt.close(fig)  
    return fig

caminho_arquivo = 'dados_socioeconomicos.csv'
caminho_relatorio = 'relatorio_socioeconomico.pdf'

dados = carregar_dados(caminho_arquivo)
gerar_relatorio(dados, caminho_relatorio)
criar_visualizacoes(dados)
criar_dashboard(dados)
