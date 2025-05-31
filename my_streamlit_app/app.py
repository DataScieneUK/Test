import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# --- إعدادات الصفحة ---
st.set_page_config(
    page_title="محلل بيانات السنوات",
    page_icon="📊",
    layout="centered"
)

st.title("📊 محلل بيانات السنوات")
st.markdown("---")

# عرض المسار الحالي للتطبيق
current_directory = os.getcwd()

st.warning("تأكد أن ملفات CSV موجودة في هذا المسار لتجنب الأخطاء.")

# --- قائمة السنوات المتاحة ---
years = list(range(2020, 2026))

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

# **هنا التعديل الرئيسي:** بناء المسار الكامل للملف
csv_file_name = f"{selected_year}.csv"
# ندمج المسار الحالي مع اسم الملف لتشكيل المسار الكامل
full_file_path = os.path.join(current_directory, csv_file_name)
st.info(f"المسار الكامل لملف التطبيق (`app.py`): **`{os.path.abspath(__file__)}`**")
st.info(f"المسار555555 الحالي للتطبيق: **`{current_directory}`**")
st.info(f"المسار555555 الحالي للتطبيق: **`{full_file_path}`**")
# التحقق مما إذا كان الملف موجودًا باستخدام المسار الكامل
if os.path.exists(full_file_path):
    try:
        # قراءة البيانات من ملف CSV باستخدام المسار الكامل
        df = pd.read_csv(full_file_path)

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
            st.warning(f"الملف '{csv_file_name}' لا يحتوي على البيانات المتوقعة أو الأعمدة 'Category' و 'Value'.")

    except Exception as e:
        st.error(f"حدث خطأ أثناء قراءة أو معالجة الملف '{csv_file_name}': {e}")
else:
    st.error(f"ملف البيانات للسنة {selected_year} ({csv_file_name}) غير موجود في المسار: `{full_file_path}`.")
    st.info("الرجاء التأكد من وجود ملف CSV لكل سنة في نفس المجلد الذي يعمل منه التطبيق.")

st.markdown("---")
st.write("تم التطوير بواسطة: [اسمك/شركتك إن أردت]")
