import streamlit as st
from database import SongSearch
from playlist_page import show_playlist_page

def show_home_page():
    st.set_page_config(page_title="TOBBify", layout="wide")
    
    st.image("tobbify.svg", width=500)
    
    # Song Search Bar
    search_term = st.text_input("ŞARKI ARA", placeholder="Şarkı adı girin...")
    
    # Perform search when user hits enter
    if search_term:
        search_results = SongSearch.search_songs(search_term)
        
        if search_results:
            st.write("Arama Sonuçları:")
            for song in search_results:
                st.write(song)
        else:
            st.write("Eşleşen şarkı bulunamadı.")
    
    st.title("Welcome to TOBBify!")
    
    # Initialize session state
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "home"
    
    if st.session_state.get("logged_in"):
        st.write(f"Welcome back, {st.session_state['username']}!")
        st.write("Explore your personalized music experience.")
        
        cols = st.columns(2)
        with cols[0]:
            if st.button("Çalma Listeleri"):
                show_playlist_page()
        
        with cols[1]:
            if st.button("Logout"):
                st.session_state["logged_in"] = False
                st.session_state["username"] = ""
                st.session_state["user_id"] = None
                st.experimental_rerun()
    else:
        st.write("Your personalized music experience awaits. Log in to explore!")
        if st.button("Login"):
            st.session_state["current_page"] = "login"
            st.experimental_rerun()
