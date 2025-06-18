import streamlit as st
from PIL import Image
import os
from data_loader import load_data
from layout import (
    render_header,
    render_status_dobradeira,
    render_pecas_faltantes,
    render_estoque_intermediario,
    set_custom_css
)

# Carregar o favicon
favicon_path = os.path.join("image", "logo.png")
favicon_image = Image.open(favicon_path)


# Tem que ser a PRIMEIRA coisa Streamlit
st.set_page_config(page_title="Dashboard Produção - MTECH", page_icon="image/logo.png" ,layout="wide")

# Depois o CSS
set_custom_css()

# ====== Sidebar Manual ======
st.sidebar.title("Navegação")
pagina = st.sidebar.radio(
    "Selecione a Página:",
    ("Geral", "Solda MIG", "Estoque Intermediário")
)

# ====== Carregamento de Dados ======
status_dobradeira, pecas_faltantes, estoque_intermediario = load_data()

# ====== Cabeçalho (Logo + Título) ======
render_header()

# ====== Renderização das Páginas ======
if pagina == "Geral":
    render_status_dobradeira(status_dobradeira)
elif pagina == "Solda MIG":
    render_pecas_faltantes(pecas_faltantes)
elif pagina == "Estoque Intermediário":
    render_estoque_intermediario(estoque_intermediario)
