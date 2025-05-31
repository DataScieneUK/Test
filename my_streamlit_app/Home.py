import streamlit as st
import os

# --- Page Configuration ---
st.set_page_config(
    page_title="UAE Health Data Analytics - WeDo",
    page_icon="🇦🇪", # يمكنك استخدام علم الإمارات كـ icon
    layout="wide", # استخدام تخطيط واسع للاستفادة من المساحة
    initial_sidebar_state="expanded" # لجعل الشريط الجانبي مفتوحاً افتراضياً
)

# --- Define Paths for Assets (Images) ---
# تأكد من تعديل هذه المسارات لتتوافق مع مكان صورك الفعلية
# إذا كانت الصور في نفس مجلد app.py، استخدم فقط اسم الملف
# إذا كانت في مجلد 'assets' داخل مجلد المشروع الرئيسي
script_dir = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(script_dir, "assets")

UAE_FLAG_PATH = os.path.join(ASSETS_DIR, "uae_flag.png") # تأكد من وجود uae_flag.png
HEADER_IMAGE_PATH = os.path.join(ASSETS_DIR, "dubai_skyline.jpg") # صورة خلفية للترحيب مثلاً
MAIN_CONTENT_IMAGE_PATH = os.path.join(ASSETS_DIR, "health_data.jpg") # صورة ذات صلة بالصحة والبيانات


# --- Header Section with UAE Flag ---
col1, col2 = st.columns([0.1, 0.9]) # عمود صغير للعلم وعمود كبير للنص
with col1:
    if os.path.exists(UAE_FLAG_PATH):
        st.image(UAE_FLAG_PATH, width=80)
    else:
        st.warning(f"Flag image not found at: {UAE_FLAG_PATH}")
with col2:
    st.markdown("<h1 style='text-align: left; color: #004D40;'>UAE National Health Data Insights 🇦🇪</h1>", unsafe_allow_html=True) # لون أخضر غامق
st.markdown("---") # خط فاصل

# --- Welcome and Introduction ---
st.write(
    """
    <div style="background-color:#E0F2F7; padding: 20px; border-radius: 10px;">
        <h2 style='color:#01579B;'>Welcome to the National Health Data Analytics Platform!</h2>
        <p style='font-size: 1.1em;'>
        This platform is dedicated to providing comprehensive and insightful analysis of health data across the United Arab Emirates.
        Developed with a commitment to advancing public health and well-being, our application leverages cutting-edge technologies to transform raw data into actionable intelligence.
        </p>
    </div>
    """, unsafe_allow_html=True
)

st.markdown("---")

# --- WeDo Company & Technology Section ---
st.columns(1)[0].write("") # Small space

col_left, col_right = st.columns([0.6, 0.4]) # عمودان للنص والصورة

with col_left:
    st.markdown("<h3 style='color:#2E7D32;'>Powered by WeDo Company</h3>", unsafe_allow_html=True)
    st.write(
        """
        At **WeDo Company**, we pride ourselves on delivering innovative solutions that empower decision-makers.
        This health data analytics platform is a testament to our dedication to excellence and our expertise in
        harnessing complex datasets for meaningful insights.
        """
    )

    st.markdown("<h3 style='color:#6A1B9A;'>Our Advanced Analytical Approach</h3>", unsafe_allow_html=True)
    st.write(
        """
        We utilize state-of-the-art methodologies including:
        - 📊 **Advanced Data Analysis:** Uncovering patterns and trends.
        - 🧠 **Artificial Intelligence (AI):** Predictive modeling and intelligent insights.
        - 🚀 **Deep Learning:** Complex pattern recognition for precision.
        - 📈 **Interactive Visualizations:** Making data understandable and actionable.
        """
    )
    st.write(
        """
        Our aim is to provide a clear and dynamic overview of the UAE's health landscape, supporting strategic planning
        and improving health outcomes for all residents. Explore our dedicated analysis pages using the sidebar.
        """
    )

with col_right:
    if os.path.exists(MAIN_CONTENT_IMAGE_PATH):
        st.image(MAIN_CONTENT_IMAGE_PATH, caption="Leveraging Technology for Health Insights", use_container_width=True)
    else:
        st.warning(f"Main content image not found at: {MAIN_CONTENT_IMAGE_PATH}")

st.markdown("---")

# --- Footer ---
st.markdown(
    """
    <div style="text-align: center; padding: 10px; background-color:#F5F5F5; border-radius: 5px;">
        <p style="font-size:0.9em; color:#757575;">
            © 2025 WeDo Company. All rights reserved. | Contact: info@wedo.com
        </p>
    </div>
    """, unsafe_allow_html=True
)
