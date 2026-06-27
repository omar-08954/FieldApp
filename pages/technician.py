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
# العنوان
# ======================================

st.title("👷 صفحة الفني")

st.divider()

technician = st.session_state.fullname

st.text_input(
    "اسم الفني",
    value=technician,
    disabled=True
)

task_number = st.text_input("رقم المهمة")

subscription_number = st.text_input("رقم الاشتراك")

task_type = st.selectbox(
    "نوع المهمة",
    [
        "تقني",
        "زيرا"
    ]
)

notes = st.selectbox(
    "الملاحظات",
    [
        "تم الفحص",
        "عائق",
        "مازال"
    ]
)

latitude = st.text_input("Latitude")

longitude = st.text_input("Longitude")

if st.button(
        "💾 حفظ المهمة",
        use_container_width=True):

    if task_number.strip() == "":
        st.error("يرجى إدخال رقم المهمة")

    elif subscription_number.strip() == "":
        st.error("يرجى إدخال رقم الاشتراك")

    elif task_exists(task_number):
        st.error("رقم المهمة موجود مسبقاً")

    else:

        add_task(
            technician,
            task_number,
            subscription_number,
            task_type,
            notes,
            latitude,
            longitude
        )

        st.success("تم حفظ المهمة بنجاح")

        st.balloons()
        