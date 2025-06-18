import streamlit as st
import plotly.express as px
from PIL import Image

def render_header():
    logo = Image.open("image/logo.png")
    st.image(logo, width=300)
    st.title(" Dashboard de Produção - MTECH")
    st.markdown("---")

def render_status_dobradeira(status_dobradeira):
    st.subheader("Displays e Peças Prontas")
    cols = st.columns(len(status_dobradeira))
    for idx, row in status_dobradeira.iterrows():
        with cols[idx]:
            st.metric(
                label=str(row[status_dobradeira.columns[0]]),
                value=str(row[status_dobradeira.columns[1]]),
                delta=str(row[status_dobradeira.columns[2]])
            )
    st.markdown("---")

def render_pecas_faltantes(pecas_faltantes_solda):
    st.subheader(" Consumo - Solda MIG")
    st.dataframe(pecas_faltantes_solda, use_container_width=True)

    fig_consumo = px.bar(
        pecas_faltantes_solda,
        x=pecas_faltantes_solda.columns[0],
        y=pecas_faltantes_solda.columns[3],
        title="Consumo por Hora - Solda MIG",
        color=pecas_faltantes_solda.columns[0]
    )
    st.plotly_chart(fig_consumo, use_container_width=True)

    fig_producao = px.bar(
        pecas_faltantes_solda,
        x=pecas_faltantes_solda.columns[0],
        y=pecas_faltantes_solda.columns[4],
        title="Produção por Hora - Solda MIG",
        color=pecas_faltantes_solda.columns[0]
    )
    st.plotly_chart(fig_producao, use_container_width=True)

    st.markdown("---")

def render_estoque_intermediario(estoque_intermediario):
    st.subheader(" Estoque Intermediário - Dobra/Solda")
    st.dataframe(estoque_intermediario, use_container_width=True)

    fig_estoque_hr = px.bar(
        estoque_intermediario,
        x=estoque_intermediario.columns[0],
        y=estoque_intermediario.columns[4],
        title="Horas de Estoque por Peça",
        color=estoque_intermediario.columns[0]
    )
    st.plotly_chart(fig_estoque_hr, use_container_width=True)

    fig_stacked = px.bar(
        estoque_intermediario,
        x=estoque_intermediario.columns[0],
        y=[
            estoque_intermediario.columns[1],
            estoque_intermediario.columns[2],
            estoque_intermediario.columns[3]
        ],
        title="Estoque por Etapa (Dobrado / Soldado / Intermediário)",
        barmode='stack'
    )
    st.plotly_chart(fig_stacked, use_container_width=True)

    st.markdown("---")

def render_update_button():
    if st.button("🔄 Atualizar Dados"):
        st.cache_data.clear()
        st.rerun()
