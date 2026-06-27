import streamlit as st
import pandas as pd
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

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
# العنوان
# ======================================

st.title("📄 التقارير")

st.divider()

tasks = get_all_tasks()

if len(tasks) == 0:
    st.info("لا توجد بيانات لإنشاء تقرير")
    st.stop()

df = pd.DataFrame([dict(row) for row in tasks])

# ======================================
# نوع التقرير
# ======================================

report_type = st.selectbox(
    "نوع التقرير",
    [
        "تقرير جميع المهام",
        "تقرير حسب الفني"
    ]
)

selected_technician = None

if report_type == "تقرير حسب الفني":

    technicians = sorted(
        df["technician"].unique().tolist()
    )

    selected_technician = st.selectbox(
        "اختر الفني",
        technicians
    )

# ======================================
# إنشاء التقرير
# ======================================

if st.button("📄 إنشاء تقرير PDF"):

    report_df = df.copy()

    if selected_technician:

        report_df = report_df[
            report_df["technician"] ==
            selected_technician
        ]

    pdf_path = "exports/report.pdf"

    doc = SimpleDocTemplate(pdf_path)

    styles = getSampleStyleSheet()

    story = []

    title = Paragraph(
        "FieldApp Report",
        styles["Title"]
    )

    story.append(title)

    story.append(
        Spacer(1, 0.3 * inch)
    )

    for _, row in report_df.iterrows():

        text = f"""
        Technician: {row['technician']}<br/>
        Task Number: {row['task_number']}<br/>
        Subscription: {row['subscription_number']}<br/>
        Status: {row['status']}<br/>
        Notes: {row['notes']}<br/>
        Date: {row['created_at']}<br/>
        """

        story.append(
            Paragraph(
                text,
                styles["BodyText"]
            )
        )

        story.append(
            Spacer(1, 0.2 * inch)
        )

    doc.build(story)

    st.success("تم إنشاء التقرير بنجاح")

    with open(pdf_path, "rb") as file:

        st.download_button(
            "📥 تحميل التقرير PDF",
            file,
            file_name="report.pdf",
            mime="application/pdf",
            use_container_width=True
        )
        