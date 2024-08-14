import streamlit as st
import requests
import random
import plotly.graph_objects as go
import logging

# Función para almacenar en caché las URLs
@st.cache_data
def get_urls():
    return [
        (st.secrets["URLS"]["URL1"], st.secrets["KEYS"]["KEY1"], st.secrets["NAMES"]["NAME1"]),
        (st.secrets["URLS"]["URL2"], st.secrets["KEYS"]["KEY2"], st.secrets["NAMES"]["NAME2"])
    ]

# Función para almacenar en caché las opciones de color
@st.cache_data
def get_color_options():
    return ["blue", "green", "orange", "red", "violet", "gray"]

# Función para almacenar en caché el índice de color
@st.cache_data
def get_color_index():
    return 0

# Función para almacenar en caché la visibilidad de los etiquetadores
@st.cache_data
def get_labelers_visibility():
    return {}

# Obtén las variables desde la caché
urls = get_urls()
color_options = get_color_options()
color_index = get_color_index()
labelers_visibility = get_labelers_visibility()
