import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

st.title("⭐ Hospital Reviews Analysis")
st.markdown("---")

# --- Define Path for Data ---
app_directory = os.path.dirname(os.path.abspath(__file__))
data_directory = os.path.abspath(os.path.join(app_directory, os.pardir))
HOSPITALS_DATA_PATH = os.path.join(data_directory, "UAE_hospitals_data.csv")

# --- Load Data ---
df_hospitals = pd.DataFrame()
if os.path.exists(HOSPITALS_DATA_PATH):
    try:
        df_hospitals = pd.read_csv(HOSPITALS_DATA_PATH)
        # Ensure numerical columns are numeric, coercing errors
        numerical_review_cols = ['number of reviews', 'positive reviews', 'negative reviews']
        for col in numerical_review_cols:
            if col in df_hospitals.columns:
                df_hospitals[col] = pd.to_numeric(df_hospitals[col], errors='coerce').fillna(0)
    except Exception as e:
        st.error(f"Error reading hospital data file: {e}. Please ensure 'UAE_hospitals_data.csv' is in your main project folder.")
else:
    st.error(f"Hospital data file '{os.path.basename(HOSPITALS_DATA_PATH)}' not found. Please ensure it's in your main project folder: `{HOSPITALS_DATA_PATH}`.")

# --- Stop if data not loaded ---
if df_hospitals.empty:
    st.warning("No data loaded to display hospital reviews.")
    st.stop()

# --- Sidebar: Hospital Selection ---
st.sidebar.header("Select a Hospital")
# Drop rows where 'Name of hospital or clinic' is missing before getting unique names
hospitals_list = df_hospitals['Name of hospital or clinic'].dropna().unique().tolist()
hospitals_list.sort() # Sort hospitals alphabetically

selected_hospital = st.sidebar.selectbox(
    "Choose a hospital to view its review details:",
    hospitals_list,
    key="hospital_selector"
)

# --- Display Content for Selected Hospital ---
if selected_hospital:
    hospital_data = df_hospitals[df_hospitals['Name of hospital or clinic'] == selected_hospital].iloc[0]

    st.subheader(f"Review Analysis for: {selected_hospital}")

    total_reviews = hospital_data['number of reviews']
    positive_reviews = hospital_data['positive reviews']
    negative_reviews = hospital_data['negative reviews']

    # Ensure valid numbers for calculations
    if pd.isna(total_reviews) or total_reviews == 0:
        st.info(f"No review data available for {selected_hospital}.")
        total_reviews = 0
        positive_reviews = 0
        negative_reviews = 0

    # Calculate percentages
    pos_percent = (positive_reviews / total_reviews * 100) if total_reviews > 0 else 0
    neg_percent = (negative_reviews / total_reviews * 100) if total_reviews > 0 else 0

    # --- Pie Chart for Review Sentiment ---
    st.markdown("#### Positive vs. Negative Reviews")
    review_labels = ['Positive', 'Negative']
    review_values = [positive_reviews, negative_reviews]
    review_colors = ['#2ca02c', '#d62728'] # Green for positive, Red for negative

    if total_reviews > 0:
        fig_pie = go.Figure(data=[go.Pie(labels=review_labels, values=review_values, hole=.3,
                                         marker_colors=review_colors,
                                         hoverinfo="label+percent+value",
                                         textinfo="label+percent",
                                         textfont_size=15)])
        fig_pie.update_layout(showlegend=True, margin=dict(t=50, b=0, l=0, r=0),
                              title_text=f"Total Reviews: {int(total_reviews)}")
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.info("No reviews to display pie chart.")

    # --- Display Keywords ---
    st.markdown("#### Most Repeated Keywords")
    col_pos_keywords, col_neg_keywords = st.columns(2)

    with col_pos_keywords:
        st.markdown("##### Positive Keywords")
        pos_keywords = hospital_data.get('most repeated keywords for the hospital in positive reviews', 'N/A')
        if pd.isna(pos_keywords) or pos_keywords == 'N/A':
            st.info("No positive keywords available.")
        else:
            st.write(pos_keywords)

    with col_neg_keywords:
        st.markdown("##### Negative Keywords")
        neg_keywords = hospital_data.get('most repeated keywords for the hospital in negative reviews', 'N/A')
        if pd.isna(neg_keywords) or neg_keywords == 'N/A':
            st.info("No negative keywords available.")
        else:
            st.write(neg_keywords)

else:
    st.info("Please select a hospital from the sidebar to view its review analysis.")

st.markdown("---")
st.write("Gain insights into hospital performance through customer reviews and key feedback themes.")