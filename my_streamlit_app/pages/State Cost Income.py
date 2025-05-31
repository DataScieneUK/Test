import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.title("💰 State Cost vs. Income Analysis")
st.markdown("---")

app_directory = os.path.dirname(os.path.abspath(__file__))
data_directory = os.path.abspath(os.path.join(app_directory, os.pardir))
HOSPITALS_DATA_PATH = os.path.join(data_directory, "UAE_hospitals_data.csv")

df_hospitals = pd.DataFrame()
if os.path.exists(HOSPITALS_DATA_PATH):
    try:
        df_hospitals = pd.read_csv(HOSPITALS_DATA_PATH)
    except Exception as e:
        st.error(f"Error reading hospital data file: {e}. Please ensure 'UAE_hospitals_data.csv' is in your main project folder.")
else:
    st.error(f"Hospital data file '{os.path.basename(HOSPITALS_DATA_PATH)}' not found. Please ensure it's in your main project folder: `{HOSPITALS_DATA_PATH}`.")

years = [2020, 2021, 2022, 2023, 2024, 2025]
cost_cols = [f'total cost of the hospital in {year} (million AED)' for year in years]
income_cols = [f'total income of the hospital in {year} (million AED)' for year in years]


required_cols_for_plot = ['State'] + cost_cols + income_cols

if not df_hospitals.empty and all(col in df_hospitals.columns for col in required_cols_for_plot):
    states = df_hospitals['State'].unique().tolist()
    states.sort()

    st.sidebar.header("Select Emirate (State)")
    selected_state = st.sidebar.selectbox(
        "Choose an Emirate to view its trends:",
        states,
        key="state_selector"
    )

    st.subheader(f"Financial Trends in {selected_state} (2020-2025)")

    df_state = df_hospitals[df_hospitals['State'] == selected_state].copy()

    state_costs = [df_state[col].sum() for col in cost_cols]
    state_incomes = [df_state[col].sum() for col in income_cols]
    st.info(state_costs[0])

    plot_df = pd.DataFrame({
        'Year': years,
        'Total Cost (Million AED)': state_costs,
        'Total Income (Million AED)': state_incomes
    })
    st.dataframe(plot_df.head(5))

    fig = px.line(plot_df,
                  x='Year',
                  y=['Total Cost (Million AED)', 'Total Income (Million AED)'],
                  title=f'Hospital Financial Performance in {selected_state}',
                  labels={'value': 'Amount (Million AED)', 'variable': 'Metric'},
                  hover_data={'Total Cost (Million AED)': ':.2f',
                              'Total Income (Million AED)': ':.2f',
                              'Year': True},
                  line_shape="linear"
                 )

    fig.update_xaxes(tickmode='linear', dtick=1)
    fig.update_yaxes(rangemode="tozero")
    fig.update_layout(hovermode="x unified")

    st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("Data is incomplete or required financial columns (e.g., 'total cost of the hospital in 2020 (million AED)') or 'State' column are missing in the hospital data file.")

st.markdown("---")
st.write("Analyze the financial trends of healthcare institutions across different Emirates.")
