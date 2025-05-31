import streamlit as st

st.set_page_config(
    page_title="محلل بيانات السنوات",
    page_icon="📊",
    layout="centered"
)

st.title("مرحبًا بك في محلل بيانات السنوات 📊")
st.markdown("---")
st.write(
    """
    استخدم الشريط الجانبي على اليسار لاستكشاف البيانات.
    - **تحليل الرسوم الدائرية:** يعرض توزيع البيانات على شكل Pie Chart تفاعلي.
    - **تحليل الرسوم الشريطية:** يعرض البيانات على شكل Bar Chart تفاعلي.
    """
)
st.markdown("---")
st.info("تم التطوير باستخدام Streamlit و Plotly.")
