import streamlit as st
import pandas as pd

# Title of the application
st.title("Commercial Pool GPM Calculator")

# Inputs from the user
st.header("Input Data")
unit_count = st.number_input("Unit Count", min_value=0, value=242)
pool_deep_area = st.number_input("Pool Deep Area (square feet)", min_value=0.0, value=2067.0)
sun_shelf_area = st.number_input("Total Sun Shelf Area (square feet)", min_value=0.0, value=299.0)
units_per_living = st.number_input("Units per Living", min_value=0.0, value=4.5)
gpm_factor = st.number_input("GPM Factor", min_value=0.0, value=0.75)
average_depth_deep = st.number_input("Average Depth Deep Pool (feet)", min_value=0.0, value=4.0)
average_depth_sun = st.number_input("Average Depth Sun Shelf (feet)", min_value=0.0, value=0.75)
gallons_per_cubic = st.number_input("Gallons per Cubic Foot", min_value=0.0, value=7.48)

# Fixed turnover times
deep_turnover = st.number_input("deep turnover", min_value=0, value=180)  # minutes for deep pool
sun_turnover = 60    # minutes for sun shelves
zero_entry_turnover = 120 # minutes for zero entries

# Calculations for Deep Pool
min_area_required = unit_count * units_per_living
min_flow_rate = unit_count * gpm_factor
cubic_feet_deep = pool_deep_area * average_depth_deep
volume_deep = cubic_feet_deep * gallons_per_cubic
flow_rate_deep = volume_deep / deep_turnover

# Calculations for Sun Shelf
cubic_feet_sun = sun_shelf_area * average_depth_sun
volume_sun = cubic_feet_sun * gallons_per_cubic
flow_rate_sun = volume_sun / sun_turnover

# Total calculations
total_flow_rate = flow_rate_deep + flow_rate_sun
total_area = pool_deep_area + sun_shelf_area
total_volume = volume_deep + volume_sun

# Display results in tables
st.header("Results")

# Deep Pool Table
st.subheader("Pool Size Calculator Deep End")
deep_data = {
    "": ["", "", f"{pool_deep_area} AREA", f"{cubic_feet_deep} CUBIC FEET", f"{volume_deep} VOLUME", ""],
    "": ["", "", "x", "x", "/", ""],
    "": ["", "", f"{average_depth_deep} AVERAGE DEPTH", f"{gallons_per_cubic} GALLONS PER CUBIC FEET", f"{deep_turnover} DESIGN TURNOVER IN MINUTES", ""],
    "": ["", "", "", "", "=", f"{flow_rate_deep} FLOW RATE"]
}
df_deep = pd.DataFrame(deep_data)
st.table(df_deep)

# Sun Shelf Table
st.subheader("Sun Shelf Calculator #1")
sun_data = {
    "": ["", f"{sun_shelf_area} SUN SHELVES AREA", f"{cubic_feet_sun} CUBIC FEET", f"{volume_sun} VOLUME", ""],
    "": ["", "x", "x", "/", ""],
    "": ["", f"{average_depth_sun} AVERAGE DEPTH", f"{gallons_per_cubic} GALLONS PER CUBIC FEET", f"{sun_turnover} TURNOVER IN MINUTES", ""],
    "": ["", "", "", "=", f"{flow_rate_sun} MIN FLOW RATE"]
}
df_sun = pd.DataFrame(sun_data)
st.table(df_sun)

# Total Table
st.subheader("Total")
total_data = {
    "TOTAL FLOW RATE": [f"{total_flow_rate}", "MIN FLOW RATE REQ'D"],
    "TOTAL AREA PROVIDED": [f"{total_area}", "MIN AREA REQUIRED"],
    "VOLUME POOL": [f"{volume_deep}", ""],
    "VOLUME SUNSHELF 1": [f"{volume_sun}", ""],
    "TOTAL VOLUME": [f"{total_volume}", ""]
}
df_total = pd.DataFrame(total_data)
st.table(df_total)

# Download button
csv_data = {
    "Project Name": ["Summerlit"],
    "Number of Units": [unit_count],
    f"{unit_count} Unit Count x {units_per_living} Units per Living =": [min_area_required],
    f"{unit_count} Unit Count x {gpm_factor} GPM Factor =": [min_flow_rate],
    f"{pool_deep_area} Pool Deep Area x {average_depth_deep} Average Depth =": [cubic_feet_deep],
    f"{cubic_feet_deep} Cubic Feet x {gallons_per_cubic} Gallons per Cubic =": [volume_deep],
    f"{volume_deep} Volume / {deep_turnover} Design Turnover =": [flow_rate_deep],
    f"{sun_shelf_area} Sun Shelves Area x {average_depth_sun} Average Depth =": [cubic_feet_sun],
    f"{cubic_feet_sun} Cubic Feet x {gallons_per_cubic} Gallons per Cubic =": [volume_sun],
    f"{volume_sun} Volume / {sun_turnover} Turnover =": [flow_rate_sun],
    "Total Flow Rate": [total_flow_rate],
    "Total Area Provided": [total_area],
    "Volume Pool": [volume_deep],
    "Volume Sun Shelf": [volume_sun],
    "Total Volume": [total_volume]
}
df_csv = pd.DataFrame(csv_data)
csv = df_csv.to_csv(index=False)
st.download_button(
    label="Download Report as CSV",
    data=csv,
    file_name="pool_size_calculator_report.csv",
    mime="text/csv"
)
