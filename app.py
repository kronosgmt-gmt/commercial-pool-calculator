import streamlit as st
import pandas as pd
from io import StringIO

# Title of the application
st.title("Commercial Pool GPM Calculator")

# Inputs from the user
st.header("Input Data")
unit_count = st.number_input("Unit Count", min_value=0, value=264)
pool_deep_area = st.number_input("Pool Deep Area (square feet)", min_value=0.0, value=1224.0)
sun_shelf_1 = st.number_input("Sun Shelf 1 (square feet)", min_value=0.0, value=0.0)
sun_shelf_2 = st.number_input("Sun Shelf 2 (square feet)", min_value=0.0, value=0.0)
sun_shelf_3 = st.number_input("Sun Shelf 3 (square feet)", min_value=0.0, value=0.0)
sun_shelf_4 = st.number_input("Sun Shelf 4 (square feet)", min_value=0.0, value=0.0)
zero_entry = st.number_input("Zero Entry (square feet)", min_value=0.0, value=0.0)
units_per_living = st.number_input("Units per Living", min_value=0.0, value=4.5)
gpm_factor = st.number_input("GPM Factor", min_value=0.0, value=0.75)
average_depth = st.number_input("Average Depth (feet)", min_value=0.0, value=4.0)
gallons_per_cubic = st.number_input("Gallons per Cubic Foot", min_value=0.0, value=7.48)
design_turnover = st.number_input("Design Turnover (minutes)", min_value=0, value=183)

# Calculate total area
total_area = pool_deep_area + sun_shelf_1 + sun_shelf_2 + sun_shelf_3 + sun_shelf_4 + zero_entry

# Calculations
min_area_required = unit_count * units_per_living
min_flow_rate = unit_count * gpm_factor
cubic_feet = total_area * average_depth
volume = cubic_feet * gallons_per_cubic
flow_rate = volume / design_turnover

# Display results
st.header("Results")
st.write(f"Minimum Area Required: {min_area_required} square feet")
st.write(f"Minimum Flow Rate: {min_flow_rate} GPM")
st.write(f"Total Area: {total_area} square feet")
st.write(f"Volume in Cubic Feet: {cubic_feet}")
st.write(f"Total Volume: {volume} gallons")
st.write(f"Flow Rate: {flow_rate} GPM")

# Create table for download
data = {
    "Project Name": ["Altera Palmetto"],
    "Number of Units": [unit_count],
    f"{unit_count} Unit Count x {units_per_living} Units per Living =": [min_area_required],
    f"{unit_count} Unit Count x {gpm_factor} GPM Factor =": [min_flow_rate],
    f"{pool_deep_area} Pool Deep Area x {average_depth} Average Depth =": [cubic_feet],
    f"{cubic_feet} Cubic Feet x {gallons_per_cubic} Gallons per Cubic =": [volume],
    f"{volume} Volume / {design_turnover} Design Turnover =": [flow_rate],
    "Total Flow Rate": [200.0],  # Example value, adjust as needed
    "Total Area Provided": [total_area],
    "Provided Pool Volume": [volume]
}
df = pd.DataFrame(data)

# Download button
csv = df.to_csv(index=False)
st.download_button(
    label="Download Report as CSV",
    data=csv,
    file_name="pool_size_calculator_report.csv",
    mime="text/csv"
)
