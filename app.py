import streamlit as st
import pandas as pd
import numpy as np

# Custom CSS for dark mode appearance
st.markdown(
    """
    <style>
    .stApp {
        background-color: #1a1a1a;
        color: #e0e0e0;
        padding: 20px;
    }
    .st-header {
        color: #a3bffa;
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .st-subheader {
        color: #b0b0b0;
        font-size: 20px;
        margin-top: 15px;
    }
    .st-table {
        background-color: #2d2d2d;
        border-radius: 5px;
        padding: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
        color: #e0e0e0;
    }
    .st-table th, .st-table td {
        border-color: #444444;
    }
    .st-download-button {
        background-color: #4dabf7;
        color: white;
        padding: 10px 20px;
        border-radius: 5px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
    }
    .st-download-button:hover {
        background-color: #339af0;
    }
    input, select, textarea {
        background-color: #333333;
        color: #e0e0e0;
        border: 1px solid #555555;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Page configuration
st.set_page_config(
    page_title="Commercial Pool GPM Calculator",
    page_icon="🏊",
    layout="wide"
)

# Title and description
st.title("Commercial Pool GPM Calculator")
st.markdown("""
This application calculates the Gallons Per Minute (GPM) for commercial pools. 
Enter the required parameters in the sidebar and review the results or download a report.
""")

# Sidebar for input parameters
st.sidebar.header("Pool Parameters")

# Input parameters
with st.sidebar:
    col1, col2 = st.columns(2)
    
    with col1:
        unit_count = st.number_input("Unit Count", min_value=0, value=0)
        pool_deep_area = st.number_input("Pool Deep Area (sq ft)", min_value=0.0, value=0.0)
        sun_shelf_area = st.number_input("Total Sun Shelf Area (sq ft)", min_value=0.0, value=0.0)
        zero_entry_area = st.number_input("Zero Entry Area (sq ft)", min_value=0.0, value=0.0)

    with col2:
        average_depth_deep = st.number_input("Avg Depth Deep Pool (ft)", min_value=0.0, value=0.0)
        average_depth_sun = st.number_input("Avg Depth Sun Shelf (ft)", min_value=0.0, value=0.0)
        average_depth_zero = st.number_input("Avg Depth Zero Entry (ft)", min_value=0.0, value=0.0)
        deep_turnover = st.number_input("Deep Turnover (minutes)", min_value=0, value=0)
        sun_turnover = st.number_input("Sun Shelf Turnover (minutes)", min_value=0, value=60)
        zero_entry_turnover = st.number_input("Zero Entry Turnover (minutes)", min_value=0, value=120)

# Fixed conversion factors (moved to calculations)
units_per_living = 4.5
gpm_factor = 0.75
gallons_per_cubic = 7.48

# Tabs for different sections
tab1, tab2, tab3 = st.tabs(["Input Data", "Results", "Reports"])

with tab1:
    st.header("Input Data")
    st.write("Adjust the parameters in the sidebar to configure the pool data.")
    if st.button("Calculate", type="primary"):
        st.session_state['params'] = {
            'unit_count': unit_count,
            'pool_deep_area': pool_deep_area,
            'sun_shelf_area': sun_shelf_area,
            'zero_entry_area': zero_entry_area,
            'average_depth_deep': average_depth_deep,
            'average_depth_sun': average_depth_sun,
            'average_depth_zero': average_depth_zero,
            'deep_turnover': deep_turnover,
            'sun_turnover': sun_turnover,
            'zero_entry_turnover': zero_entry_turnover
        }
        st.session_state['calculated'] = True
        st.success("Calculation triggered. View results in the 'Results' tab.")

with tab2:
    st.header("Results")
    if 'calculated' not in st.session_state or not st.session_state['calculated']:
        st.info("Please calculate the results in the 'Input Data' tab first.")
    else:
        params = st.session_state['params']
        
        # Calculations for Deep Pool
        min_area_required = params['unit_count'] * units_per_living
        min_flow_rate = params['unit_count'] * gpm_factor
        cubic_feet_deep = params['pool_deep_area'] * params['average_depth_deep']
        volume_deep = cubic_feet_deep * gallons_per_cubic
        flow_rate_deep = volume_deep / params['deep_turnover']

        # Debug output for Deep Pool
        st.write("**Debug - Deep Pool Calculation:**")
        st.write(f"Cubic Feet: {cubic_feet_deep:.2f}")
        st.write(f"Volume (Gallons): {volume_deep:.2f}")
        st.write(f"Flow Rate (GPM): {flow_rate_deep:.2f}")

        # Calculations for Sun Shelf
        cubic_feet_sun = params['sun_shelf_area'] * params['average_depth_sun']
        volume_sun = cubic_feet_sun * gallons_per_cubic
        flow_rate_sun = volume_sun / params['sun_turnover']

        # Calculations for Zero Entry
        cubic_feet_zero = params['zero_entry_area'] * params['average_depth_zero']
        volume_zero = cubic_feet_zero * gallons_per_cubic
        flow_rate_zero = volume_zero / params['zero_entry_turnover']

        # Total calculations
        total_flow_rate = flow_rate_deep + flow_rate_sun + flow_rate_zero
        total_area = params['pool_deep_area'] + params['sun_shelf_area'] + params['zero_entry_area']
        total_volume = volume_deep + volume_sun + volume_zero

        # Display results in tables with two decimal places
        st.markdown('<div class="st-subheader">Pool Size Calculator Deep End</div>', unsafe_allow_html=True)
        deep_data = {
            "": ["", "", f"{params['pool_deep_area']:.2f} AREA", f"{cubic_feet_deep:.2f} CUBIC FEET", f"{volume_deep:.2f} VOLUME", ""],
            "": ["", "", "x", "x", "/", ""],
            "": ["", "", f"{params['average_depth_deep']:.2f} AVERAGE DEPTH", f"{gallons_per_cubic:.2f} GALLONS PER CUBIC FEET", f"{params['deep_turnover']} DESIGN TURNOVER IN MINUTES", ""],
            "": ["", "", "", "", "=", f"{flow_rate_deep:.2f} FLOW RATE"]
        }
        df_deep = pd.DataFrame(deep_data)
        st.markdown('<div class="st-table">', unsafe_allow_html=True)
        st.table(df_deep)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="st-subheader">Sun Shelf Calculator #1</div>', unsafe_allow_html=True)
        sun_data = {
            "": ["", f"{params['sun_shelf_area']:.2f} SUN SHELVES AREA", f"{cubic_feet_sun:.2f} CUBIC FEET", f"{volume_sun:.2f} VOLUME", ""],
            "": ["", "x", "x", "/", ""],
            "": ["", f"{params['average_depth_sun']:.2f} AVERAGE DEPTH", f"{gallons_per_cubic:.2f} GALLONS PER CUBIC FEET", f"{params['sun_turnover']} TURNOVER IN MINUTES", ""],
            "": ["", "", "", "=", f"{flow_rate_sun:.2f} MIN FLOW RATE"]
        }
        df_sun = pd.DataFrame(sun_data)
        st.markdown('<div class="st-table">', unsafe_allow_html=True)
        st.table(df_sun)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="st-subheader">Zero Entry Calculator</div>', unsafe_allow_html=True)
        zero_data = {
            "": ["", f"{params['zero_entry_area']:.2f} ZERO ENTRY AREA", f"{cubic_feet_zero:.2f} CUBIC FEET", f"{volume_zero:.2f} VOLUME", ""],
            "": ["", "x", "x", "/", ""],
            "": ["", f"{params['average_depth_zero']:.2f} AVERAGE DEPTH", f"{gallons_per_cubic:.2f} GALLONS PER CUBIC FEET", f"{params['zero_entry_turnover']} TURNOVER IN MINUTES", ""],
            "": ["", "", "", "=", f"{flow_rate_zero:.2f} MIN FLOW RATE"]
        }
        df_zero = pd.DataFrame(zero_data)
        st.markdown('<div class="st-table">', unsafe_allow_html=True)
        st.table(df_zero)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="st-subheader">Total</div>', unsafe_allow_html=True)
        total_data = {
            "TOTAL FLOW RATE": [f"{total_flow_rate:.2f}", "MIN FLOW RATE REQ'D"],
            "TOTAL AREA PROVIDED": [f"{total_area:.2f}", "MIN AREA REQUIRED"],
            "VOLUME POOL": [f"{volume_deep:.2f}", ""],
            "VOLUME SUNSHELF": [f"{volume_sun:.2f}", ""],
            "VOLUME ZERO ENTRY": [f"{volume_zero:.2f}", ""],
            "TOTAL VOLUME": [f"{total_volume:.2f}", ""]
        }
        df_total = pd.DataFrame(total_data)
        st.markdown('<div class="st-table">', unsafe_allow_html=True)
        st.table(df_total)
        st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.header("Reports")
    if 'calculated' not in st.session_state or not st.session_state['calculated']:
        st.info("Please calculate the results in the 'Input Data' tab first.")
    else:
        params = st.session_state['params']
        # Calculations (same as in Results tab for consistency)
        cubic_feet_deep = params['pool_deep_area'] * params['average_depth_deep']
        volume_deep = cubic_feet_deep * gallons_per_cubic
        flow_rate_deep = volume_deep / params['deep_turnover']
        cubic_feet_sun = params['sun_shelf_area'] * params['average_depth_sun']
        volume_sun = cubic_feet_sun * gallons_per_cubic
        flow_rate_sun = volume_sun / params['sun_turnover']
        cubic_feet_zero = params['zero_entry_area'] * params['average_depth_zero']
        volume_zero = cubic_feet_zero * gallons_per_cubic
        flow_rate_zero = volume_zero / params['zero_entry_turnover']
        total_flow_rate = flow_rate_deep + flow_rate_sun + flow_rate_zero
        total_area = params['pool_deep_area'] + params['sun_shelf_area'] + params['zero_entry_area']
        total_volume = volume_deep + volume_sun + volume_zero

        # CSV data for download with two decimal places
        csv_data = {
            "Project Name": ["Summerlit"],
            "Number of Units": [params['unit_count']],
            f"{params['unit_count']} Unit Count x {units_per_living} Units per Living =": [np.round(params['unit_count'] * units_per_living, 2)],
            f"{params['unit_count']} Unit Count x {gpm_factor} GPM Factor =": [np.round(params['unit_count'] * gpm_factor, 2)],
            f"{params['pool_deep_area']} Pool Deep Area x {params['average_depth_deep']} Avg Depth =": [np.round(cubic_feet_deep, 2)],
            f"{cubic_feet_deep:.2f} Cubic Feet x {gallons_per_cubic} Gallons per Cubic =": [np.round(volume_deep, 2)],
            f"{volume_deep:.2f} Volume / {params['deep_turnover']} Design Turnover =": [np.round(flow_rate_deep, 2)],
            f"{params['sun_shelf_area']} Sun Shelves Area x {params['average_depth_sun']} Avg Depth =": [np.round(cubic_feet_sun, 2)],
            f"{cubic_feet_sun:.2f} Cubic Feet x {gallons_per_cubic} Gallons per Cubic =": [np.round(volume_sun, 2)],
            f"{volume_sun:.2f} Volume / {params['sun_turnover']} Turnover =": [np.round(flow_rate_sun, 2)],
            f"{params['zero_entry_area']} Zero Entry Area x {params['average_depth_zero']} Avg Depth =": [np.round(cubic_feet_zero, 2)],
            f"{cubic_feet_zero:.2f} Cubic Feet x {gallons_per_cubic} Gallons per Cubic =": [np.round(volume_zero, 2)],
            f"{volume_zero:.2f} Volume / {params['zero_entry_turnover']} Turnover =": [np.round(flow_rate_zero, 2)],
            "Total Flow Rate": [np.round(total_flow_rate, 2)],
            "Total Area Provided": [np.round(total_area, 2)],
            "Volume Pool": [np.round(volume_deep, 2)],
            "Volume Sun Shelf": [np.round(volume_sun, 2)],
            "Volume Zero Entry": [np.round(volume_zero, 2)],
            "Total Volume": [np.round(total_volume, 2)]
        }
        df_csv = pd.DataFrame(csv_data)
        csv = df_csv.to_csv(index=False)
        st.download_button(
            label="Download Report as CSV",
            data=csv,
            file_name="pool_gpm_report.csv",
            mime="text/csv",
            key="download-csv"
        )
        st.dataframe(df_csv, hide_index=True)
