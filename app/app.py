import streamlit as st

# AQUI TEM QUE SER A PRIMEIRA COISA
st.set_page_config(page_title="Dashboard Produção - MTECH", page_icon="image/logo.png", layout="wide")

from data_loader import load_data
import dashboard as dash_layout

def main():
    dash_layout.render_header()
    status_dobradeira, pecas_faltantes_solda, estoque_intermediario = load_data()
    dash_layout.render_status_dobradeira(status_dobradeira)
    dash_layout.render_pecas_faltantes(pecas_faltantes_solda)
    dash_layout.render_estoque_intermediario(estoque_intermediario)
    dash_layout.render_update_button()

if __name__ == "__main__":
    main()
