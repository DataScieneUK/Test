import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os # لاستخدام وظائف نظام التشغيل مثل التحقق من وجود الملفات

# --- إعدادات الصفحة ---
st.set_page_config(
    page_title="محلل بيانات السنوات",
    page_icon="📊",
    layout="centered" # يمكن أن تكون "wide" أيضاً
)

st.title("📊 محلل بيانات السنوات")
st.markdown("---")

# **أضف هذا السطر هنا لعرض المسار:**
st.info(f"المسار الحالي للتطبيق: **`{os.getcwd()}`**")

# --- قائمة السنوات المتاحة ---
years = list(range(2020, 2026)) # من 2020 إلى 2025

# --- الواجهة الجانبية (Sidebar) ---
st.sidebar.header("اختر السنة")
selected_year = st.sidebar.radio(
    "اختر سنة لعرض بياناتها:",
    years
)

st.sidebar.markdown("---")
st.sidebar.info("هذا التطبيق يعرض بيانات من ملفات CSV بناءً على السنة المختارة.")

# --- المنطقة الرئيسية لعرض البيانات ---
st.subheader(f"البيانات للسنة: {selected_year}")

# اسم الملف المتوقع
file_name = f"{selected_year}.csv"

# التحقق مما إذا كان الملف موجودًا
if os.path.exists(file_name):
    try:
        # قراءة البيانات من ملف CSV
        df = pd.read_csv(file_name)

        # التحقق من أن DataFrame ليس فارغاً وبه الأعمدة المطلوبة
        if not df.empty and 'Category' in df.columns and 'Value' in df.columns:
            st.write("تم قراءة البيانات بنجاح:")
            st.dataframe(df) # لعرض جدول البيانات

            # إنشاء Pie Chart
            st.subheader("توزيع البيانات (Pie Chart)")
            fig, ax = plt.subplots()
            ax.pie(df['Value'], labels=df['Category'], autopct='%1.1f%%', startangle=90)
            ax.axis('equal') # يضمن أن تكون الدائرة متساوية الأبعاد
            st.pyplot(fig) # لعرض الرسم البياني في Streamlit

        else:
            st.warning(f"الملف '{file_name}' لا يحتوي على البيانات المتوقعة أو الأعمدة 'Category' و 'Value'.")

    except Exception as e:
        st.error(f"حدث خطأ أثناء قراءة أو معالجة الملف '{file_name}': {e}")
else:
    st.warning(f"ملف البيانات للسنة {selected_year} ({file_name}) غير موجود في نفس المجلد.")
    st.info("الرجاء التأكد من وجود ملف CSV لكل سنة في نفس المجلد.")

st.markdown("---")
st.write("تم التطوير بواسطة: [اسمك/شركتك إن أردت]")
