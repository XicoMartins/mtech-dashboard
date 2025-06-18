import streamlit as st
import plotly.express as px
from PIL import Image
import os
import plotly.graph_objects as go
import pandas as pd
import base64


def set_custom_css():
    st.markdown("""
        <style>
            body {
                background-color: #2c2f33;
                color: #ffffff;
            }
            .stText, .stMarkdown, .stMetric, .stDataFrame {
                color: #ffffff;
            }
            hr {
                border: 1px solid #444;
            }
        </style>
    """, unsafe_allow_html=True)



def render_header():
    logo_path = os.path.join("image", "logo.png")
    logo = Image.open(logo_path)

    col1, col2 = st.columns([1, 3])

    with col1:
        st.image(logo, width=180)

    with col2:
        st.markdown("""
            <h2 style='margin-bottom: 5px; margin-top: 20px;'>DASHBOARD DE PRODUÇÃO - MTECH</h2>
            <p style='color: white; margin-top: 5px;font-size: 30px;'>Controle de Produção - RACK MINI ADES</p>
        """, unsafe_allow_html=True)

    st.markdown("<hr style='margin-top:10px; margin-bottom:10px;'>", unsafe_allow_html=True)

def render_status_dobradeira(status_dobradeira):
    # Converte a imagem para base64 para embutir no HTML
    icon_path = os.path.join("image", "industry.png")
    with open(icon_path, "rb") as img_file:
        img_base64 = base64.b64encode(img_file.read()).decode()

    st.markdown(f"""
        <p style="display: flex; align-items: center; margin-bottom: 10px;">
            <img src="data:image/png;base64,{img_base64}" width="100" style="margin-right: 10px;">
            <span style="font-size: 40px; font-weight: bold; color: white;">Displays e Peças Prontas</span>
        </p>
    """, unsafe_allow_html=True)


    num_cols = 4  # Número de cards por linha
    rows = [
        status_dobradeira.iloc[i:i+num_cols]
        for i in range(0, len(status_dobradeira), num_cols)
    ]

    card_style = """
        background-color: #1e1e1e;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.3);
        margin-bottom: 20px;
    """

    for chunk in rows:
        cols = st.columns(len(chunk))
        for idx, row in chunk.iterrows():
            processo = str(row[status_dobradeira.columns[0]])
            displays = str(row[status_dobradeira.columns[1]])
            pecas = str(row[status_dobradeira.columns[2]])

            with cols[list(chunk.index).index(idx)]:
                st.markdown(f"""
                    <div style="{card_style}">
                        <h4 style='color:#00BFFF;'>{processo}</h4>
                        <h2 style='margin-top:10px;'>{displays} Displays Prontos</h2>
                        <p style='margin-top:10px;'>🔩 <b>{pecas}</b> Peças Prontas</p>
                    </div>
                """, unsafe_allow_html=True)

    st.markdown("---")



def render_pecas_faltantes(pecas_faltantes_solda):
    # Converte o ícone para base64
    icon_path = os.path.join("image", "eco-factory.png")
    with open(icon_path, "rb") as img_file:
        img_base64 = base64.b64encode(img_file.read()).decode()

    # Renderiza o título com ícone e texto lado a lado
    st.markdown(f"""
        <p style="display: flex; align-items: center; margin-bottom: 10px;">
            <img src="data:image/png;base64,{img_base64}" width="50" style="margin-right: 10px;">
            <span style="font-size: 40px; font-weight: bold; color: white;">Consumo - Solda MIG</span>
        </p>
    """, unsafe_allow_html=True)

    # Limpar a tabela (tirar linha None)
    pecas_faltantes_solda = pecas_faltantes_solda.dropna(subset=[pecas_faltantes_solda.columns[0]]).reset_index(drop=True)

    # ===== Sidebar: Filtros com botão "Selecionar Tudo" =====
    lista_pecas = pecas_faltantes_solda[pecas_faltantes_solda.columns[0]].unique().tolist()

    st.sidebar.markdown("### Filtro de Peças")
    select_all = st.sidebar.checkbox("Selecionar Todas", value=True)

    if select_all:
        pecas_selecionadas = st.sidebar.multiselect(
            "Peças:",
            options=lista_pecas,
            default=lista_pecas
        )
    else:
        pecas_selecionadas = st.sidebar.multiselect(
            "Peças:",
            options=lista_pecas
        )

    # Filtrar os dados
    df = pecas_faltantes_solda[pecas_faltantes_solda[pecas_faltantes_solda.columns[0]].isin(pecas_selecionadas)]

    # =========================
    # Gráfico 1: QNT x USADAS (Agrupado lado a lado)
    # =========================
    fig_qnt_usadas = go.Figure()

    fig_qnt_usadas.add_trace(go.Bar(
        x=df[pecas_faltantes_solda.columns[0]],
        y=df[pecas_faltantes_solda.columns[1]],
        name='Quantidade (QNT)',
        marker_color='#5bc0de',
        text=df[pecas_faltantes_solda.columns[1]],
        textposition='outside'
    ))

    fig_qnt_usadas.add_trace(go.Bar(
        x=df[pecas_faltantes_solda.columns[0]],
        y=df[pecas_faltantes_solda.columns[2]],
        name='Peças Usadas',
        marker_color='#d9534f',
        text=df[pecas_faltantes_solda.columns[2]],
        textposition='outside'
    ))

    fig_qnt_usadas.update_layout(
        barmode='group',
        title='Quantidade Total x Peças Usadas',
        xaxis_title='Peça',
        yaxis_title='',
        plot_bgcolor='#20232a',
        paper_bgcolor='#20232a',
        font_color='white'
    )

    st.plotly_chart(fig_qnt_usadas, use_container_width=True)

    # =========================
    # Gráfico 2: Consumo/Hora x Produção/Hora (Agrupado lado a lado)
    # =========================
    fig_con_prod = go.Figure()

    fig_con_prod.add_trace(go.Bar(
        x=df[pecas_faltantes_solda.columns[0]],
        y=df[pecas_faltantes_solda.columns[3]],
        name='Consumo por Hora',
        marker_color='#f0ad4e',
        text=df[pecas_faltantes_solda.columns[3]],
        textposition='outside'
    ))

    fig_con_prod.add_trace(go.Bar(
        x=df[pecas_faltantes_solda.columns[0]],
        y=df[pecas_faltantes_solda.columns[4]],
        name='Produção por Hora',
        marker_color='#5cb85c',
        text=df[pecas_faltantes_solda.columns[4]],
        textposition='outside'
    ))

    fig_con_prod.update_layout(
        barmode='group',
        title='Consumo/Hora x Produção/Hora',
        xaxis_title='Peça',
        yaxis_title='',
        plot_bgcolor='#20232a',
        paper_bgcolor='#20232a',
        font_color='white'
    )

    st.plotly_chart(fig_con_prod, use_container_width=True)

    # Garantir que as colunas usadas no gráfico sejam numéricas
    df[pecas_faltantes_solda.columns[1]] = pd.to_numeric(df[pecas_faltantes_solda.columns[1]], errors='coerce')
    df[pecas_faltantes_solda.columns[3]] = pd.to_numeric(df[pecas_faltantes_solda.columns[3]], errors='coerce')
    df[pecas_faltantes_solda.columns[4]] = pd.to_numeric(df[pecas_faltantes_solda.columns[4]], errors='coerce')

    
    # =========================
    # Gráfico 3: Bubble Chart (Dispersão das 4 variáveis)
    # =========================
    fig_bubble = px.scatter(
        df,
        x=pecas_faltantes_solda.columns[3],  # CONSUMO/HR
        y=pecas_faltantes_solda.columns[4],  # PRODUÇÃO/HR
        size=pecas_faltantes_solda.columns[1],  # QNT
        color=pecas_faltantes_solda.columns[0],  # Nome da peça
        hover_name=pecas_faltantes_solda.columns[0],
        size_max=60,
        title="Relação entre Consumo/Hora, Produção/Hora e Quantidade"
    )

    fig_bubble.update_layout(
        plot_bgcolor='#20232a',
        paper_bgcolor='#20232a',
        font_color='white',
        xaxis_title='Consumo por Hora',
        yaxis_title='Produção por Hora',
        legend_title='Peças'
    )

    st.plotly_chart(fig_bubble, use_container_width=True)

    st.markdown("---")




def render_estoque_intermediario(estoque_intermediario):
    # Converte o ícone para base64
    icon_path = os.path.join("image", "available.png")
    with open(icon_path, "rb") as img_file:
        img_base64 = base64.b64encode(img_file.read()).decode()

    # Renderiza o título com ícone e texto lado a lado
    st.markdown(f"""
        <p style="display: flex; align-items: center; margin-bottom: 10px;">
            <img src="data:image/png;base64,{img_base64}" width="50" style="margin-right: 10px;">
            <span style="font-size: 40px; font-weight: bold; color: white;">Estoque Intermediário - Dobra/Solda</span>
        </p>
    """, unsafe_allow_html=True)

    # Limpar linha None
    estoque_intermediario = estoque_intermediario.dropna(subset=[estoque_intermediario.columns[0]]).reset_index(drop=True)

    # Garantir colunas numéricas
    for col in estoque_intermediario.columns[1:]:
        estoque_intermediario[col] = pd.to_numeric(estoque_intermediario[col], errors='coerce')

    # ===== Sidebar: Filtro de Peças =====
    lista_pecas = estoque_intermediario[estoque_intermediario.columns[0]].unique().tolist()
    st.sidebar.markdown("### Filtro de Peças - Estoque")
    select_all = st.sidebar.checkbox("Selecionar Todas", value=True)

    if select_all:
        pecas_selecionadas = st.sidebar.multiselect(
            "Peças:",
            options=lista_pecas,
            default=lista_pecas
        )
    else:
        pecas_selecionadas = st.sidebar.multiselect(
            "Peças:",
            options=lista_pecas
        )

    df = estoque_intermediario[estoque_intermediario[estoque_intermediario.columns[0]].isin(pecas_selecionadas)]

    # =========================
    # Gráfico 1: Barras Empilhadas - Dobradas x Soldadas x Estoque
    # =========================
    fig_stack = go.Figure()

    fig_stack.add_trace(go.Bar(
        x=df[df.columns[0]],
        y=df[df.columns[1]],
        name='Peças Dobradas',
        marker_color='#5bc0de'
    ))

    fig_stack.add_trace(go.Bar(
        x=df[df.columns[0]],
        y=df[df.columns[2]],
        name='Peças Soldadas',
        marker_color='#f0ad4e'
    ))

    fig_stack.add_trace(go.Bar(
        x=df[df.columns[0]],
        y=df[df.columns[3]],
        name='Estoque Intermediário',
        marker_color='#5cb85c'
    ))

    fig_stack.update_layout(
        barmode='stack',
        title='Fluxo de Produção: Dobradas x Soldadas x Estoque Intermediário',
        xaxis_title='Peça',
        yaxis_title='Unidades',
        plot_bgcolor='#20232a',
        paper_bgcolor='#20232a',
        font_color='white'
    )

    st.plotly_chart(fig_stack, use_container_width=True)

    # =========================
    # Gráfico 2: Horas de Estoque (colunas coloridas)
    # =========================
    colors = ['red' if h <= 5 else 'green' for h in df[df.columns[4]]]

    fig_horas = go.Figure()
    fig_horas.add_trace(go.Bar(
        x=df[df.columns[0]],
        y=df[df.columns[4]],
        marker_color=colors,
        text=df[df.columns[4]],
        textposition='outside'
    ))

    fig_horas.update_layout(
        title='Cobertura de Estoque (Horas Disponíveis)',
        xaxis_title='Peça',
        yaxis_title='Horas',
        plot_bgcolor='#20232a',
        paper_bgcolor='#20232a',
        font_color='white'
    )

    st.plotly_chart(fig_horas, use_container_width=True)

    # =========================
    # Gráfico 3: Top 5 Estoque Intermediário (Pizza)
    # =========================
    df_top5 = df.sort_values(by=df.columns[3], ascending=False).head(5)

    fig_pizza = px.pie(
        df_top5,
        names=df_top5[df.columns[0]],
        values=df_top5[df.columns[3]],
        title='Top 5 Peças com Maior Estoque Intermediário'
    )

    fig_pizza.update_layout(
        plot_bgcolor='#20232a',
        paper_bgcolor='#20232a',
        font_color='white'
    )

    st.plotly_chart(fig_pizza, use_container_width=True)

    # =========================
    # Opcional: Tabela Detalhada
    # =========================
    st.markdown("---")
    icon_path = os.path.join("image", "report.png")
    with open(icon_path, "rb") as img_file:
        img_base64 = base64.b64encode(img_file.read()).decode()
    # Renderiza o título com ícone e texto lado a lado
    st.markdown(f"""
        <p style="display: flex; align-items: center; margin-bottom: 10px; margin-top: 20px;">
            <img src="data:image/png;base64,{img_base64}" width="30" style="margin-right: 10px;">
            <span style="font-size: 26px; font-weight: bold; color: white;">Detalhamento Completo (após filtros)</span>
        </p>
    """, unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True)

