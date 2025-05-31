import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.title("📈 Detailed Scatter Plot Analysis")
st.markdown("---")

app_directory = os.path.dirname(os.path.abspath(__file__))
data_directory = os.path.abspath(os.path.join(app_directory, os.pardir))
HOSPITALS_DATA_PATH = os.path.join(data_directory, "UAE_hospitals_data.csv")

df_hospitals = pd.DataFrame()
if os.path.exists(HOSPITALS_DATA_PATH):
    try:
        df_hospitals = pd.read_csv(HOSPITALS_DATA_PATH)
        if 'Hospital rate' in df_hospitals.columns:
            df_hospitals['Hospital rate'] = pd.to_numeric(df_hospitals['Hospital rate'], errors='coerce')
        
        # Convert numerical columns to numeric, coercing errors, where relevant for plotting
        numerical_cols_to_convert = [
            'Number of Doctors', 'Number of patients in 2020', 'Number of patients in 2021',
            'Number of patients in 2022', 'Number of patients in 2023', 'Number of patients in 2024',
            'Number of patients in 2025', 'total cost of the hospital in 2020 (million AED)',
            'total cost of the hospital in 2021 (million AED)', 'total cost of the hospital in 2022 (million AED)',
            'total cost of the hospital in 2023 (million AED)', 'total cost of the hospital in 2024 (million AED)',
            'total cost of the hospital in 2025 (million AED)', 'total income of the hospital in 2020 (million AED)',
            'total income of the hospital in 2021 (million AED)', 'total income of the hospital in 2022 (million AED)',
            'total income of the hospital in 2023 (million AED)', 'total income of the hospital in 2024 (million AED)',
            'total income of the hospital in 2025 (million AED)', 'total number of surgeries in 2020',
            'total number of surgeries in 2021', 'total number of surgeries in 2022', 'total number of surgeries in 2023',
            'total number of surgeries in 2024', 'total number of surgeries in 2025',
            'number of customers make reviews for the hospital', 'number of reviews',
            'positive reviews', 'negative reviews'
        ]
        for col in numerical_cols_to_convert:
            if col in df_hospitals.columns:
                df_hospitals[col] = pd.to_numeric(df_hospitals[col], errors='coerce')

    except Exception as e:
        st.error(f"Error reading hospital data file: {e}. Please ensure 'UAE_hospitals_data.csv' is in your main project folder.")
else:
    st.error(f"Hospital data file '{os.path.basename(HOSPITALS_DATA_PATH)}' not found. Please ensure it's in your main project folder: `{HOSPITALS_DATA_PATH}`.")

if df_hospitals.empty:
    st.warning("No data loaded to display charts.")
    st.stop()

# Get all numerical columns suitable for scatter plots (excluding Lat/Lon for now)
numerical_columns = df_hospitals.select_dtypes(include=['number']).columns.tolist()
# Filter out lat/lon as they are for maps
numerical_columns = [col for col in numerical_columns if col not in ['Location_Lat', 'Location_Lon']]


st.sidebar.header("Scatter Plot Controls")
# Allow user to select X and Y axes
x_axis = st.sidebar.selectbox("Select X-axis:", numerical_columns, index=0)
y_axis = st.sidebar.selectbox("Select Y-axis:", numerical_columns, index=1)
color_by = st.sidebar.selectbox("Color points by (Categorical):", ['None'] + df_hospitals.select_dtypes(include=['object', 'category']).columns.tolist(), index=1)
size_by = st.sidebar.selectbox("Size points by (Numerical):", ['None'] + numerical_columns, index=0)

# Filter out NaN values for selected axes to avoid errors in plotting
df_plot = df_hospitals.dropna(subset=[x_axis, y_axis])

if not df_plot.empty:
    st.subheader(f"Relationship between {x_axis} and {y_axis}")

    # Create the scatter plot
    if color_by == 'None' and size_by == 'None':
        fig = px.scatter(df_plot, x=x_axis, y=y_axis,
                         hover_name="Name of hospital or clinic",
                         title=f'{x_axis} vs. {y_axis}')
    elif color_by != 'None' and size_by == 'None':
        fig = px.scatter(df_plot, x=x_axis, y=y_axis, color=color_by,
                         hover_name="Name of hospital or clinic",
                         title=f'{x_axis} vs. {y_axis} (Colored by {color_by})')
    elif color_by == 'None' and size_by != 'None':
        # Drop NaN for size_by column if it's selected
        df_plot_size = df_plot.dropna(subset=[size_by])
        fig = px.scatter(df_plot_size, x=x_axis, y=y_axis, size=size_by,
                         hover_name="Name of hospital or clinic",
                         title=f'{x_axis} vs. {y_axis} (Sized by {size_by})')
    else: # Both color_by and size_by are selected
        df_plot_both = df_plot.dropna(subset=[size_by])
        fig = px.scatter(df_plot_both, x=x_axis, y=y_axis, color=color_by, size=size_by,
                         hover_name="Name of hospital or clinic",
                         title=f'{x_axis} vs. {y_axis} (Colored by {color_by}, Sized by {size_by})')

    fig.update_layout(hovermode="closest")
    st.plotly_chart(fig, use_container_width=True)

else:
    st.warning(f"No valid data to plot for {x_axis} vs. {y_axis} after removing missing values.")

st.markdown("---")
st.write("Explore relationships between different numerical metrics in the UAE's healthcare data.")