import streamlit as st

import os
from pathlib import Path
import sys

script_dir = Path(__file__).parent
sys.path.append(str(script_dir))

from utils.ev.ev_simulation_extended import setup_ev_simulation
from utils.ev.merge_trips import fetch_data

st.set_page_config(page_title='EV & WFH Input')
st.title("EV & WFH Input")

# Dictionary to map number of EVs from words to numbers
ev_mapping = {
    "None": 0,
    "One": 1,
    "Two": 2,
    "Three": 3
}

# Check if the number of EVs has been set in the session state
if 'num_evs' not in st.session_state:
    st.session_state.num_evs = 'None'  # Default value

# Create a select box and update session state
num_evs = st.selectbox(
    "How many EVs do you have?",
    ("None", "One", "Two", "Three"),
    index=0,
    help="Select the number of electric vehicles you own."
)

st.session_state.num_evs = num_evs  # Update session state

# Convert num_evs to an integer using the mapping
num_evs_int = ev_mapping[num_evs]

# Conditional display based on the number of EVs
if num_evs_int == 0:
    if st.button("Go to Results"):
        st.write("Redirecting to results...")  # This can link to another page or action
else:
    with st.form("ev_details_form"):
        ev_details = {}
        for i in range(num_evs_int):
            st.subheader(f"EV {i+1} Details")
            battery_capacity = st.number_input(f"EV {i+1} Battery Capacity (kWh)", min_value=1.0, value=60.0)
            min_soc = st.slider(f"EV {i+1} Min Desired SoC (%)", 0, 100, 20)
            max_soc = st.slider(f"EV {i+1} Max Desired SoC (%)", 0, 100, 80)
            charging_connectivity = st.selectbox(f"EV {i+1} Charging Connectivity Type", ["Unidirectional", "Bidirectional"])
            charging_capacity = st.number_input(f"EV {i+1} Charging Capacity (kW)", min_value=0.1, value=7.4)
            charging_preference = st.selectbox(
                f"EV {i+1} Charging Preference",
                ["Always charge as soon as possible",
                 "Efficient EV charging with high SOC level at departure",
                 "Efficient EV charging with no strong guarantees about the SOC at departure"]
            )
            ev_details[f"ev_{i+1}"] = {
                "battery_capacity": battery_capacity,
                "min_soc": min_soc,
                "max_soc": max_soc,
                "charging_connectivity": charging_connectivity,
                "charging_capacity": charging_capacity,
                "charging_preference": charging_preference
            }
        
        if st.form_submit_button("Submit EV Details"):
            st.session_state.ev_details = ev_details  # Save data into session state
            st.success("Details Saved Successfully!")

# call BE ev files to create ev input file and store it in data/
#call ev_simulation_extended.py
# Example parameters
battery_capacity = 40
min_soc = 0.2
max_soc = 0.8
charging_capacity = 22
charging_connectivity = True
charging_preference = 'Home'
num_days = 365
output_file = 'ev_trips.csv'

# Call the function with the parameters
setup_ev_simulation(battery_capacity, min_soc, max_soc, charging_capacity, charging_connectivity, charging_preference, num_days, output_file)
#call merge_trips.py


# Optionally, add a button to navigate manually if needed
if st.button('Go to Results Page'):
    st.write("Navigating to results...")  # Placeholder for navigation logic
