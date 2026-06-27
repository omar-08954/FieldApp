import streamlit as st
import pandas as pd
from datetime import datetime

from database.database import get_all_tasks

# ======================================
# التحقق من تسجيل الدخول
# ======================================

if not st.session_state.get("logged_in", False):
    st.warning("يرجى تسجيل الدخول أولاً")
    st.stop()

# ======================================
# عنوان الصفحة
# ======================================

st.title("📅 مهام اليوم")

st.divider()

tasks = get_all_tasks()

if len(tasks) == 0:
    st.info("لا توجد مهام")
    st.stop()

df = pd.DataFrame([dict(row) for row in tasks])

# ======================================
# فلترة مهام اليوم
# ======================================

today = datetime.now().strftime("%Y-%m-%d")

df["task_date"] = pd.to_datetime(
    df["created_at"]
).dt.strftime("%Y-%m-%d")

today_df = df[df["task_date"] == today]

# ======================================
# عرض البيانات
# ======================================

if len(today_df) == 0:

    st.info("لا توجد مهام مسجلة اليوم")

else:

    st.metric(
        "عدد مهام اليوم",
        len(today_df)
    )

    st.dataframe(
        today_df[
            [
                "technician",
                "task_number",
                "subscription_number",
                "status",
                "created_at"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )
    