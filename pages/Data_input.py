import streamlit as st
from streamlit.components.v1 import html

import os
from pathlib import Path
import sys
import json
import numpy as np

script_dir = Path(__file__).parent
sys.path.append(str(script_dir))

from utils.uk_load.faraday import fetch_data
from utils.uk_load.faraday_postprocessing import process_files
#from utils.us_load.worker_us_load import run_trace_estimation
from utils.solar.solar import fetch_solar_data_from_api

# Mapping input combinations to pre-downloaded file names
def get_load_file_path(energy_rating, number_habitable_rooms, house_type):
    energy_rating_map = {
        "A/B/C": "A",
        "D/E/F/G": "D"
    }
    rooms_map = {
        "3+": "3",
        "2": "2"
    }
    house_type_map = {
        "Terraced": "Terraced",
        "Semi-detached": "Semi",
        "Detached": "Detached",
    }
    energy_letter = energy_rating_map[energy_rating]
    rooms_number = rooms_map[number_habitable_rooms]
    house_word = house_type_map[house_type]

    loadpath = f"{energy_letter}_{rooms_number}_{house_word}.txt"
    return loadpath


st.set_page_config(page_title='Data Input')
st.title("Data Input")

country = st.selectbox(
   "In which country are you located?",
    ("UK", "US", "Other"),
    index=1,  # Default to UK for demonstration
    help="Select the country where you are located to tailor the input fields accordingly."
)

st.subheader("Solar Data")
st.image("sun3.jpg")
st.markdown("Please provide your latitude and longitude to automatically compute the solar generation profile for your house with PVWatts. Alternatively, you can upload a txt file with hourly solar generation over a year, normalized to 1kW of PV. ")   



# Function to display inputs based on country
def display_inputs_for_country(country):
     # Latitude and Longitude inputs
    latitude = st.number_input("Enter Latitude", value=39.7392, key="latitude")
    longitude = st.number_input("Enter Longitude", value=-104.9903, key="longitude")

    if st.button("Submit"):
        if country == "US":
            fetch_solar_data_from_api(latitude, longitude, "pages/data/solar.txt", 1)
        elif country == "Other" or country == "UK":
            fetch_solar_data_from_api(latitude, longitude, "pages/data/solar.txt", 0)

    upload_file_solar = st.file_uploader("Or Upload Solar Data File", type=['txt'], key="upload_solar")

    st.subheader("Load Data")
    st.image("meter.jpeg")
    # Other inputs
    upload_file = st.file_uploader("Upload a txt file with your hourly load consumption from at least one year:", type=['txt'], key="upload_load")

    
    # Display specific inputs based on the country
    if country == "UK":
        st.write("""
        Please fill out the following information about your house if you are located in the UK and do not have access to historical hourly load data. We will generate your load profile using the Faraday foundation model from the Centre for Net Zero. 
        """)
        energy_rating = st.selectbox(
           "Energy Rating",
            ("A/B/C", "D/E/F/G"),
            help="Select the energy efficiency rating of your house."
        )
        number_habitable_rooms = st.selectbox(
            "Number of Habitable Rooms",
            ("3+", "2"),
            help="Select the number of habitable rooms in the property."
        )
        house_type = st.selectbox(
            "House Type",
            ("Terraced", "Semi-detached", "Detached"),
            help="Select the type of house."
        )


        if st.button('Fetch Load Profile'):
            loadpath = 'pages/data/pre_downloaded_uk_load'
            file_name = get_load_file_path(energy_rating, number_habitable_rooms, house_type)
            full_load_path = os.path.join(loadpath, file_name)

            if os.path.exists(full_load_path):
                st.session_state.full_load_path = full_load_path
                st.success("Load file created")
            else:
                st.error(f"Load profile for the selected inputs not found: {full_load_path}")

    st.subheader("Other Parameters")
    st.markdown("Please provide your desired level of self-consumption. For example, with a level of 50% self consumption you would meet at least 50% of your load from PV generated electricity.")
    desired_self_consumption = st.slider("Desired level of self-consumption (%)", 0, 100, 50, key="desired_self_consumption")
    optional_params = st.expander("Optional Parameters")
    with optional_params:
        desired_robustness = st.slider("Desired robustness of the results (%)", 80, 100, 90, key="desired_robustness")
        max_pv_capacity = st.number_input("Maximum PV capacity on the roof (kW)", value=0.0, key="max_pv_capacity")
        max_battery_capacity = st.number_input("Maximum battery capacity (kWh)", value=0.0, key="max_battery_capacity")
        local_pv_price = st.number_input("Local price of PV per kW ($)", value=0.0, key="local_pv_price")
        local_battery_price = st.number_input("Local price of stationary battery per kWh ($)", value=0.0, key="local_battery_price")
            
        # Store values in session state
        if st.button("Save Inputs"):
            #st.session_state.energy_rating = energy_rating
            #st.session_state.number_habitable_rooms = number_habitable_rooms
            #st.session_state.house_type = house_type
            st.session_state.desired_self_consumption = desired_self_consumption
            st.session_state.desired_robustness = desired_robustness
            st.session_state.max_pv_capacity = max_pv_capacity
            st.session_state.max_battery_capacity = max_battery_capacity
            st.session_state.local_pv_price = local_pv_price
            st.session_state.local_battery_price = local_battery_price
            st.success("Inputs saved successfully")

# Render the appropriate input fields based on the selected country
display_inputs_for_country(country)
