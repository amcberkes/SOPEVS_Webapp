import streamlit as st

# Set page configuration
st.set_page_config(page_title='SOPEVS')

# Page Title
st.title("SOPEVS: Sizing & Operation for PV-EV integrated Single-Family Houses")
st.write("""
Welcome to the SOPEVS! This tool will help you to determine the optimal sizing of solar PV and stationary storage for your single-family house. The sizing results will be computed for different operation policy choices. EV usage and WFH schedules can be taken into account. 
More information on the methodology used can be found in the SOPEVS paper [here](tbd).
There are four main sections in this application:
""")

# File Upload Section Description
st.subheader("1. Data Input")
st.write("""
In the **Data Input** section, we ask you for a few inputs regarding the location and load consumpton of the single-family house.
""")
#st.write("""
#There are additional specifications you can make for the simulation:
#- **PV model type:** tbd.
#- **tbd:** tbd. 

#""")

# Results Section Description
st.subheader("2. EV and WFH inputs")
st.markdown("##### EV")
#st.write("""
#tbd
#""")

st.markdown("##### WFH")
#st.write("""
#tbd
#""")




# Results Section Description
st.subheader("3. Results")
#st.write("""
#tbd
#""")
