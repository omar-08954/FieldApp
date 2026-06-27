import streamlit as st
import pandas as pd

from database.database import get_all_tasks

# ======================================
# التحقق من تسجيل الدخول
# ======================================

if not st.session_state.get("logged_in", False):
    st.warning("يرجى تسجيل الدخول أولاً")
    st.stop()

if st.session_state.get("role") != "admin":
    st.error("هذه الصفحة مخصصة للمدير فقط")
    st.stop()

# ======================================
# عنوان الصفحة
# ======================================

st.title("🗺️ خريطة المهام")

st.divider()

# ======================================
# جلب البيانات
# ======================================

tasks = get_all_tasks()

if len(tasks) == 0:
    st.info("لا توجد مهام لعرضها")
    st.stop()

df = pd.DataFrame([dict(row) for row in tasks])

# ======================================
# التحقق من وجود إحداثيات
# ======================================

if "latitude" not in df.columns or "longitude" not in df.columns:
    st.warning("لا توجد بيانات GPS")
    st.stop()

# حذف السجلات التي لا تحتوي على إحداثيات

df = df[
    (df["latitude"] != "") &
    (df["longitude"] != "")
]

if len(df) == 0:
    st.info("لا توجد مواقع مسجلة حتى الآن")
    st.stop()

# ======================================
# تحويل الإحداثيات إلى أرقام
# ======================================

df["latitude"] = pd.to_numeric(
    df["latitude"],
    errors="coerce"
)

df["longitude"] = pd.to_numeric(
    df["longitude"],
    errors="coerce"
)

df = df.dropna(
    subset=["latitude", "longitude"]
)

# ======================================
# عرض الخريطة
# ======================================

st.subheader("📍 مواقع المهام")

map_df = df.rename(
    columns={
        "latitude": "lat",
        "longitude": "lon"
    }
)

st.map(map_df)

# ======================================
# عرض الجدول
# ======================================

st.divider()

st.subheader("📋 بيانات المواقع")

st.dataframe(

    df[
        [
            "technician",
            "task_number",
            "status",
            "latitude",
            "longitude"
        ]
    ],

    use_container_width=True,
    hide_index=True

)
