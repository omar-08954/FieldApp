import streamlit as st
from database.database import create_tables, create_default_users, login_user

# ======================================
# إعداد الصفحة
# ======================================

st.set_page_config(
    page_title="شركة الفكر الصاعد للمقاولات",
    page_icon="🏗️",
    layout="wide"
)

# ======================================
# إنشاء قاعدة البيانات
# ======================================

create_tables()
create_default_users()

# ======================================
# Session State
# ======================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "fullname" not in st.session_state:
    st.session_state.fullname = ""

if "role" not in st.session_state:
    st.session_state.role = ""

# ======================================
# شاشة تسجيل الدخول
# ======================================

if not st.session_state.logged_in:

    st.title("🏗️ شركة الفكر الصاعد للمقاولات")

    st.subheader("نظام إدارة المهام الميدانية")

    st.divider()

    username = st.text_input("اسم المستخدم")

    password = st.text_input(
        "كلمة المرور",
        type="password"
    )

    if st.button("تسجيل الدخول", use_container_width=True):

        user = login_user(username, password)

        if user:

            st.session_state.logged_in = True

            st.session_state.username = user["username"]

            st.session_state.fullname = user["fullname"]

            st.session_state.role = user["role"]

            st.rerun()

        else:

            st.error("اسم المستخدم أو كلمة المرور غير صحيحة")

# ======================================
# بعد تسجيل الدخول
# ======================================

else:

    st.success(
        f"مرحبًا {st.session_state.fullname}"
    )

    col1, col2 = st.columns(2)

    with col1:
        st.write(f"**اسم المستخدم:** {st.session_state.username}")

    with col2:
        st.write(f"**الصلاحية:** {st.session_state.role}")

    st.divider()

    if st.session_state.role == "admin":

        st.info("⬅ اختر صفحة Admin من القائمة الجانبية")

    else:

        st.info("⬅ اختر صفحة Technician من القائمة الجانبية")

    if st.button("تسجيل الخروج"):

        for key in list(st.session_state.keys()):
            del st.session_state[key]

        st.rerun()
        