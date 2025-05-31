import streamlit as st
import pandas as pd
import plotly.express as px # استيراد plotly.express
import os

# --- إعدادات الصفحة ---
st.set_page_config(
    page_title="محلل بيانات السنوات",
    page_icon="📊",
    layout="centered"
)

st.title("📊 محلل بيانات السنوات")
st.markdown("---")

# عرض المسار الحالي لملف التطبيق والمجلد الذي يتواجد فيه
#st.info(f"المسار الكامل لملف التطبيق (`app.py`): **`{os.path.abspath(__file__)}`**")
app_directory = os.path.dirname(os.path.abspath(__file__))
#st.info(f"مجلد التطبيق (المتوقع لملفات CSV): **`{app_directory}`**")
st.warning("تأكد أن جميع ملفات CSV موجودة في هذا المسار لتجنب الأخطاء.")

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

# اسم الملف المتوقع
csv_file_name = f"{selected_year}.csv"
# ندمج مجلد التطبيق مع اسم الملف لتشكيل المسار الكامل
#full_file_path = os.path.join(app_directory, csv_file_name)
full_file_path = os.path.join(current_directory + r"/my_streamlit_app/", csv_file_name)
# التحقق مما إذا كان الملف موجودًا باستخدام المسار الكامل
if os.path.exists(full_file_path):
    try:
        # قراءة البيانات من ملف CSV باستخدام المسار الكامل
        df = pd.read_csv(full_file_path)

        # التحقق من أن DataFrame ليس فارغاً وبه الأعمدة المطلوبة
        if not df.empty and 'Category' in df.columns and 'Value' in df.columns:
            st.write("تم قراءة البيانات بنجاح:")
            st.dataframe(df) # لعرض جدول البيانات

            # --- إنشاء Pie Chart تفاعلي باستخدام Plotly ---
            st.subheader("توزيع البيانات التفاعلي (Pie Chart)")

            # استخدام plotly.express لإنشاء Pie Chart
            # names='Category' لتسميات الشرائح
            # values='Value' للقيم التي تحدد حجم الشرائح
            # title لتحديد عنوان للرسم البياني
            # hover_data لتعريف البيانات الإضافية التي تظهر عند التمرير بالماوس
            fig = px.pie(df,
                         names='Category',
                         values='Value',
                         title=f"توزيع البيانات لـ {selected_year}",
                         hole=0.3, # لجعلها دونات شارت اختيارياً
                         hover_data=['Value']) # عرض القيمة عند التمرير بالماوس

            # تحديث قالب الرسم البياني ليكون أجمل (اختياري)
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')

            st.plotly_chart(fig, use_container_width=True) # لعرض الرسم البياني في Streamlit

        else:
            st.warning(f"الملف '{csv_file_name}' لا يحتوي على البيانات المتوقعة أو الأعمدة 'Category' و 'Value'.")

    except Exception as e:
        st.error(f"حدث خطأ أثناء قراءة أو معالجة الملف '{csv_file_name}': {e}")
else:
    st.error(f"ملف البيانات للسنة {selected_year} ({csv_file_name}) غير موجود في المسار: `{full_file_path}`.")
    st.info("الرجاء التأكد من وجود ملف CSV لكل سنة في نفس المجلد الذي يعمل منه التطبيق.")

st.markdown("---")
st.write("تم التطوير بواسطة: [اسمك/شركتك إن أردت]")



