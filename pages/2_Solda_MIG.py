import streamlit as st
from app.data_loader import load_data
from app.layout import render_header, render_pecas_faltantes
from PIL import Image
import os

favicon_path = os.path.join("image", "logo.png")
favicon_image = Image.open(favicon_path)

st.set_page_config(page_title="Solda MIG - Dashboard MTECH", page_icon="image/logo.png" , layout="wide")

render_header()
_, pecas_faltantes, _ = load_data()
render_pecas_faltantes(pecas_faltantes)
