import streamlit as st

# Set page configuration
st.set_page_config(page_title='SOPEVS')

st.markdown("<h1 style='text-align: center;'>SOPEVS</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Solar PV and Stationary Storage Sizing Tool for Single-Family Houses</h3>", unsafe_allow_html=True)



# Add Image
st.image("house.png")

st.write("""
Welcome to the SOPEVS! This tool will help you to determine the optimal sizing of solar PV and stationary storage for your single-family house. 
""")
st.write("""It is the first sizing algorithm that takes on such a personalised approach and also takes into account unidirectional and bidirectional electric vehicles (EVs). The sizing results will be computed for different operation policy choices, to show the user the benefits of different home energy management system paradigms and give suggestions for potential improvements (like getting a bidirectional charger or leaving your EV at home for certain days). 
SOPEVS can also take into account your electric vehicle usage and Work-From-Home schedules. This allwos to optimise the operation strategy towards personalised user lifestyles.
""")

st.write("""
SOPEVS was developed by researchers at the University of Cambridge. More information on the methodology used can be found in the SOPEVS paper [here](www.anaïsberkes.com).
There are three main sections in this application:
""")

# File Upload Section Description
st.subheader("1. Data Input")
st.write("""
In the **Data Input** section, we ask you for a few inputs regarding the location and load consumption of the single-family house.
""")
st.write(""" SOPEVS can be used for single-family houses in any location in the world if historical hourly load data for a minimum of one year is available. The tool can also be used for any UK house that does not direct access to historical load data, as the tool has a built-in load profile generator for UK homes. This profile-generator is based on the Faraday foundation model from the Centre for Net Zero from Octopus Energy. 
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
