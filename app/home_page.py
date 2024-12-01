import streamlit as st
from database import SongSearch, UserSubscription
import pandas as pd

def show_home_page():
    st.set_page_config(page_title="tobbify - home", layout="wide")

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
        .lyrics-container {
            background-color: #ffffff;
            border: 2px solid #3498db;
            border-radius: 10px;
            padding: 20px;
            margin: 20px auto;
            max-width: 600px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            font-family: 'Courier New', monospace;
            font-size: 16px;
            line-height: 1.5;
            color: #2c3e50;
            overflow-y: auto;
            max-height: 400px;
            white-space: pre-wrap;
        }
        .lyrics-container p {
            margin: 0;
            padding: 0;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<h1>tobbify</h1>", unsafe_allow_html=True)
    st.markdown('<p class="section-title1">your personalized music streaming experience!</p>', unsafe_allow_html=True)

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
            
            selected_song = st.selectbox("select a song to view lyrics", df["song title"])
            
            if selected_song:
                lyrics = SongSearch.get_song_lyrics(selected_song)
                if lyrics:
                    for line in lyrics.split("\n"):
                        st.markdown(f"<p class='lyrics-container'>{line}</p>", unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.warning("lyrics not found")
        else:
            st.markdown('<p class="section-title1">no matching songs found</p>', unsafe_allow_html=True)
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "home"

    if st.session_state.get("logged_in"):
        st.write(f"welcome back, {st.session_state['username']}!")
        st.write("explore your personalized music experience")
        
        cols = st.columns(6)
        with cols[0]:
            if st.button("view playlists"):
                st.session_state["current_page"] = "playlists"
        with cols[1]:
            if st.button("view profile"):
                st.session_state["current_page"] = "subscription"
        with cols[2]:
            if st.button("play song"):
                st.session_state["current_page"] = "music"
        with cols[3]:
            if st.button("song recommendations"):
                st.session_state["current_page"] = "recommendation"
        with cols[4]:
            if st.button("data visualization"):
                st.session_state["current_page"] = "graphs"
        with cols[5]:
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
        
    if st.session_state["current_page"] == "subscription":
        show_subscription_page()
    elif st.session_state["current_page"] == "login":
        st.write("redirecting to login page...")
    elif st.session_state["current_page"] == "signup":
        st.write("redirecting to sign up page...")
    elif st.session_state["current_page"] == "playlists":
        st.write("redirecting to playlists page...")
    elif st.session_state["current_page"] == "music":
        st.write("redirecting to music page...")
    elif st.session_state["current_page"] == "recommendation":
        st.write("redirecting to recommendation page...")


def show_subscription_page():
    st.session_state["current_page"] = "subscription"

def show_music_page():
    st.session_state["current_page"] = "music"