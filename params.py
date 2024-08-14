import streamlit as st
import requests
import random
import plotly.graph_objects as go
import logging

# Función para almacenar en caché las URLs
urls = [
    (st.secrets["URLS"]["URL1"],st.secrets["KEYS"]["KEY1"],st.secrets["NAMES"]["NAME1"]),
        (st.secrets["URLS"]["URL2"],st.secrets["KEYS"]["KEY2"],st.secrets["NAMES"]["NAME2"])
]
# Store visibility checkboxes for each labeler
labelers_visibility = {}
labeler_color_map = {}
color_options = ["blue", "green", "orange", "red", "violet","gray"]
color_index = 0
