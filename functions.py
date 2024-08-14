import streamlit as st
import requests
import random
import plotly.graph_objects as go
import logging
#function
@st.cache_data
def get_labelers_data(start_date, end_date, urls):
    labelers_data = {}
    for url, api_key,_ in urls:
        params = {
            "api_key": api_key,
            "startDate": start_date.strftime("%Y-%m-%d"),
            "endDate": end_date.strftime("%Y-%m-%d")
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            labelers = data["labelers"]
            for labeler in labelers:
                labeler_id = labeler["id"]
                labeler_name = labeler["displayName"]
                images_labeled = sum(entry["imagesLabeled"] for entry in data["data"] if entry["labelerId"] == labeler_id)
                boxes_labeled = sum(entry["boxesDrawn"] for entry in data["data"] if entry["labelerId"] == labeler_id)
                if labeler_id not in labelers_data:
                    labelers_data[labeler_id] = {"name": labeler_name, "images": images_labeled, "boxes": boxes_labeled}
                else:
                    labelers_data[labeler_id]["images"] += images_labeled
                    labelers_data[labeler_id]["boxes"] += boxes_labeled
        else:
            st.error(f"Error al realizar la solicitud a la API: {url}")
    return labelers_data
