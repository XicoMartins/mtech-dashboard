import streamlit as st
import pandas as pd
import plotly.express as px
import os

# 🎯 Layout da página
st.set_page_config(
    page_title="Dashboard Produção - MTECH",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Dashboard de Produção - MTECH")
st.subheader("Status Operacional | Peças Faltantes | Estoque Intermediário")
st.markdown("---")

# 🚩 Caminho do arquivo Excel
file_path = os.path.join(os.path.dirname(__file__), 'BASE PARA DASH TESTE.xlsx')

# 🚀 Função para carregar os dados
@st.cache_data
def load_data():
    # 🔧 Ler STATUS DOBRADEIRA
    status_dobradeira = pd.read_excel(
        file_path,
        sheet_name=0,
        skiprows=7,
        nrows=11,
        usecols="A:C"
    )
    status_dobradeira.columns = status_dobradeira.iloc[0]  # Linha 1 vira cabeçalho
    status_dobradeira = status_dobradeira[1:].reset_index(drop=True)  # Remove a linha 1 dos dados

    # 🔥 Ler PEÇAS FALTANTES - SOLDA MIG
    pecas_faltantes_solda = pd.read_excel(
        file_path,
        sheet_name=0,
        skiprows=20,
        nrows=11,
        usecols="A:E"
    )
    pecas_faltantes_solda.columns = pecas_faltantes_solda.iloc[0]
    pecas_faltantes_solda = pecas_faltantes_solda[1:].reset_index(drop=True)

    # 📦 Ler ESTOQUE INTERMEDIÁRIO - DOBRA/SOLDA
    estoque_intermediario = pd.read_excel(
        file_path,
        sheet_name=0,
        skiprows=32,
        nrows=11,
        usecols="A:E"
    )
    estoque_intermediario.columns = estoque_intermediario.iloc[0]
    estoque_intermediario = estoque_intermediario[1:].reset_index(drop=True)

    return status_dobradeira, pecas_faltantes_solda, estoque_intermediario


# 🔄 Carregar os dados
status_dobradeira, pecas_faltantes_solda, estoque_intermediario = load_data()

# =============================================
# 🔧 Painel STATUS DOBRADEIRA
# =============================================
st.subheader("Displays Prontos")

cols = st.columns(len(status_dobradeira))

for idx, row in status_dobradeira.iterrows():
    with cols[idx]:
        st.metric(
            label=str(row[status_dobradeira.columns[0]]),
            value=str(row[status_dobradeira.columns[1]]),
            delta=str(row[status_dobradeira.columns[2]])
        )

st.markdown("---")

# =============================================
# 🔥 Painel PEÇAS FALTANTES - SOLDA MIG
# =============================================
st.subheader("Consumo - Solda MIG")

st.dataframe(pecas_faltantes_solda, use_container_width=True)

fig1 = px.bar(
    pecas_faltantes_solda,
    x=pecas_faltantes_solda.columns[0],
    y=pecas_faltantes_solda.columns[3],
    title="Consumo/Hr de Peças",
    color=pecas_faltantes_solda.columns[0],
    labels={pecas_faltantes_solda.columns[3]: 'Quantidade'}
)
st.plotly_chart(fig1, use_container_width=True)

st.markdown("---")

# =============================================
# 📦 Painel ESTOQUE INTERMEDIÁRIO - DOBRA/SOLDA
# =============================================
st.subheader("📦 Estoque Intermediário - Dobra/Solda")

st.dataframe(estoque_intermediario, use_container_width=True)

fig2 = px.bar(
    estoque_intermediario,
    x=estoque_intermediario.columns[0],
    y=estoque_intermediario.columns[3],
    title="Estoque Intermediário - Quantidade",
    color=estoque_intermediario.columns[0],
    labels={estoque_intermediario.columns[3]: 'Quantidade'}
)
st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# =============================================
# 🔄 Botão de Atualizar Dados
# =============================================
if st.button("🔄 Atualizar Dados"):
    st.cache_data.clear()  # Limpa o cache
    st.rerun()             # Atualiza a página
