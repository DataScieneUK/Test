import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.title("💰 State Cost vs. Income Analysis")
st.markdown("---")

# --- Define Path for Data ---
app_directory = os.path.dirname(os.path.abspath(__file__))
# Navigate up one directory to reach the main project folder where UAE_hospitals_data.csv is located
data_directory = os.path.abspath(os.path.join(app_directory, os.pardir))
HOSPITALS_DATA_PATH = os.path.join(data_directory, "UAE_hospitals_data.csv")

st.info(f"Data directory for hospitals: **`{data_directory}`**")
st.warning(f"Ensure '{os.path.basename(HOSPITALS_DATA_PATH)}' is in this directory.")

# --- Load Data ---
df_hospitals = pd.DataFrame() # Initialize an empty DataFrame
if os.path.exists(HOSPITALS_DATA_PATH):
    try:
        df_hospitals = pd.read_csv(HOSPITALS_DATA_PATH)
        st.success(f"Successfully loaded hospital data from: `{os.path.basename(HOSPITALS_DATA_PATH)}`")
    except Exception as e:
        st.error(f"Error reading hospital data file: {e}")
else:
    st.error(f"Hospital data file '{os.path.basename(HOSPITALS_DATA_PATH)}' not found at: `{HOSPITALS_DATA_PATH}`.")
    st.info("Please ensure 'UAE_hospitals_data.csv' is in your main project folder.")

# Check if DataFrame is loaded and has essential columns
required_cols_for_plot = ['State'] + \
                         [f'total cost of the hospital in {year} (million AED)' for year in range(2020, 2026)] + \
                         [f'total income of the hospital in {year} (million AED)' for year in range(2020, 2026)]

if not df_hospitals.empty and all(col in df_hospitals.columns for col in required_cols_for_plot):

    # Get unique states for sidebar selection
    states = df_hospitals['State'].unique().tolist()
    states.sort() # Sort states alphabetically

    # --- Sidebar Selection for State ---
    st.sidebar.header("Select Emirate (State)")
    selected_state = st.sidebar.selectbox(
        "Choose an Emirate to view its trends:",
        states,
        key="state_selector" # Unique key for this widget
    )

    st.subheader(f"Cost & Income Trends for: {selected_state}")

    # Filter data for the selected state
    df_state = df_hospitals[df_hospitals['State'] == selected_state].copy()

    # Aggregate data by summing up for the selected state
    # This sums up costs/incomes from all hospitals within that state
    state_costs = [df_state[f'total cost of the hospital in {year} (million AED)'].sum() for year in range(2020, 2026)]
    state_incomes = [df_state[f'total income of the hospital in {year} (million AED)'].sum() for year in range(2020, 2026)]
    years = list(range(2020, 2026))

    # Create a DataFrame for plotting
    plot_df = pd.DataFrame({
        'Year': years,
        'Total Cost (Million AED)': state_costs,
        'Total Income (Million AED)': state_incomes
    })

    # --- Create Interactive Line Plot with Plotly ---
    fig = px.line(plot_df,
                  x='Year',
                  y=['Total Cost (Million AED)', 'Total Income (Million AED)'], # Plot both cost and income
                  title=f'Hospital Financial Performance in {selected_state} (2020-2025)',
                  labels={'value': 'Amount (Million AED)', 'variable': 'Metric'}, # Label axes and legend
                  hover_data={'Total Cost (Million AED)': ':.2f', # Format hover text
                              'Total Income (Million AED)': ':.2f',
                              'Year': True}, # Show year on hover
                  line_shape="linear" # Options: "linear", "hv", "vh", "spline"
                 )

    fig.update_xaxes(tickmode='linear', dtick=1) # Ensure all years are shown as ticks
    fig.update_yaxes(rangemode="tozero") # Start y-axis from zero
    fig.update_layout(hovermode="x unified") # Show unified hover tooltip across both lines

    st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("Data is incomplete or required columns (State, Cost/Income for years) are missing in the hospital data file.")
    st.info("Please check your 'UAE_hospitals_data.csv' to ensure it has the correct columns and data.")

st.markdown("---")
st.write("Analyze the financial trends of healthcare institutions across different Emirates.")