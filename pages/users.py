import streamlit as st
import pandas as pd

from database.database import (
    get_all_users,
    add_user,
    delete_user
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

st.title("👥 إدارة المستخدمين")

st.divider()

# ======================================
# إضافة مستخدم
# ======================================

st.subheader("➕ إضافة مستخدم جديد")

with st.form("add_user_form"):

    fullname = st.text_input("الاسم الكامل")

    username = st.text_input("اسم المستخدم")

    password = st.text_input(
        "كلمة المرور",
        type="password"
    )

    role = st.selectbox(
        "الصلاحية",
        [
            "technician",
            "admin"
        ]
    )

    submit = st.form_submit_button("إضافة المستخدم")

    if submit:

        if (
            fullname.strip() == "" or
            username.strip() == "" or
            password.strip() == ""
        ):

            st.error("يرجى تعبئة جميع الحقول")

        else:

            try:

                add_user(
                    username,
                    password,
                    fullname,
                    role
                )

                st.success("تمت إضافة المستخدم بنجاح")

                st.rerun()

            except Exception as e:

                st.error(f"حدث خطأ: {e}")

st.divider()

# ======================================
# عرض المستخدمين
# ======================================

st.subheader("📋 المستخدمون")

users = get_all_users()

if users:

    df = pd.DataFrame([dict(row) for row in users])

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.subheader("🗑️ حذف مستخدم")

    options = {
        f"{row['fullname']} ({row['username']})": row["id"]
        for row in users
    }

    selected = st.selectbox(
        "اختر المستخدم",
        list(options.keys())
    )

    if st.button("حذف المستخدم"):

        delete_user(options[selected])

        st.success("تم حذف المستخدم")

        st.rerun()

else:

    st.info("لا يوجد مستخدمون.")
    