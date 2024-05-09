import streamlit as st
from pathlib import Path
import sys

script_dir = Path(__file__).parent
sys.path.append(str(script_dir))

from utils.ev.ev_simulation_extended import setup_ev_simulation
from utils.ev.merge_trips import process_file


st.set_page_config(page_title='EV Details Input')
st.title("EV Details Input")

with st.form("ev_details_form"):
    # User inputs for EV details
    battery_capacity = st.number_input("Battery Capacity (kWh)", min_value=1.0, value=60.0)
    min_soc = st.slider("Min Desired SoC (%)", 0, 100, 20) / 100  # Convert percentage to decimal
    max_soc = st.slider("Max Desired SoC (%)", 0, 100, 80) / 100  # Convert percentage to decimal
    charging_connectivity = st.selectbox("Charging Connectivity Type", ["Unidirectional", "Bidirectional"])
    consumption = st.number_input("Consumption (Wh/km)", min_value=1.0, value=164.0)

    # Convert user-friendly charging connectivity to boolean or appropriate backend format
    charging_connectivity_bool = True if charging_connectivity == "Bidirectional" else False

    # Define output file path relative to the project or absolute path
    output_file = 'pages/utils/ev/ev_trips.csv'
    num_days = 365  # Set the number of days for the simulation

    # Submit button for the form
    submitted = st.form_submit_button("Submit EV Details")
    if submitted:
        setup_ev_simulation(
            battery_capacity,
           min_soc,
           max_soc,
           consumption,
            num_days,
           output_file
        )
        process_file('pages/utils/ev/ev_trips.csv', 'pages/data/ev.csv')
        st.success("Simulation completed successfully! Check the output file.")