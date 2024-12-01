import streamlit as st
from database import UserAuthentication

def show_signup_page():
    # Sayfa yapılandırması
    st.set_page_config(page_title="tobbify sign up", layout="wide")
    
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

    st.markdown("<h1>sign up</h1>", unsafe_allow_html=True)

    # Kullanıcı adı, şifre ve email giriş alanları
    username = st.text_input("choose a username")
    email = st.text_input("enter your email")
    password = st.text_input("choose a password", type="password")
    confirm_password = st.text_input("confirm your password", type="password")

    if st.button("continue"):
        # Boş alan kontrolü
        if not username or not email or not password or not confirm_password:
            st.error("all fields are required")
        elif password != confirm_password:
            st.error("passwords do not match")
        else:
            success = UserAuthentication.register(username, password, email)
            if success:
                st.success("sign up successful! redirecting to login page...")
                st.session_state["current_page"] = "login"
            else:
                st.error("username already exists. please choose another one.")

    if st.button("back to homepage"):
        st.session_state["current_page"] = "home"