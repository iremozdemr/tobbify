import streamlit as st
import requests
import pandas as pd

def search_deezer(query):
    """Search Deezer for tracks."""
    try:
        url = f"https://api.deezer.com/search?q={query}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            tracks = []
            for track in data['data'][:5]: 
                tracks.append({
                    "title": track["title"],
                    "artist": track["artist"]["name"],
                    "album": track["album"]["title"],
                    "album cover": track["album"]["cover_small"],
                    "duration (s)": track["duration"],
                    "preview": track["preview"],  
                    "deezer link": track["link"],  
                })
            return tracks
        else:
            st.error("failed to fetch data from Deezer")
            return []
    except Exception as e:
        st.error(f"error fetching data from Deezer: {e}")
        return []

def show_music_page():
    st.title("music player 🎵")

    search_query = st.text_input("search for a song, album, or artist 🎤")
    if search_query:
        tracks = search_deezer(search_query)
        if tracks:
            st.write("search results 🎶:")

            track_data = [
                {
                    "title": track["title"],
                    "artist": track["artist"],
                    "album": track["album"],
                    "duration (s)": track["duration (s)"],
                    "deezer link": f"[listen on deezer]({track['deezer link']})",
                }
                for track in tracks
            ]
            df = pd.DataFrame(track_data)
            st.dataframe(df, use_container_width=True)

            for track in tracks:
                st.write(f"**{track['title']}** by {track['artist']}")
                st.image(track["album cover"], width=100, caption=track["album"])
                st.audio(track["preview"], format="audio/mp3")
        else:
            st.write("no results found")
    
    if st.button("back to homepage"):
        st.session_state["current_page"] = "home"

if __name__ == "__main__":
    show_music_page()