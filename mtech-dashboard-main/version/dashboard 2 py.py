import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# 🎯 Configuração da página do Streamlit
# Define o título, ícone e layout da página. O layout "wide" faz o conteúdo ocupar toda a largura da tela.
st.set_page_config(
    page_title="Dashboard de Produção MTECH",
    page_icon="📊",
    layout="wide"
)

# Título principal e subtítulo do dashboard
st.title("📊 Dashboard Produção")
st.subheader("Status Operacional | Peças Faltantes | Estoque Intermediário")
st.markdown("---")

# 🚩 Define o caminho para o arquivo Excel de forma robusta
# Usar Path é uma prática moderna que funciona bem em diferentes sistemas operacionais (Windows, Linux, etc.)
try:
    file_path = Path(__file__).parent / 'BASE PARA DASH TESTE.xlsx'
except NameError:
    # Fallback para quando o script é executado em ambientes onde __file__ não está definido (ex: notebooks)
    file_path = Path('BASE PARA DASH TESTE.xlsx').resolve()


# 🚀 Função otimizada para carregar os dados do Excel
# O decorador @st.cache_data garante que o Streamlit não recarregue o arquivo a cada interação do usuário,
# melhorando muito a performance. O cache só é limpo quando os dados de entrada mudam ou o cache é zerado manualmente.
@st.cache_data
def load_data(path):
    """Carrega todos os dataframes necessários a partir do arquivo Excel."""
    try:
        # Lê cada tabela especificando a aba (sheet_name=0, a primeira), as linhas a serem puladas (skiprows),
        # o número de linhas a serem lidas (nrows) e as colunas a serem usadas (usecols).
        status_dobradeira = pd.read_excel(
            path, sheet_name=0, skiprows=7, nrows=11, usecols="A:C"
        )
        pecas_faltantes_solda = pd.read_excel(
            path, sheet_name=0, skiprows=20, nrows=11, usecols="A:E"
        )
        estoque_intermediario = pd.read_excel(
            path, sheet_name=0, skiprows=32, nrows=11, usecols="A:E"
        )
        return status_dobradeira, pecas_faltantes_solda, estoque_intermediario
    except FileNotFoundError:
        # Se o arquivo não for encontrado, exibe uma mensagem de erro clara no dashboard e interrompe a execução.
        st.error(f"❌ Erro: O arquivo '{path.name}' não foi encontrado. Verifique se ele está na mesma pasta que o script.")
        st.stop()


# 🔧 Função reutilizável para criar as seções do dashboard (Tabela + Gráfico)
def criar_secao_dashboard(titulo, df, coluna_x, coluna_y):
    """Gera um subcabeçalho, um dataframe e um gráfico de barras para uma seção do dashboard."""
    st.subheader(titulo)
    st.dataframe(df, use_container_width=True)

    # Cria o gráfico de barras com Plotly Express
    fig = px.bar(
        df,
        x=coluna_x,
        y=coluna_y,
        title=f"{titulo} - Quantidade",
        color=coluna_x,  # Colore as barras de acordo com a categoria
        labels={coluna_y: 'Quantidade'}
    )
    # Exibe o gráfico no Streamlit, usando a largura total do container
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("---")


# 🔄 Carrega os dados na inicialização do script
df_status_dobradeira, df_pecas_faltantes, df_estoque_intermediario = load_data(file_path)


# ==============================================================================
# SEÇÃO 1: STATUS DA DOBRADEIRA
# ==============================================================================
st.subheader("🔩 Status Dobradeira")

# Renomeia as colunas para facilitar o acesso e deixar o código mais legível
df_status_dobradeira.columns = ['Maquina', 'Status', 'Observacao']

# Cria colunas dinamicamente no Streamlit para exibir as métricas lado a lado
cols = st.columns(len(df_status_dobradeira))
for idx, row in df_status_dobradeira.iterrows():
    with cols[idx]:
        # st.metric é ideal para exibir KPIs (Key Performance Indicators)
        st.metric(
            label=row['Maquina'],
            value=row['Status'],
            delta=row['Observacao']
        )
st.markdown("---")


# ==============================================================================
# SEÇÃO 2: PEÇAS FALTANTES - SOLDA MIG
# ==============================================================================
# Renomeia as colunas para maior clareza
df_pecas_faltantes.columns = ['Produto', 'Codigo', 'Descricao', 'Quantidade', 'Observacao']
# Chama a função para criar a seção do dashboard
criar_secao_dashboard(
    titulo="Peças Usadas Solda MIG",
    df=df_pecas_faltantes,
    coluna_x='Produto',
    coluna_y='Quantidade'
)


# ==============================================================================
# SEÇÃO 3: ESTOQUE INTERMEDIÁRIO - DOBRA/SOLDA
# ==============================================================================
# Renomeia as colunas
df_estoque_intermediario.columns = ['Produto', 'Codigo', 'Descricao', 'Quantidade', 'Observacao']
# Chama a função para criar a segunda seção do dashboard
criar_secao_dashboard(
    titulo="📦 Estoque Intermediário - Dobra/Solda",
    df=df_estoque_intermediario,
    coluna_x='Produto',
    coluna_y='Quantidade'
)


# ==============================================================================
# BOTÃO DE ATUALIZAÇÃO
# ==============================================================================
# Este botão permite ao usuário forçar a limpeza do cache e recarregar os dados do zero.
st.write("Clique no botão abaixo para forçar a atualização dos dados do arquivo Excel.")
if st.button("🔄 Atualizar Dados"):
    st.cache_data.clear()  # Limpa o cache de dados
    st.rerun()  # Reinicia o script a partir do topo