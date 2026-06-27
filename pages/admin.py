import streamlit as st
import pandas as pd

from database.database import (
    get_all_tasks,
    delete_task,
    update_task
)

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
# عنوان الصفحة
# ======================================

st.title("👔 لوحة المدير")

st.divider()

# ======================================
# جلب المهام
# ======================================

tasks = get_all_tasks()

if len(tasks) == 0:
    st.info("لا توجد مهام مسجلة.")
    st.stop()

df = pd.DataFrame([dict(row) for row in tasks])

# ======================================
# الإحصائيات
# ======================================

col1, col2, col3 = st.columns(3)

col1.metric("إجمالي المهام", len(df))

col2.metric(
    "المكتملة",
    len(df[df["status"] == "مكتملة"])
)

col3.metric(
    "قيد التنفيذ",
    len(df[df["status"] == "قيد التنفيذ"])
)

st.divider()

# ======================================
# البحث
# ======================================

search = st.text_input("🔍 البحث")

if search:

    df = df[
        df["technician"].astype(str).str.contains(search, case=False)
        |
        df["task_number"].astype(str).str.contains(search, case=False)
        |
        df["subscription_number"].astype(str).str.contains(search, case=False)
    ]

# ======================================
# عرض المهام
# ======================================

st.subheader("📋 جميع المهام")

st.dataframe(
    df[
        [
            "id",
            "technician",
            "task_number",
            "subscription_number",
            "status",
            "notes",
            "created_at"
        ]
    ],
    use_container_width=True,
    hide_index=True
)

st.divider()

# ======================================
# تعديل مهمة
# ======================================

st.subheader("✏️ تعديل مهمة")

task_ids = df["id"].tolist()

selected_id = st.selectbox(
    "اختر رقم المهمة",
    task_ids
)

selected_task = df[df["id"] == selected_id].iloc[0]

new_subscription = st.text_input(
    "رقم الاشتراك",
    value=selected_task["subscription_number"]
)

new_status = st.selectbox(
    "الحالة",
    [
        "مكتملة",
        "قيد التنفيذ",
        "مؤجلة",
        "العميل غير موجود",
        "يحتاج مراجعة"
    ],
    index=[
        "مكتملة",
        "قيد التنفيذ",
        "مؤجلة",
        "العميل غير موجود",
        "يحتاج مراجعة"
    ].index(selected_task["status"])
)

new_notes = st.text_area(
    "الملاحظات",
    value=selected_task["notes"]
)

if st.button("💾 حفظ التعديلات"):

    update_task(
        selected_id,
        new_subscription,
        new_status,
        new_notes
    )

    st.success("تم تعديل المهمة بنجاح")

    st.rerun()

st.divider()

# ======================================
# حذف مهمة
# ======================================

st.subheader("🗑️ حذف مهمة")

delete_id = st.selectbox(
    "اختر المهمة للحذف",
    task_ids,
    key="delete_box"
)

if st.button("حذف المهمة"):

    delete_task(delete_id)

    st.success("تم حذف المهمة")

    st.rerun()

# ======================================
# Excel
# ======================================

st.divider()

excel_path = "exports/tasks.xlsx"

df.to_excel(
    excel_path,
    index=False
)

with open(excel_path, "rb") as file:

    st.download_button(
        "📥 تحميل Excel",
        file,
        file_name="tasks.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )
    import os

st.divider()

st.subheader("📷 عرض صور المهمة")

task_numbers = df["task_number"].tolist()

selected_task = st.selectbox(
    "اختر رقم المهمة",
    task_numbers,
    key="images_task"
)

image_files = []

if os.path.exists("images"):

    for file in os.listdir("images"):

        if str(selected_task) in file:

            image_files.append(file)

if len(image_files) == 0:

    st.info("لا توجد صور لهذه المهمة")

else:

    cols = st.columns(2)

    for index, image in enumerate(image_files):

        image_path = os.path.join(
            "images",
            image
        )

        with cols[index % 2]:

            st.image(
                image_path,
                caption=image,
                use_container_width=True
            )
            