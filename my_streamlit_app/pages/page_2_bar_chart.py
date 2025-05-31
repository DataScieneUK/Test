import streamlit as st
import pandas as pd
import plotly.express as px
import os

# st.set_page_config(page_title="رسم بياني شريطي", page_icon="📊")
st.title("📊 تحليل الرسوم الشريطية")
st.markdown("---")

# عرض المسار الحالي لملف التطبيق والمجلد الذي يتواجد فيه
st.info(f"المسار الكامل لملف التطبيق (`app.py`): **`{os.path.abspath(__file__)}`**")
app_directory = os.path.dirname(os.path.abspath(__file__))
# ملاحظة: `app_directory` هنا سيشير إلى مجلد `pages`.
# يجب أن نعود خطوة للخلف للوصول إلى ملفات CSV في المجلد الرئيسي.
data_directory = os.path.abspath(os.path.join(app_directory, os.pardir))
st.info(f"مجلد البيانات (المتوقع لملفات CSV): **`{data_directory}`**")
st.warning("تأكد أن جميع ملفات CSV موجودة في هذا المسار لتجنب الأخطاء.")


# --- قائمة السنوات المتاحة ---
years = list(range(2020, 2026))

# --- الواجهة الجانبية (Sidebar) ---
selected_year = st.sidebar.radio(
    "اختر سنة لعرض بياناتها:",
    years,
    key="bar_chart_year_selector" # يجب أن يكون له مفتاح فريد لـ st.sidebar.radio
)

# --- المنطقة الرئيسية لعرض البيانات ---
st.subheader(f"البيانات للسنة: {selected_year}")

# اسم الملف المتوقع
csv_file_name = f"{selected_year}.csv"
# ندمج مجلد البيانات (المجلد الرئيسي) مع اسم الملف لتشكيل المسار الكامل
full_file_path = os.path.join(data_directory, csv_file_name)

# التحقق مما إذا كان الملف موجودًا باستخدام المسار الكامل
if os.path.exists(full_file_path):
    try:
        # قراءة البيانات من ملف CSV باستخدام المسار الكامل
        df = pd.read_csv(full_file_path)

        # التحقق من أن DataFrame ليس فارغاً وبه الأعمدة المطلوبة
        if not df.empty and 'Category' in df.columns and 'Value' in df.columns:
            st.write("تم قراءة البيانات بنجاح:")
            st.dataframe(df) # لعرض جدول البيانات

            # --- إنشاء Bar Chart تفاعلي باستخدام Plotly ---
            st.subheader("توزيع البيانات التفاعلي (Bar Chart)")

            # استخدام plotly.express لإنشاء Bar Chart
            # x='Category' للمحور الأفقي
            # y='Value' للمحور الرأسي
            # title لتحديد عنوان للرسم البياني
            # hover_data لتعريف البيانات الإضافية التي تظهر عند التمرير بالماوس
            fig = px.bar(df,
                         x='Category',
                         y='Value',
                         title=f"توزيع البيانات لـ {selected_year}",
                         color='Category', # لتلوين الأعمدة بناءً على الفئة (اختياري)
                         hover_data=['Value']) # عرض القيمة عند التمرير بالماوس

            st.plotly_chart(fig, use_container_width=True) # لعرض الرسم البياني في Streamlit

        else:
            st.warning(f"الملف '{csv_file_name}' لا يحتوي على البيانات المتوقعة أو الأعمدة 'Category' و 'Value'.")

    except Exception as e:
        st.error(f"حدث خطأ أثناء قراءة أو معالجة الملف '{csv_file_name}': {e}")
else:
    st.error(f"ملف البيانات للسنة {selected_year} ({csv_file_name}) غير موجود في المسار: `{full_file_path}`.")
    st.info("الرجاء التأكد من وجود ملف CSV لكل سنة في نفس المجلد الذي يعمل منه التطبيق (المجلد الرئيسي).")

st.markdown("---")
st.write("للتنقل بين الرسوم البيانية، استخدم الشريط الجانبي.")