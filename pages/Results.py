import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Set up the page configuration
st.set_page_config(page_title='Results')

# Title of the Streamlit app
st.title("Results")

# Create the DataFrame for the chart data
chart_data = pd.DataFrame({
    "cost": [30000, 28000, 26000, 24000, 22000, 20000, 18000, 16000, 14000, 12000],
    "pv": [20, 18, 16, 14, 12, 10, 8, 6, 4, 2],
    "battery": [30, 26, 22, 18, 14, 10, 6, 2, 0, 0],
    "self-consumption": [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1],
})

# Find recommended values based on minimum cost
recommended = chart_data.loc[chart_data['cost'].idxmin()]
st.write("\n")
st.write("\n")
# Display recommended configuration
st.subheader('Recommended System Configuration')
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
    x="self-consumption", 
    y="cost",
    title="Cost vs Self-Consumption",
    markers=True,  # Adds markers to line points
)

# Add hover data
fig.update_traces(
    mode='markers+lines', 
    hovertemplate='Self-Consumption: %{x}<br>Cost: %{y}<br>PV: %{customdata[0]} kW<br>Battery: %{customdata[1]} kWh',
    customdata=np.stack((chart_data['pv'], chart_data['battery']), axis=-1)
)

# Add x-axis and y-axis labels
fig.update_layout(
    xaxis_title="Self Consumption",
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
