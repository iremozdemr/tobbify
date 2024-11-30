import streamlit as st
from database import SongSearch
import pandas as pd


def show_home_page():
    # Page configuration
    st.set_page_config(page_title="tobbify - home", layout="wide")
    
    # Custom CSS for improved aesthetics
    st.markdown(
        """
        <style>
        body {
            background-color: #f0f2f6;
        }
        h1 {
            color: #3498db;
            font-size: 72px;
            text-align: center;
            font-family: Arial, sans-serif;
        }
        .section-title1 {
            color: #2c3e50;
            font-size: 24px;
            text-align: center;
            margin-top: 20px;
            margin-bottom: 20px;
            font-family: Arial, sans-serif;
            margin-bottom: 50px;
        }
        .section-title2 {
            color: #2c3e50;
            font-size: 24px;
            text-align: center;
            margin-top: 20px;
            font-family: Arial, sans-serif;
        }
        .button-container {
            display: flex;
            justify-content: center;
            gap: 20px; /* Space between buttons */
            margin-top: 10px; /* Space after search bar */
        }
        .search-container {
            background-color: #ffffff;
            border-radius: 10px;
            padding: 20px;
            margin: 20px auto 40px auto;
            max-width: 600px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        }
        .search-container input {
            font-size: 16px;
        }
        .enlarged-button {
            font-size: 20px;
            padding: 15px 30px;
            background-color: #3498db;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        .enlarged-button:hover {
            background-color: #1d6fa5;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # TOBBify heading and description
    st.markdown("<h1>tobbify</h1>", unsafe_allow_html=True)
    st.markdown('<p class="section-title1">your personalized music streaming experience!</p>', unsafe_allow_html=True)

    # Song search bar
    search_term = st.text_input("search for songs", placeholder="enter song name...")
    if search_term:
        search_results = SongSearch.search_songs(search_term)
        if search_results:
            st.markdown('<p class="section-title1">search results:</p>', unsafe_allow_html=True)
            split_results = [
                {
                    "song title": song.split("by", 1)[0].strip(),
                    "artist": song.split("by", 1)[1].strip(),
                }
                if "by" in song.lower()
                else {"song title": song.strip(), "artist": "unknown"}
                for song in search_results
            ]
            df = pd.DataFrame(split_results)
            st.table(df)
        else:
            st.markdown('<p class="section-title1">no matching songs found</p>', unsafe_allow_html=True)

    # Initialize session state
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "home"

    if st.session_state.get("logged_in"):
        st.write(f"welcome back, {st.session_state['username']}!")
        st.write("explore your personalized music experience")
        
        cols = st.columns(2)
        with cols[0]:
            if st.button("view playlists"):
                st.session_state["current_page"] = "playlists"
        with cols[1]:
            if st.button("logout"):
                st.session_state["logged_in"] = False
                st.session_state["username"] = ""
                st.session_state["user_id"] = None
                st.session_state["current_page"] = "home"
    else:
        st.write("your personalized music experience awaits, login to explore!")
        if st.button("login"):
            st.session_state["current_page"] = "login"
        if st.button("sign up"):
            st.session_state["current_page"] = "signup"

    # Redirect to the correct page based on current_page
    if st.session_state["current_page"] == "login":
        st.write("redirecting to login page...")
    elif st.session_state["current_page"] == "signup":
        st.write("redirecting to sign up page...")
    elif st.session_state["current_page"] == "playlists":
        st.write("redirecting to playlists page...")