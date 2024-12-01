import streamlit as st
import requests

def search_deezer(query):
    try:
        url = f"https://api.deezer.com/search?q={query}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            tracks = []
            for track in data['data'][:5]:  # Limit to 5 results
                tracks.append({
                    "title": track["title"],
                    "artist": track["artist"]["name"],
                    "preview": track["preview"],  # 30-second preview URL
                    "link": track["link"],  # Deezer track URL
                })
            return tracks
        else:
            st.error("failed to fetch data from deezer")
            return []
    except Exception as e:
        st.error(f"error fetching data from deezer: {e}")
        return []

def show_music_page():
    st.title("music player")

    # Song search bar
    search_query = st.text_input("search for a song on deezer")
    if search_query:
        tracks = search_deezer(search_query)
        if tracks:
            st.write("search results:")
            for track in tracks:
                st.write(f"**{track['title']}** by {track['artist']}")
                st.audio(track["preview"], format="audio/mp3")
                st.write(f"[listen on deezer]({track['link']})")
        else:
            st.write("no results found")
    
    if st.button("back to homepage"):
        st.session_state["current_page"] = "home"

if __name__ == "__main__":
    show_music_page()