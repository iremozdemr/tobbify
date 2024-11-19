import streamlit as st
import pandas as pd
from typing import List

# Streamlit Page Configuration
st.set_page_config(page_title="TOBBify", layout="wide")

# Display the logo at the top
st.image("logo.png", width=500)

# Custom CSS 
st.markdown("""
    <style>
    /* Background */
    body {
        background-color: #121212;
        color: #ffffff;
    }
    .sidebar .sidebar-content {
        background-color: #191414;
    }
    .stButton > button {
        color: #ffffff;
        background-color: #3c78d8;  /* Yeni renk */
        border-radius: 20px;
        border: 1px solid #3c78d8; /* Yeni renk */
    }
    .stButton > button:hover {
        background-color: #5a8dee;  /* Daha açık mavi ton */
    }
    .stRadio > div {
        color: #ffffff;
    }
    .stSelectbox > div > div {
        color: #000000; /* Dropdown text color */
    }
    table {
        color: #ffffff;
    }
    .css-1cpxqw2, .css-1d391kg {  /* Table header */
        color: #ffffff;
        background-color: #3c78d8;  /* Yeni renk */
    }
    h1, h2, h3, h4, h5, h6 {
        color: #3c78d8;  /* Yeni renk */
    }
    </style>
""", unsafe_allow_html=True)

# Mock Data
songs_data = [
    {"song_id": 1, "title": "Song A", "artist": "Artist A", "album": "Album A", "genre": "Pop"},
    {"song_id": 2, "title": "Song B", "artist": "Artist B", "album": "Album B", "genre": "Rock"},
    {"song_id": 3, "title": "Song C", "artist": "Artist C", "album": "Album C", "genre": "Jazz"},
    {"song_id": 4, "title": "Song D", "artist": "Artist D", "album": "Album D", "genre": "Classical"},
    {"song_id": 5, "title": "Song E", "artist": "Artist E", "album": "Album E", "genre": "Hip-Hop"},
]
songs_df = pd.DataFrame(songs_data)

# Functions
def search_songs(query: str) -> pd.DataFrame:
    """Search for songs based on a query."""
    return songs_df[songs_df.apply(lambda row: query.lower() in row["title"].lower() or query.lower() in row["artist"].lower(), axis=1)]

def get_recommendations(playback_history: List[int]) -> pd.DataFrame:
    """Generate song recommendations based on playback history."""
    if not playback_history:
        return pd.DataFrame()
    last_played = playback_history[-1]
    genre = songs_df[songs_df["song_id"] == last_played]["genre"].values[0]
    return songs_df[songs_df["genre"] == genre]

# Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Search", "Playlists"])

# User session state for playlists and playback history
if "playlists" not in st.session_state:
    st.session_state["playlists"] = {}
if "playback_history" not in st.session_state:
    st.session_state["playback_history"] = []

if page == "Home":
    st.header("Welcome to TOBBify!")
    st.subheader("Recommended Songs")
    recommendations = get_recommendations(st.session_state["playback_history"])
    if recommendations.empty:
        st.write("Play some songs to get recommendations!")
    else:
        st.table(recommendations)

elif page == "Search":
    st.header("Search Songs")
    query = st.text_input("Search for songs or artists:")
    if query:
        results = search_songs(query)
        if not results.empty:
            st.table(results)
            selected_song = st.selectbox("Select a song to play:", results["title"].tolist())
            if st.button("Play"):
                song_id = results[results["title"] == selected_song]["song_id"].values[0]
                st.session_state["playback_history"].append(song_id)
                st.success(f"Now playing: {selected_song}")
        else:
            st.write("No results found.")

elif page == "Playlists":
    st.header("Manage Playlists")
    playlist_name = st.text_input("Create a new playlist:")
    if st.button("Create Playlist"):
        if playlist_name and playlist_name not in st.session_state["playlists"]:
            st.session_state["playlists"][playlist_name] = []
            st.success(f"Playlist '{playlist_name}' created!")
        else:
            st.error("Playlist name is invalid or already exists.")

    st.subheader("Your Playlists")
    for playlist, songs in st.session_state["playlists"].items():
        with st.expander(playlist):
            if songs:
                playlist_songs = songs_df[songs_df["song_id"].isin(songs)]
                st.table(playlist_songs)
            else:
                st.write("No songs in this playlist yet.")
            available_songs = songs_df[~songs_df["song_id"].isin(songs)]
            add_song = st.selectbox(f"Add a song to '{playlist}':", available_songs["title"].tolist(), key=f"add_{playlist}")
            if st.button(f"Add to {playlist}", key=f"btn_{playlist}"):
                song_id = available_songs[available_songs["title"] == add_song]["song_id"].values[0]
                st.session_state["playlists"][playlist].append(song_id)
                st.success(f"Added {add_song} to '{playlist}'")

# Footer
st.sidebar.markdown("**TOBBify Team © 2024**")