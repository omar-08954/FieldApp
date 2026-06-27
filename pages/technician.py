import os
import streamlit as st

from database.database import (
    add_task,
    task_exists
)

# ======================================
# التحقق من تسجيل الدخول
# ======================================

if not st.session_state.get("logged_in", False):
    st.warning("يرجى تسجيل الدخول أولاً")
    st.stop()

# ======================================
# إنشاء مجلد الصور
# ======================================

if not os.path.exists("images"):
    os.makedirs("images")

# ======================================
# عنوان الصفحة
# ======================================

st.title("👷 صفحة الفني")

st.subheader("إضافة مهمة جديدة")

st.divider()

# ======================================
# بيانات المهمة
# ======================================

technician = st.session_state.fullname

st.text_input(
    "اسم الفني",
    value=technician,
    disabled=True
)

task_number = st.text_input("رقم المهمة")

subscription_number = st.text_input("رقم الاشتراك")

status = st.selectbox(
    "حالة المهمة",
    [
        "مكتملة",
        "قيد التنفيذ",
        "مؤجلة",
        "العميل غير موجود",
        "يحتاج مراجعة"
    ]
)

notes = st.text_area("الملاحظات")

# ======================================
# الموقع الجغرافي
# ======================================

st.subheader("📍 الموقع الجغرافي")

latitude = st.text_input("Latitude")

longitude = st.text_input("Longitude")

st.caption(
    "في الإصدارات القادمة سيتم جلب الموقع تلقائياً من الهاتف."
)

# ======================================
# الصور
# ======================================

st.subheader("📷 صور المهمة")

before_image = st.file_uploader(
    "صورة قبل التنفيذ",
    type=["jpg", "jpeg", "png"],
    key="before"
)

after_image = st.file_uploader(
    "صورة بعد التنفيذ",
    type=["jpg", "jpeg", "png"],
    key="after"
)

if before_image:
    st.image(
        before_image,
        caption="صورة قبل التنفيذ",
        use_container_width=True
    )

if after_image:
    st.image(
        after_image,
        caption="صورة بعد التنفيذ",
        use_container_width=True
    )

st.divider()

# ======================================
# حفظ المهمة
# ======================================

if st.button("💾 حفظ المهمة", use_container_width=True):

    if task_number.strip() == "":
        st.error("يرجى إدخال رقم المهمة")

    elif subscription_number.strip() == "":
        st.error("يرجى إدخال رقم الاشتراك")

    elif task_exists(task_number):
        st.error("رقم المهمة موجود بالفعل")

    else:

        # حفظ صورة قبل التنفيذ
        if before_image:

            before_path = (
                f"images/"
                f"{task_number}_before_{before_image.name}"
            )

            with open(before_path, "wb") as f:
                f.write(before_image.getbuffer())

        # حفظ صورة بعد التنفيذ
        if after_image:

            after_path = (
                f"images/"
                f"{task_number}_after_{after_image.name}"
            )

            with open(after_path, "wb") as f:
                f.write(after_image.getbuffer())

        # حفظ المهمة
        add_task(
            technician,
            task_number,
            subscription_number,
            status,
            notes,
            latitude,
            longitude
        )

        st.success("✅ تم حفظ المهمة بنجاح")

        st.balloons()

        st.rerun()
        