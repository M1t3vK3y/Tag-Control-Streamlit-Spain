import streamlit as st
import requests
import random
import plotly.graph_objects as go
import logging
from functions import get_labelers_data
from params import urls, labelers_visibility, color_options, color_index, labeler_color_map
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



assigned_colors = {}
for labeler_id, data in labelers_data.items():
    if labeler_id not in assigned_colors:
        random.seed(labeler_id)  # Para asegurar una asignación consistente
        color = color_options[color_index % len(color_options)]
        assigned_colors[labeler_id] = color
        color_index += 1


# Guardar los checkbox de visibilidad para cada etiquetador
for labeler_id, data in labelers_data.items():
    labeler_name = data["name"]
    random.seed(labeler_id)
    color = assigned_colors[labeler_id]
    colored_label = f":{color}[{labeler_name}]"
    labelers_visibility[labeler_id] = st.sidebar.checkbox(colored_label, value=True, key=labeler_id)


selected_labelers = {labeler_id: data for labeler_id, data in labelers_data.items() if labelers_visibility[labeler_id]}
if selected_labelers:
    # Dividir en dos columnas
    col1, col2 = st.columns(2)
    
    # Gráfico de "Imágenes Etiquetadas"
    with col1:
        fig1 = go.Figure()
        color_index = 0
        for labeler_id, data in selected_labelers.items():
            total_images = sum(data['urls'][url]['images'] for url in data['urls'])
            color = assigned_colors[labeler_id]
            fig1.add_trace(go.Bar(
                x=[data['name']],
                y=[total_images],
                name=data['name'],
                marker_color=color
            ))
            color_index += 1
        fig1.update_layout(title='Imágenes Etiquetadas por Etiquetador 🚀🚀🚀', xaxis_title='Etiquetador', yaxis_title='Imágenes Etiquetadas')
        st.plotly_chart(fig1)
    
    # Gráfico de "Cajas Etiquetadas"
    with col2:
        fig2 = go.Figure()
        color_index = 0
        for labeler_id, data in selected_labelers.items():
            total_boxes = sum(data['urls'][url]['boxes'] for url in data['urls'])
            color = assigned_colors[labeler_id]
            fig2.add_trace(go.Bar(
                x=[data['name']],
                y=[total_boxes],
                name=data['name'],
                marker_color=color
            ))
            color_index += 1
        fig2.update_layout(title='Cajas Etiquetadas por Etiquetador 🚀🚀🚀', xaxis_title='Etiquetador', yaxis_title='Cajas Etiquetadas')
        st.plotly_chart(fig2)
if selected_labelers:
    # Dividir en dos columnas
    col3, col4 = st.columns(2)
    
    # Gráfico de sector para el porcentaje de "Imágenes Etiquetadas"
    with col3:
        fig3 = go.Figure()
        labels = [data['name'] for data in selected_labelers.values()]
        values = [sum(data['urls'][url]['images'] for url in data['urls']) for data in selected_labelers.values()]    
        # Create a list of colors for the pie chart
        colors = [assigned_colors[labeler_id] for labeler_id in selected_labelers.keys()]
        fig3.add_trace(go.Pie(labels=labels, values=values, marker=dict(colors=colors)))
        fig3.update_layout(title='Percentage of Images Labeled by Labeler')
        st.plotly_chart(fig3)
    
    # Gráfico de sector para el porcentaje de "Cajas Etiquetadas"
    with col4:
        fig4 = go.Figure()
        labels = [data['name'] for data in selected_labelers.values()]
        values = [sum(data['urls'][url]['boxes'] for url in data['urls']) for data in selected_labelers.values()]
        colors = [assigned_colors[labeler_id] for labeler_id in selected_labelers.keys()]
        fig4.add_trace(go.Pie(labels=labels, values=values, marker=dict(colors=colors)))
        fig4.update_layout(title='Percentage of Boxes Labeled by Labeler')
        st.plotly_chart(fig4)
if selected_labelers:
    # Dividir en dos columnas
    col5, col6 = st.columns(2)
    
    # Barra de progreso para imágenes etiquetadas
    # Progress of Images Labeled
    with col5:
        st.subheader('Progress of Images Labeled')
        color_index = 0
        for url, api_key, name in params.urls:
            st.markdown(f"<h4 style='text-align: center; text-decoration: underline;'>{name}</h4>", unsafe_allow_html=True)
            for labeler_id, data in selected_labelers.items():
                if url in data["urls"]:
                    images = data["urls"][url]["images"]
                    images_progress = min((images / 500), 1.0)  # Asegurar que esté dentro del rango [0.0, 1.0]
                    color = assigned_colors[labeler_id]
                    st.progress(images_progress)
                    st.subheader(f':{color}[{data["name"]}]: {images} / 500')
                    subcol1, subcol2= st.columns(2)
                    with subcol1:
                           # Esto se puede usar para un pequeño espacio
                         st.metric(label="", value="", delta="") 
                         st.metric(label="", value="", delta="")# Esto ocupa más espacio visualmente
                         

                    # Mostrar información de "boxesRemoved"
                    with subcol2:
                         st.write("")  # Esto se puede usar para un pequeño espacio
                        
                         

                    # Mostrar información de "boxesUpdated"
                    
                    color_index += 1
    
    # Progress of Boxes Labeled
    with col6:
        st.subheader('Progress of Boxes Labeled')
        color_index = 0
        for url, api_key, name in params.urls:
            st.markdown(f"<h4 style='text-align: center; text-decoration: underline;'>{name}</h4>", unsafe_allow_html=True)
            for labeler_id, data in selected_labelers.items():
                if url in data["urls"]:
                    boxes = data["urls"][url]["boxes"]
                    boxes_progress = min((boxes / 8000), 1.0)  # Asegurar que esté dentro del rango [0.0, 1.0]
                    color = assigned_colors[labeler_id]

                    # Mostrar barra de progreso para "boxes"
                    st.progress(boxes_progress)
                    st.subheader(f':{color}[{data["name"]}]: {boxes} / 8000')

                    # Dividir en tres columnas para mostrar boxesAdded, boxesRemoved y boxesUpdated
                    subcol1, subcol2, subcol3 = st.columns(3)

                    # Mostrar información de "boxesAdded"
                    with subcol1:
                        boxes_added = data["urls"][url]["boxesAdded"]  # Extraer el valor de boxesAdded
                        st.metric("Boxes Added", boxes_added)

                    # Mostrar información de "boxesRemoved"
                    with subcol2:
                        boxes_removed = data["urls"][url]["boxesRemoved"]  # Extraer el valor de boxesRemoved
                        st.metric("Boxes Removed", boxes_removed)

                    # Mostrar información de "boxesUpdated"
                    with subcol3:
                        boxes_updated = data["urls"][url]["boxesUpdated"]  # Extraer el valor de boxesUpdated
                        st.metric("Boxes Updated", boxes_updated)

                    color_index += 1
st.markdown("---")  # Línea divisoria
st.subheader("URLs utilizadas para la obtención de datos (incluyendo las fechas seleccionadas)")
for url, api_key, name in params.urls:
    full_url = f"{url}?api_key={api_key}&startDate={start_date.strftime('%Y-%m-%d')}&endDate={end_date.strftime('%Y-%m-%d')}"
    st.write(f"- {name}: {full_url}")
