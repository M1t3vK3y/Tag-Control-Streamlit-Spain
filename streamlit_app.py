import streamlit as st
import requests
import random
import plotly.graph_objects as go
import logging
from functions import get_labelers_data
import params 

labelers_visibility = {}
color_options = ["blue", "green", "orange", "red", "violet","gray"]
color_index = 0    
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

if 'labelers_visibility' not in st.session_state:
    st.session_state.labelers_visibility = {}
if 'color_index' not in st.session_state:
    st.session_state.color_index = 0

labeler_color_map = {}

for labeler_id, data in labelers_data.items():
    labeler_name = data["name"]
    
    # Assign color to labeler and save in the map
    color = params.color_options[st.session_state.color_index % len(params.color_options)]
    st.session_state.color_index += 1
    labeler_color_map[labeler_id] = color
    
    # Check if labeler_id exists in session_state, otherwise default to True
    if labeler_id not in st.session_state.labelers_visibility:
        st.session_state.labelers_visibility[labeler_id] = True
    
    colored_label = f":{color}[{labeler_name}]"
    st.session_state.labelers_visibility[labeler_id] = st.sidebar.checkbox(colored_label, value=st.session_state.labelers_visibility[labeler_id], key=labeler_id)

selected_labelers = {labeler_id: data for labeler_id, data in labelers_data.items() if st.session_state.labelers_visibility[labeler_id]}
if selected_labelers:
    # Split into two columns
    col1, col2 = st.columns(2)
    
    # "Images Labeled" Chart
    with col1:
        fig1 = go.Figure()
        for labeler_id, data in selected_labelers.items():
            total_images = sum(data['urls'][url]['images'] for url in data['urls'])
            color = labeler_color_map[labeler_id]
            fig1.add_trace(go.Bar(
                x=[data['name']],
                y=[total_images],
                name=data['name'],
                marker_color=color
            ))
        fig1.update_layout(title='Images Labeled by Labeler 🚀🚀🚀', xaxis_title='Labeler', yaxis_title='Images Labeled')
        st.plotly_chart(fig1)
    
    # "Boxes Labeled" Chart
    with col2:
        fig2 = go.Figure()
        for labeler_id, data in selected_labelers.items():
            total_boxes = sum(data['urls'][url]['boxes'] for url in data['urls'])
            color = labeler_color_map[labeler_id]
            fig2.add_trace(go.Bar(
                x=[data['name']],
                y=[total_boxes],
                name=data['name'],
                marker_color=color
            ))
        fig2.update_layout(title='Boxes Labeled by Labeler 🚀🚀🚀', xaxis_title='Labeler', yaxis_title='Boxes Labeled')
        st.plotly_chart(fig2)

if selected_labelers:
    # Split into two columns
    col3, col4 = st.columns(2)
    
    # Pie chart for "Images Labeled" percentage
    with col3:
        fig3 = go.Figure()
        labels = [data['name'] for data in selected_labelers.values()]
        values = [sum(data['urls'][url]['images'] for url in data['urls']) for data in selected_labelers.values()]
        colors = [labeler_color_map[labeler_id] for labeler_id in selected_labelers.keys()]
        fig3.add_trace(go.Pie(labels=labels, values=values, marker=dict(colors=colors)))
        fig3.update_layout(title='Percentage of Images Labeled by Labeler')
        st.plotly_chart(fig3)
    
    # Pie chart for "Boxes Labeled" percentage
    with col4:
        fig4 = go.Figure()
        labels = [data['name'] for data in selected_labelers.values()]
        values = [sum(data['urls'][url]['boxes'] for url in data['urls']) for data in selected_labelers.values()]
        colors = [labeler_color_map[labeler_id] for labeler_id in selected_labelers.keys()]
        fig4.add_trace(go.Pie(labels=labels, values=values, marker=dict(colors=colors)))
        fig4.update_layout(title='Percentage of Boxes Labeled by Labeler')
        st.plotly_chart(fig4)

if selected_labelers:
    # Split into two columns
    col5, col6 = st.columns(2)
    
    # Progress bar for labeled images
    with col5:
        st.subheader('Progress of Images Labeled')
        for url, api_key, name in params.urls:
            st.markdown(f"<h4 style='text-align: center; text-decoration: underline;'>{name}</h4>", unsafe_allow_html=True)
            for labeler_id, data in selected_labelers.items():
                if url in data["urls"]:
                    images = data["urls"][url]["images"]
                    images_progress = min((images / 500), 1.0)  # Ensure it's within the range [0.0, 1.0]
                    color = labeler_color_map[labeler_id]
                    st.progress(images_progress)
                    st.subheader(f':{color}[{data["name"]}]: {images} / 500')

    # Progress bar for labeled boxes
    with col6:
        st.subheader('Progress of Boxes Labeled')
        for url, api_key, name in params.urls:
            st.markdown(f"<h4 style='text-align: center; text-decoration: underline;'>{name}</h4>", unsafe_allow_html=True)
            for labeler_id, data in selected_labelers.items():
                if url in data["urls"]:
                    boxes = data["urls"][url]["boxes"]
                    boxes_progress = min((boxes / 8000), 1.0)  # Ensure it's within the range [0.0, 1.0]
                    color = labeler_color_map[labeler_id]
                    st.progress(boxes_progress)
                    st.subheader(f':{color}[{data["name"]}]: {boxes} / 8000')
