import streamlit as st
from app.data_loader import load_data
from app.layout import render_header, render_status_dobradeira
from PIL import Image
import os

# Definir o favicon com sua logo
favicon_path = os.path.join("image", "logo.png")
favicon_image = Image.open(favicon_path)

st.set_page_config(page_title="Geral - Dashboard MTECH", page_icon="image/logo.png" , layout="wide")

render_header()
status_dobradeira, _, _ = load_data()
render_status_dobradeira(status_dobradeira)

