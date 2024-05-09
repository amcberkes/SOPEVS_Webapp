import streamlit as st
from streamlit.components.v1 import html

import os
from pathlib import Path
import sys

script_dir = Path(__file__).parent
sys.path.append(str(script_dir))

from utils.uk_load.faraday import fetch_data

from utils.uk_load.faraday_postprocessing import process_files


st.set_page_config(page_title='Data Input')
st.title("Data Input")
st.markdown("Please provide the necessary data for the simulation:")

country = st.selectbox(
    "In which country are you located?",
    ("US", "UK", "Germany"),
    index=1,  # Default to UK for demonstration
    help="Select the country where you are located to tailor the input fields accordingly."
)

st.write("You selected:", country)

# Function to display inputs based on country
def display_inputs_for_country(country):
    # JavaScript to fetch geolocation and update Streamlit session state
    location_html = """
    <button onclick="getLocation()">Detect My Location</button>
    <script>
    function getLocation() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(showPosition, showError);
        } else {
            alert('Geolocation is not supported by this browser.');
        }
    }
    function showPosition(position) {
        // Send the latitude and longitude to Streamlit's session state
        Streamlit.setComponentValue({'latitude': position.coords.latitude, 'longitude': position.coords.longitude});
    }
    function showError(error) {
        switch(error.code) {
            case error.PERMISSION_DENIED:
                alert('User denied the request for Geolocation.');
                break;
            case error.POSITION_UNAVAILABLE:
                alert('Location information is unavailable.');
                break;
            case error.TIMEOUT:
                alert('The request to get user location timed out.');
                break;
            case error.UNKNOWN_ERROR:
                alert('An unknown error occurred.');
                break;
        }
    }
    </script>
    """
    html(location_html, height=50)

    # Check if the latitude and longitude are set in the session state
    if 'latitude' in st.session_state and 'longitude' in st.session_state:
        st.write(f"Detected coordinates: Latitude {st.session_state['latitude']}, Longitude {st.session_state['longitude']}")

    # Other inputs
    upload_file = st.file_uploader("Or upload a txt file with hourly load consumption over a year", type=['txt'])

    # Display specific inputs based on the country
    if country == "UK":
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
            ("Terraced", "Semi-detached", "Detached", "Any House Types"),
            help="Select the type of house."
        )

        if st.button('Fetch Load Profile'):
            fetch_data(energy_rating, number_habitable_rooms, house_type)
            result_message = fetch_data(energy_rating, number_habitable_rooms, house_type)
            st.text(result_message) 
            st.success("Load profile fetched successfully")
            # call post processing 
            input_directory = 'Single_load_files_uk'
            output_directory = '../../data/'
            process_files(input_directory, output_directory)

        desired_self_consumption = st.slider("Desired level of self-consumption (%)", 0, 100, 50)
        optional_params = st.expander("Optional Parameters")
        with optional_params:
            desired_robustness = st.slider("Desired robustness of the results (%)", 80, 100, 90)
            max_pv_capacity = st.number_input("Maximum PV capacity on the roof (kW)", value=0.0)
            max_battery_capacity = st.number_input("Maximum battery capacity (kWh)", value=0.0)
            local_pv_price = st.number_input("Local price of PV per kW ($)", value=0.0)
            local_battery_price = st.number_input("Local price of stationary battery per kWh ($)", value=0.0)

    else:  # US and Germany
        average_monthly_load = st.text_input("Average electricity monthly load for each month of the year in kWh")
        desired_self_consumption = st.slider("Desired level of self-consumption (%)", 0, 100, 50)
        optional_params = st.expander("Optional Parameters")
        with optional_params:
            desired_robustness = st.slider("Desired robustness of the results (%)", 80, 100, 90)
            max_pv_capacity = st.number_input("Maximum PV capacity on the roof (kW)", value=0.0)
            max_battery_capacity = st.number_input("Maximum battery capacity (kWh)", value=0.0)
            local_pv_price = st.number_input("Local price of PV per kW ($)", value=0.0)
            local_battery_price = st.number_input("Local price of stationary battery per kWh ($)", value=0.0)

# Render the appropriate input fields based on the selected country
display_inputs_for_country(country)
