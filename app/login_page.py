import streamlit as st
from database import UserAuthentication

def show_login_page():
    # Sayfa yapılandırması
    st.set_page_config(page_title="tobbify login", layout="wide")

    st.markdown(
        """
        <style>
        body {
            background-color: #f0f2f6;
        }
        h1 {
            color: #3498db;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<h1>login</h1>", unsafe_allow_html=True)

    # Oturum durumunu kontrol et
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "home"
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    if "username" not in st.session_state:
        st.session_state["username"] = None
    if "user_id" not in st.session_state:
        st.session_state["user_id"] = None

    # Giriş formu
    username = st.text_input("username")
    password = st.text_input("password", type="password")

    if st.button("continue"):
        if not username or not password:
            st.error("username and password cannot be empty")
        else:
            success, user, user_id = UserAuthentication.login(username, password)
            if success:
                st.session_state["logged_in"] = True
                st.session_state["username"] = user
                st.session_state["current_page"] = "home"
                st.session_state["user_id"] = user_id
                st.success("login successful! redirecting to home page...")
            else:
                st.error("invalid username or password")

    if st.button("back to home"):
        st.session_state["current_page"] = "home"

    # Geçerli sayfayı kontrol et ve yönlendirme yap
    if st.session_state["current_page"] == "home" and st.session_state["logged_in"]:
        st.stop()  # Sayfa değişimlerini işlemek için Streamlit'in akışını durdurur

def main():
    show_login_page()

if __name__ == "__main__":
    main()