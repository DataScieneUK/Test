import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- Page Configuration (Optional for sub-pages, but good for clarity) ---
# st.set_page_config(page_title="UAE Hospitals Map", page_icon="🗺️")

st.title("🗺️ Interactive UAE Hospitals Map")
st.markdown("---")

# --- Define Paths for Data ---
app_directory = os.path.dirname(os.path.abspath(__file__))
# نرجع خطوة للخلف للوصول إلى المجلد الرئيسي حيث يوجد ملف UAE_hospitals_data.csv
data_directory = os.path.abspath(os.path.join(app_directory, os.pardir))
HOSPITALS_DATA_PATH = os.path.join(data_directory, "UAE_hospitals_data.csv")

st.info(f"مجلد البيانات (المتوقع لملف المستشفيات): **`{data_directory}`**")
st.warning(f"تأكد أن ملف '{os.path.basename(HOSPITALS_DATA_PATH)}' موجود في هذا المسار لتجنب الأخطاء.")

# --- Load Data ---
df_hospitals = pd.DataFrame() # تعريف DataFrame فارغ مبدئياً
if os.path.exists(HOSPITALS_DATA_PATH):
    try:
        df_hospitals = pd.read_csv(HOSPITALS_DATA_PATH)
        st.success(f"تم تحميل بيانات المستشفيات بنجاح من: `{os.path.basename(HOSPITALS_DATA_PATH)}`")
        st.dataframe(df_hospitals.head()) # عرض أول 5 صفوف من البيانات
    except Exception as e:
        st.error(f"حدث خطأ أثناء قراءة ملف بيانات المستشفيات: {e}")
else:
    st.error(f"ملف بيانات المستشفيات '{os.path.basename(HOSPITALS_DATA_PATH)}' غير موجود في المسار المحدد: `{HOSPITALS_DATA_PATH}`.")
    st.info("الرجاء التأكد من وجود ملف 'UAE_hospitals_data.csv' في المجلد الرئيسي لمشروعك.")

# --- Check for essential columns before plotting ---
required_columns = ['Location_Lat', 'Location_Lon', 'Name of hospital or clinic']
if not df_hospitals.empty and all(col in df_hospitals.columns for col in required_columns):
    # Drop rows with missing latitude or longitude
    df_hospitals.dropna(subset=['Location_Lat', 'Location_Lon'], inplace=True)

    st.subheader("Interactive Map of UAE Hospitals")

    # Define hover data columns
    hover_cols = [
        'Hospital rate',
        'State',
        'Number of Doctors',
        'Number of patients in 2020',
        'Types of treatment it contains',
        'total cost of the hospital in 2020 (million AED)',
        'total income of the hospital in 2020 (million AED)',
        'total number of surgeries in 2020'
    ]

    # Filter hover_cols to only include columns that actually exist in the DataFrame
    existing_hover_cols = [col for col in hover_cols if col in df_hospitals.columns]

    if not df_hospitals.empty:
        # Create the interactive map using Plotly Express
        fig = px.scatter_mapbox(df_hospitals,
                                lat="Location_Lat",
                                lon="Location_Lon",
                                hover_name="Name of hospital or clinic", # الاسم الذي يظهر في التلميح الرئيسي
                                hover_data=existing_hover_cols, # البيانات الإضافية التي تظهر عند التمرير
                                color="State", # تلوين النقاط حسب الولاية (اختياري)
                                zoom=7, # مستوى التكبير الأولي (7 مناسب للإمارات)
                                center={"lat": 24.4539, "lon": 54.3773}, # مركز الخريطة (أبوظبي)
                                mapbox_style="open-street-map", # نوع الخريطة (يمكنك تجربة "carto-positron", "stamen-terrain", etc.)
                                title="Hospitals and Clinics Across the UAE"
                               )

        # تحديث حجم النقط (اختياري)
        fig.update_traces(marker=dict(size=10, opacity=0.8))
        # تحديث هوامش الخريطة (اختياري)
        fig.update_layout(margin={"r":0,"t":50,"l":0,"b":0})

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("لا توجد بيانات مستشفيات صالحة لعرضها على الخريطة بعد إزالة الصفوف المفقودة.")

else:
    st.warning("البيانات غير مكتملة أو الأعمدة المطلوبة (Location_Lat, Location_Lon, Name of hospital or clinic) غير موجودة في ملف المستشفيات.")

st.markdown("---")
st.write("استكشف مواقع المستشفيات والبيانات الرئيسية الخاصة بها على الخريطة التفاعلية.")