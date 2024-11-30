import streamlit as st
from database import UserAuthentication

def show_login_page():
    # Sayfa yapılandırması
    st.set_page_config(page_title="tobbify login", layout="wide")
    st.title("login page")

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

    # Giriş durumunu göster
    if st.session_state["logged_in"]:
        st.info(f"logged in as {st.session_state['username']}")

def main():
    show_login_page()

if __name__ == "__main__":
    main()