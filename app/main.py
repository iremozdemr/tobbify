import streamlit as st
import home_page
import login_page
import signup_page  # Yeni signup modülü
import playlist_page
import subscription

def main():
    # Oturum durumunu başlat
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "home"

    # Geçerli sayfaya göre ilgili sayfayı göster
    if st.session_state["current_page"] == "home":
        home_page.show_home_page()
    elif st.session_state["current_page"] == "login":
        login_page.main()
    elif st.session_state["current_page"] == "signup":
        signup_page.show_signup_page()
    elif st.session_state["current_page"] == "playlists":
        playlist_page.show_playlist_page()
    elif st.session_state["current_page"] == "subscription":
        subscription.show_subscription_page()

if __name__ == "__main__":
    main()