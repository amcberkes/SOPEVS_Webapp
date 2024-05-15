import os
import json
import logging
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from utils.worker import run_simulation_sync

# Constants
BINARY_FOLDER = os.getenv("ROBUST_SIZING_BINARY_PATH", "pages/bin/")
SIM = "sim"
SIMULATE_NUM_LOAD_TRACE = 4
SIZING_LOSS_TARGETS = [0.1, 0.3, 0.5, 0.7, 0.9]

# Logging setup
logging.basicConfig(level=logging.DEBUG, filename='simulation.log', filemode='w',
                    format='%(name)s - %(levelname)s - %(message)s')

# Streamlit part
# Set up the page configuration
st.set_page_config(page_title='Results')

# Title of the Streamlit app
st.title("Results")

# Example input data, replace with actual input collection as needed
input_data = {
    "method": "sim",
    "estimation_type": 1,
    "pv_price_per_kw": 2100,
    "battery_price_per_kwh": 480,
    "pv_max_kw": 15,
    "battery_max_kwh": 25,
    "confidence_level": 0.85,
    "days_in_sample": 100,
    "load_file": "pages/data/load.txt",
    "solar_file": "pages/data/solar.txt",
    "max_soc": 0.8,
    "min_soc": 0.2,
    "ev_battery_capacity": 60.0,
    "charging_rate": 7.4,
    "operation_policy": "safe_unidirectional",
    "path_to_ev_data": "pages/data/ev.csv",
    "desired_epsilon": 0.7
}

# Button to run the simulation
if st.button('Run Simulation'):
    results = run_simulation_sync(**input_data)

    # Prepare the DataFrame
    chart_data_list = []
    for res in results:
        if res.get("success") == 1 and res.get("target") != input_data["desired_epsilon"]:
            chart_data_list.append({
                "cost": res.get("total_cost", np.nan),
                "pv": res.get("pv_kw", np.nan),
                "battery": res.get("battery_kwh", np.nan),
                "self_consumption": (1 - res.get("target", np.nan)) * 100  # Convert to percentage
            })

    if not chart_data_list:
        st.error("No successful simulation results to display.")
    else:
        chart_data = pd.DataFrame(chart_data_list)

        # Check if the 'cost' column exists and has valid data
        if 'cost' not in chart_data or chart_data['cost'].isnull().all():
            st.error("Cost data is not available in the simulation results.")
        else:
            # Find recommended values based on minimum cost
            recommended = chart_data.loc[chart_data['cost'].idxmin()]
            st.write("\n")
            st.write("\n")
            # Display recommended configuration
            st.subheader('Recommended System Configuration for at least (1-epsilon)% of electricity consumption met by PV')
            col1, col2, col3 = st.columns(3)
            col1.metric("Recommended PV Size", f"{recommended['pv']} kW")
            col2.metric("Recommended Battery Size", f"{recommended['battery']} kWh")
            col3.metric("Estimated Cost", f"${recommended['cost']:,.0f}")

            # Add spacing between sections
            st.write("\n")  # Add a blank line for more space
            st.write("\n")

            # Using Plotly Express to create an interactive line chart
            fig = px.line(
                chart_data, 
                x="self_consumption", 
                y="cost",
                title="Cost vs Self-Consumption",
                markers=True,  # Adds markers to line points
            )

            # Add hover data
            fig.update_traces(
                mode='markers+lines', 
                hovertemplate='Self-Consumption: %{x:.1f}%<br>Cost: %{y}<br>PV: %{customdata[0]} kW<br>Battery: %{customdata[1]} kWh',
                customdata=np.stack((chart_data['pv'], chart_data['battery']), axis=-1)
            )

            # Add x-axis and y-axis labels
            fig.update_layout(
                xaxis_title="Self-Consumption (%)",
                yaxis_title="Cost ($)",
                hovermode="x unified"
            )

            # Show plot in Streamlit
            st.plotly_chart(fig, use_container_width=True)

            # Convert DataFrame to CSV for download
            csv = chart_data.to_csv(index=False)
            st.download_button(
                label="Download data as CSV",
                data=csv,
                file_name='results_data.csv',
                mime='text/csv',
            )
