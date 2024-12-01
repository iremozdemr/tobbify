import streamlit as st
import requests

def search_deezer(query):
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
                    "preview": track["preview"], 
                    "link": track["link"],  
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

    # Custom CSS for border
    st.markdown(
        """
        <style>
        .track-container {
            border: 2px solid #3498db;
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 20px;
            background-color: #f9f9f9;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        }
        .track-title {
            font-size: 18px;
            font-weight: bold;
            color: #333333;
        }
        .track-artist {
            font-size: 16px;
            color: #555555;
        }
        .track-link {
            font-size: 14px;
            color: #3498db;
            text-decoration: none;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    search_query = st.text_input("search for a song, album or artist")
    if search_query:
        tracks = search_deezer(search_query)
        if tracks:
            st.write("search results:")
            for track in tracks:
                st.markdown(
                    f"""
                    <div class="track-container">
                        <img src="{track['album cover']}" alt="album cover" width="100" style="float: left; margin-right: 15px; border-radius: 10px;">
                        <div>
                            <p class="track-title">{track['title']}</p>
                            <p class="track-artist">by {track['artist']}</p>
                            <audio controls style="margin-top: 10px;">
                                <source src="{track['preview']}" type="audio/mpeg">
                                Your browser does not support the audio element.
                            </audio>
                            <p><a href="{track['link']}" class="track-link" target="_blank">listen on deezer</a></p>
                        </div>
                        <div style="clear: both;"></div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        else:
            st.write("no results found")
    
    if st.button("back to homepage"):
        st.session_state["current_page"] = "home"

if __name__ == "__main__":
    show_music_page()