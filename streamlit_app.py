import streamlit as st
import requests
import random
import plotly.graph_objects as go
import logging
from functions import get_labelers_data
import params 

st.set_page_config(layout="wide")

# Configure logging to save to a file
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

# Application Title
st.title("Labelers Statistics ⚽ 🏃‍♂️💨")

# Create a sidebar to select dates
st.sidebar.title("Select Dates")

# Calendar for start date
start_date = st.sidebar.date_input("Start Date")

# Calendar for end date
end_date = st.sidebar.date_input("End Date")

# Get the labelers' data
labelers_data = get_labelers_data(start_date, end_date, params.urls)

# Guardar los checkbox de visibilidad para cada etiquetador

for labeler_id, data in labelers_data.items():
    labeler_name = data["name"]
    random.seed(labeler_id)
    color = color_options[color_index % len(color_options)]
    color_index += 1
    colored_label = f":{color}[{labeler_name}]"
    labelers_visibility[labeler_id] = st.sidebar.checkbox(colored_label, value=True, key=labeler_id)



selected_labelers = {labeler_id: data for labeler_id, data in labelers_data.items() if labelers_visibility[labeler_id]}
if selected_labelers:
    # Dividir en dos columnas
    col1, col2 = st.columns(2)
    
    # Gráfico de "Imágenes Etiquetadas"
    with col1:
        fig1 = go.Figure()
        for labeler_id, data in selected_labelers.items():
            random.seed(labeler_id)
            color = color_options[list(labelers_visibility.keys()).index(labeler_id) % len(color_options)]
            fig1.add_trace(go.Bar(
                x=[data['name']],
                y=[data['images']],
                name=data['name'],
                marker_color=color
            ))
        fig1.update_layout(title='Imágenes Etiquetadas por Etiquetador 🚀🚀🚀', xaxis_title='Etiquetador', yaxis_title='Imágenes Etiquetadas')
        st.plotly_chart(fig1)
    
    # Gráfico de "Cajas Etiquetadas"
    with col2:
        fig2 = go.Figure()
        for labeler_id, data in selected_labelers.items():
            random.seed(labeler_id)
            color = color_options[list(labelers_visibility.keys()).index(labeler_id) % len(color_options)]
            fig2.add_trace(go.Bar(
                x=[data['name']],
                y=[data['boxes']],
                name=data['name'],
                marker_color=color
            ))
        fig2.update_layout(title='Cajas Etiquetadas por Etiquetador 🚀🚀🚀', xaxis_title='Etiquetador', yaxis_title='Cajas Etiquetadas')
        st.plotly_chart(fig2)
if selected_labelers:
    # Dividir en dos columnas
    col3, col4 = st.columns(2)
    
    # Gráfico de sector para el porcentaje de "Imágenes Etiquetadas"
    with col3:
        fig3 = go.Figure()
        labels = [data['name'] for data in selected_labelers.values()]
        values = [data['images'] for data in selected_labelers.values()]
        colors = [color_options[list(labelers_visibility.keys()).index(labeler_id) % len(color_options)] for labeler_id in selected_labelers.keys()]
        fig3.add_trace(go.Pie(labels=labels, values=values, marker=dict(colors=colors)))
        fig3.update_layout(title='Porcentaje de Imágenes Etiquetadas por Etiquetador')
        st.plotly_chart(fig3)
    
    # Gráfico de sector para el porcentaje de "Cajas Etiquetadas"
    with col4:
        fig4 = go.Figure()
        labels = [data['name'] for data in selected_labelers.values()]
        values = [data['boxes'] for data in selected_labelers.values()]
        colors = [color_options[list(labelers_visibility.keys()).index(labeler_id) % len(color_options)] for labeler_id in selected_labelers.keys()]
        fig4.add_trace(go.Pie(labels=labels, values=values, marker=dict(colors=colors)))
        fig4.update_layout(title='Porcentaje de Cajas Etiquetadas por Etiquetador')
        st.plotly_chart(fig4)
if selected_labelers:
    # Dividir en dos columnas
    col5, col6 = st.columns(2)
    
    # Barra de progreso para imágenes etiquetadas
    with col5:
        st.subheader('Progreso de Imágenes Etiquetadas')
        for labeler_id, data in selected_labelers.items():
            images_progress = min((data['images'] / 500), 1.0)  # Asegurar que esté dentro del rango [0.0, 1.0]
            color = color_options[list(labelers_visibility.keys()).index(labeler_id) % len(color_options)]
            st.progress(images_progress)
            st.subheader(f':{color}[{data["name"]}]: {data["images"]} / 500')

    # Barra de progreso para cajas etiquetadas
    with col6:
        st.subheader('Progreso de Cajas Etiquetadas')
        for labeler_id, data in selected_labelers.items():
            boxes_progress = min((data['boxes'] / 8000), 1.0)  # Asegurar que esté dentro del rango [0.0, 1.0]
            color = color_options[list(labelers_visibility.keys()).index(labeler_id) % len(color_options)]
            st.progress(boxes_progress)
            st.subheader(f':{color}[{data["name"]}]: {data["boxes"]} / 8000')
