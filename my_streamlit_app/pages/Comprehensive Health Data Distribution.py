import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.title("📊 Comprehensive Health Data Distribution")
st.markdown("---")

# --- Define Path for Data ---
app_directory = os.path.dirname(os.path.abspath(__file__))
# Navigate up one directory to reach the main project folder where UAE_hospitals_data.csv is located
data_directory = os.path.abspath(os.path.join(app_directory, os.pardir))
HOSPITALS_DATA_PATH = os.path.join(data_directory, "UAE_hospitals_data.csv")

# --- Load Data ---
df_hospitals = pd.DataFrame()
if os.path.exists(HOSPITALS_DATA_PATH):
    try:
        df_hospitals = pd.read_csv(HOSPITALS_DATA_PATH)
    except Exception as e:
        st.error(f"Error reading hospital data file: {e}. Please ensure 'UAE_hospitals_data.csv' is in your main project folder.")
else:
    st.error(f"Hospital data file '{os.path.basename(HOSPITALS_DATA_PATH)}' not found. Please ensure it's in your main project folder: `{HOSPITALS_DATA_PATH}`.")

# --- Ensure DataFrame is not empty before proceeding ---
if df_hospitals.empty:
    st.warning("No data loaded to display charts.")
    st.stop() # Stop execution if no data

# --- Sidebar Controls ---
st.sidebar.header("Chart Filters")
selected_year = st.sidebar.selectbox(
    "Select Year for Time-Series Metrics:",
    list(range(2020, 2026)),
    key="pie_chart_year_selector"
)

# --- Helper function to create a Pie Chart ---
def create_pie_chart(df, names_col, values_col, title, hover_data=None):
    if df.empty or names_col not in df.columns or values_col not in df.columns:
        st.warning(f"Cannot create '{title}' chart: Missing '{names_col}' or '{values_col}' column, or empty data.")
        return

    # Aggregate data for the pie chart
    plot_df = df.groupby(names_col)[values_col].sum().reset_index()
    if plot_df.empty:
        st.warning(f"No data to display for '{title}' after aggregation.")
        return

    fig = px.pie(plot_df,
                 names=names_col,
                 values=values_col,
                 title=title,
                 hole=0.3,
                 hover_data=hover_data)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide', margin=dict(t=50, b=0, l=0, r=0))
    st.plotly_chart(fig, use_container_width=True)

# --- Define columns for displaying charts ---
col1, col2, col3 = st.columns(3) # 3 columns for charts

# --- Chart 1: Distribution of Hospitals by State ---
with col1:
    st.subheader("Hospitals by State")
    state_counts = df_hospitals['State'].value_counts().reset_index()
    state_counts.columns = ['State', 'Count']
    create_pie_chart(state_counts, 'State', 'Count', 'Distribution of Hospitals by State')

# --- Chart 2: Distribution of Hospitals by Hospital Rate (Grouped) ---
with col2:
    st.subheader("Hospital Rating Distribution")
    # Group hospital rates into broader categories if they are too granular
    if 'Hospital rate' in df_hospitals.columns:
        # Example: Group rates into bins
        bins = [0, 3.0, 4.0, 5.0]
        labels = ['Below 3.0', '3.0 - 3.9', '4.0 - 5.0']
        df_hospitals['Rating Group'] = pd.cut(df_hospitals['Hospital rate'], bins=bins, labels=labels, right=False)
        rating_counts = df_hospitals['Rating Group'].value_counts().reset_index()
        rating_counts.columns = ['Rating Group', 'Count']
        create_pie_chart(rating_counts, 'Rating Group', 'Count', 'Distribution of Hospital Ratings')
    else:
        st.warning("Column 'Hospital rate' not found for chart.")

# --- Chart 3: Distribution of Patients by State for Selected Year ---
with col3:
    st.subheader(f"Patients by State ({selected_year})")
    patient_col = f'Number of patients in {selected_year}'
    if patient_col in df_hospitals.columns:
        create_pie_chart(df_hospitals, 'State', patient_col, f'Patient Distribution by State in {selected_year}')
    else:
        st.warning(f"Column '{patient_col}' not found for chart.")

# --- New Row of Charts ---
col4, col5, col6 = st.columns(3)

# --- Chart 4: Distribution of Total Cost by State for Selected Year ---
with col4:
    st.subheader(f"Total Cost by State ({selected_year})")
    cost_col = f'total cost of the hospital in {selected_year} (million AED)'
    if cost_col in df_hospitals.columns:
        create_pie_chart(df_hospitals, 'State', cost_col, f'Cost Distribution by State in {selected_year}')
    else:
        st.warning(f"Column '{cost_col}' not found for chart.")

# --- Chart 5: Distribution of Total Income by State for Selected Year ---
with col5:
    st.subheader(f"Total Income by State ({selected_year})")
    income_col = f'total income of the hospital in {selected_year} (million AED)'
    if income_col in df_hospitals.columns:
        create_pie_chart(df_hospitals, 'State', income_col, f'Income Distribution by State in {selected_year}')
    else:
        st.warning(f"Column '{income_col}' not found for chart.")

# --- Chart 6: Distribution of Total Surgeries by State for Selected Year ---
with col6:
    st.subheader(f"Total Surgeries by State ({selected_year})")
    surgeries_col = f'total number of surgeries in {selected_year}'
    if surgeries_col in df_hospitals.columns:
        create_pie_chart(df_hospitals, 'State', surgeries_col, f'Surgeries Distribution by State in {selected_year}')
    else:
        st.warning(f"Column '{surgeries_col}' not found for chart.")

# --- New Row of Charts ---
col7, col8, col9 = st.columns(3)

# --- Chart 7: Overall Review Sentiment (Positive vs. Negative) ---
with col7:
    st.subheader("Overall Review Sentiment")
    if 'positive reviews' in df_hospitals.columns and 'negative reviews' in df_hospitals.columns:
        total_positive = df_hospitals['positive reviews'].sum()
        total_negative = df_hospitals['negative reviews'].sum()
        sentiment_df = pd.DataFrame({
            'Sentiment': ['Positive Reviews', 'Negative Reviews'],
            'Count': [total_positive, total_negative]
        })
        create_pie_chart(sentiment_df, 'Sentiment', 'Count', 'Overall Review Sentiment')
    else:
        st.warning("Columns 'positive reviews' or 'negative reviews' not found for chart.")

# --- Chart 8: Distribution of Doctors by State ---
with col8:
    st.subheader("Doctors by State")
    if 'Number of Doctors' in df_hospitals.columns:
        create_pie_chart(df_hospitals, 'State', 'Number of Doctors', 'Distribution of Doctors by State')
    else:
        st.warning("Column 'Number of Doctors' not found for chart.")

# --- Chart 9: Distribution of Patients by Hospital Rate (Selected Year) ---
with col9:
    st.subheader(f"Patients by Rating ({selected_year})")
    patient_col_rate = f'Number of patients in {selected_year}'
    if 'Hospital rate' in df_hospitals.columns and patient_col_rate in df_hospitals.columns:
        # Group hospital rates into broader categories for this chart too
        bins = [0, 3.0, 4.0, 5.0]
        labels = ['Below 3.0', '3.0 - 3.9', '4.0 - 5.0']
        df_hospitals['Rating Group'] = pd.cut(df_hospitals['Hospital rate'], bins=bins, labels=labels, right=False)
        create_pie_chart(df_hospitals, 'Rating Group', patient_col_rate, f'Patient Distribution by Rating in {selected_year}')
    else:
        st.warning(f"Columns 'Hospital rate' or '{patient_col_rate}' not found for chart.")

# --- Chart 10: Distribution of Treatment Types (Requires splitting and counting) ---
# This chart might be complex if 'Types of treatment it contains' is a comma-separated string.
# We will split it and count occurrences.
st.markdown("---")
st.subheader("Distribution of Treatment Types")
if 'Types of treatment it contains' in df_hospitals.columns:
    # Split the string by comma and stack them to count individual types
    all_treatments = df_hospitals['Types of treatment it contains'].dropna().str.split(',').explode().str.strip()
    if not all_treatments.empty:
        treatment_counts = all_treatments.value_counts().reset_index()
        treatment_counts.columns = ['Treatment Type', 'Count']
        create_pie_chart(treatment_counts, 'Treatment Type', 'Count', 'Overall Distribution of Treatment Types')
    else:
        st.warning("No valid treatment types found in the data.")
else:
    st.warning("Column 'Types of treatment it contains' not found for chart.")


st.markdown("---")
st.write("Explore various distributions within the UAE's healthcare data through interactive pie charts.")