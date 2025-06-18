import streamlit as st
from app.data_loader import load_data
from app.layout import render_header, render_estoque_intermediario
from PIL import Image
import os

favicon_path = os.path.join("image", "logo.png")
favicon_image = Image.open(favicon_path)


st.set_page_config(page_title="Estoque Intermediário - Dashboard MTECH", page_icon="image/logo.png" , layout="wide")

render_header()
_, _, estoque_intermediario = load_data()
render_estoque_intermediario(estoque_intermediario)
