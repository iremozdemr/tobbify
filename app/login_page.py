import streamlit as st
from database import UserAuthentication

def show_login_page():
    st.set_page_config(page_title="TOBBify Login", layout="wide")
    st.title("Login Page")

    # Oturum durumunu başlat
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "home"

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        success, user, user_id = UserAuthentication.login(username, password)
        if success:
            st.session_state["logged_in"] = True
            st.session_state["username"] = user
            st.session_state["current_page"] = "home"
            st.session_state["user_id"] = user_id
            st.experimental_rerun()
        else:
            st.error("Invalid username or password")

    if st.button("Back to Home"):
        st.session_state["current_page"] = "home"
        st.experimental_rerun()

def main():
    show_login_page()

if __name__ == "__main__":
    main()