import streamlit as st
import requests
import random
import plotly.graph_objects as go
import logging

#secrets
urls = [
    (st.secrets["URLS"]["URL1"],st.secrets["KEYS"]["KEY1"],st.secrets["NAMES"]["NAME1"]),
        (st.secrets["URLS"]["URL2"],st.secrets["KEYS"]["KEY2"],st.secrets["NAMES"]["NAME2"])
]
# Store visibility checkboxes for each labeler

