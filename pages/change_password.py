import streamlit as st

from database.database import (
    change_password
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

st.title("🔐 تغيير كلمة المرور")

st.divider()

new_password = st.text_input(
    "كلمة المرور الجديدة",
    type="password"
)

confirm_password = st.text_input(
    "تأكيد كلمة المرور",
    type="password"
)

if st.button(
        "حفظ كلمة المرور",
        use_container_width=True):

    if new_password == "":
        st.error("يرجى إدخال كلمة المرور")

    elif new_password != confirm_password:
        st.error("كلمتا المرور غير متطابقتين")

    else:

        # البحث عن id المستخدم الحالي
        from database.database import get_connection

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""
        SELECT id

        FROM users

        WHERE username=?
        """, (
            st.session_state.username,
        ))

        user = cursor.fetchone()

        conn.close()

        change_password(
            user["id"],
            new_password
        )

        st.success(
            "تم تغيير كلمة المرور بنجاح"
        )

        st.balloons()
        