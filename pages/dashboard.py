import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from database.database import get_all_tasks

# ======================================
# التحقق من تسجيل الدخول
# ======================================

if not st.session_state.get("logged_in", False):
    st.warning("يرجى تسجيل الدخول أولاً.")
    st.stop()

if st.session_state.get("role") != "admin":
    st.error("هذه الصفحة مخصصة للمدير فقط.")
    st.stop()

# ======================================
# العنوان
# ======================================

st.title("📊 لوحة الإحصائيات")

st.divider()

tasks = get_all_tasks()

if len(tasks) == 0:
    st.info("لا توجد بيانات لعرضها.")
    st.stop()

df = pd.DataFrame([dict(row) for row in tasks])

# ======================================
# الإحصائيات
# ======================================

total = len(df)

completed = len(df[df["status"] == "مكتملة"])

in_progress = len(df[df["status"] == "قيد التنفيذ"])

postponed = len(df[df["status"] == "مؤجلة"])

col1, col2, col3, col4 = st.columns(4)

col1.metric("إجمالي المهام", total)
col2.metric("المكتملة", completed)
col3.metric("قيد التنفيذ", in_progress)
col4.metric("المؤجلة", postponed)

st.divider()

# ======================================
# الرسم البياني
# ======================================

status_counts = df["status"].value_counts()

fig, ax = plt.subplots()

ax.pie(
    status_counts,
    labels=status_counts.index,
    autopct="%1.1f%%"
)

ax.set_title("توزيع حالات المهام")

st.pyplot(fig)

st.divider()

# ======================================
# جدول ملخص
# ======================================

summary = pd.DataFrame({
    "الحالة": status_counts.index,
    "العدد": status_counts.values
})

st.subheader("ملخص الحالات")

st.dataframe(
    summary,
    use_container_width=True,
    hide_index=True
)
