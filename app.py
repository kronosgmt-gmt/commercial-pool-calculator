import streamlit as st
import pandas as pd

# Custom CSS for better appearance
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f0f2f6;
        padding: 20px;
    }
    .st-header {
        color: #1e3a8a;
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .st-subheader {
        color: #4b5563;
        font-size: 20px;
        margin-top: 15px;
    }
    .st-table {
        background-color: white;
        border-radius: 5px;
        padding: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    .st-download-button {
        background-color: #3b82f6;
        color: white;
        padding: 10px 20px;
        border-radius: 5px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
    }
    .st-download-button:hover {
        background-color: #2563eb;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title of the application
st.title("Commercial Pool GPM Calculator")

# Inputs from the user in columns for better layout
st.markdown('<div class="st-header">Input Data</div>', unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    unit_count = st.number_input("Unit Count", min_value=0, value=242)
    pool_deep_area = st.number_input("Pool Deep Area (square feet)", min_value=0.0, value=2067.0)
    sun_shelf_area = st.number_input("Total Sun Shelf Area (square feet)", min_value=0.0, value=299.0)
    zero_entry_area = st.number_input("Zero Entry Area (square feet)", min_value=0.0, value=0.0)

with col2:
    units_per_living = st.number_input("Units per Living", min_value=0.0, value=4.5)
    gpm_factor = st.number_input("GPM Factor", min_value=0.0, value=0.75)
    average_depth_deep = st.number_input("Average Depth Deep Pool (feet)", min_value=0.0, value=4.0)
    average_depth_sun = st.number_input("Average Depth Sun Shelf (feet)", min_value=0.0, value=0.75)
    average_depth_zero = st.number_input("Average Depth Zero Entry (feet)", min_value=0.0, value=0.5)
    gallons_per_cubic = st.number_input("Gallons per Cubic Foot", min_value=0.0, value=7.48)
    deep_turnover = st.number_input("Deep Turnover (minutes)", min_value=0, value=180)
    sun_turnover = st.number_input("Sun Shelf Turnover (minutes)", min_value=0, value=60)
    zero_entry_turnover = st.number_input("Zero Entry Turnover (minutes)", min_value=0, value=120)

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

# Calculations for Zero Entry
cubic_feet_zero = zero_entry_area * average_depth_zero
volume_zero = cubic_feet_zero * gallons_per_cubic
flow_rate_zero = volume_zero / zero_entry_turnover

# Total calculations
total_flow_rate = flow_rate_deep + flow_rate_sun + flow_rate_zero
total_area = pool_deep_area + sun_shelf_area + zero_entry_area
total_volume = volume_deep + volume_sun + volume_zero

# Display results in tables
st.markdown('<div class="st-header">Results</div>', unsafe_allow_html=True)

# Deep Pool Table
st.markdown('<div class="st-subheader">Pool Size Calculator Deep End</div>', unsafe_allow_html=True)
deep_data = {
    "": ["", "", f"{pool_deep_area} AREA", f"{cubic_feet_deep} CUBIC FEET", f"{volume_deep} VOLUME", ""],
    "": ["", "", "x", "x", "/", ""],
    "": ["", "", f"{average_depth_deep} AVERAGE DEPTH", f"{gallons_per_cubic} GALLONS PER CUBIC FEET", f"{deep_turnover} DESIGN TURNOVER IN MINUTES", ""],
    "": ["", "", "", "", "=", f"{flow_rate_deep} FLOW RATE"]
}
df_deep = pd.DataFrame(deep_data)
st.markdown('<div class="st-table">', unsafe_allow_html=True)
st.table(df_deep)
st.markdown('</div>', unsafe_allow_html=True)

# Sun Shelf Table
st.markdown('<div class="st-subheader">Sun Shelf Calculator #1</div>', unsafe_allow_html=True)
sun_data = {
    "": ["", f"{sun_shelf_area} SUN SHELVES AREA", f"{cubic_feet_sun} CUBIC FEET", f"{volume_sun} VOLUME", ""],
    "": ["", "x", "x", "/", ""],
    "": ["", f"{average_depth_sun} AVERAGE DEPTH", f"{gallons_per_cubic} GALLONS PER CUBIC FEET", f"{sun_turnover} TURNOVER IN MINUTES", ""],
    "": ["", "", "", "=", f"{flow_rate_sun} MIN FLOW RATE"]
}
df_sun = pd.DataFrame(sun_data)
st.markdown('<div class="st-table">', unsafe_allow_html=True)
st.table(df_sun)
st.markdown('</div>', unsafe_allow_html=True)

# Zero Entry Table
st.markdown('<div class="st-subheader">Zero Entry Calculator</div>', unsafe_allow_html=True)
zero_data = {
    "": ["", f"{zero_entry_area} ZERO ENTRY AREA", f"{cubic_feet_zero} CUBIC FEET", f"{volume_zero} VOLUME", ""],
    "": ["", "x", "x", "/", ""],
    "": ["", f"{average_depth_zero} AVERAGE DEPTH", f"{gallons_per_cubic} GALLONS PER CUBIC FEET", f"{zero_entry_turnover} TURNOVER IN MINUTES", ""],
    "": ["", "", "", "=", f"{flow_rate_zero} MIN FLOW RATE"]
}
df_zero = pd.DataFrame(zero_data)
st.markdown('<div class="st-table">', unsafe_allow_html=True)
st.table(df_zero)
st.markdown('</div>', unsafe_allow_html=True)

# Total Table
st.markdown('<div class="st-subheader">Total</div>', unsafe_allow_html=True)
total_data = {
    "TOTAL FLOW RATE": [f"{total_flow_rate}", "MIN FLOW RATE REQ'D"],
    "TOTAL AREA PROVIDED": [f"{total_area}", "MIN AREA REQUIRED"],
    "VOLUME POOL": [f"{volume_deep}", ""],
    "VOLUME SUNSHELF": [f"{volume_sun}", ""],
    "VOLUME ZERO ENTRY": [f"{volume_zero}", ""],
    "TOTAL VOLUME": [f"{total_volume}", ""]
}
df_total = pd.DataFrame(total_data)
st.markdown('<div class="st-table">', unsafe_allow_html=True)
st.table(df_total)
st.markdown('</div>', unsafe_allow_html=True)

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
    f"{zero_entry_area} Zero Entry Area x {average_depth_zero} Average Depth =": [cubic_feet_zero],
    f"{cubic_feet_zero} Cubic Feet x {gallons_per_cubic} Gallons per Cubic =": [volume_zero],
    f"{volume_zero} Volume / {zero_entry_turnover} Turnover =": [flow_rate_zero],
    "Total Flow Rate": [total_flow_rate],
    "Total Area Provided": [total_area],
    "Volume Pool": [volume_deep],
    "Volume Sun Shelf": [volume_sun],
    "Volume Zero Entry": [volume_zero],
    "Total Volume": [total_volume]
}
df_csv = pd.DataFrame(csv_data)
csv = df_csv.to_csv(index=False)
st.markdown('<div class="st-download-button">', unsafe_allow_html=True)
st.download_button(
    label="Download Report as CSV",
    data=csv,
    file_name="pool_size_calculator_report.csv",
    mime="text/csv"
)
st.markdown('</div>', unsafe_allow_html=True)
