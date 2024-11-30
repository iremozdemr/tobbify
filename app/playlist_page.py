import streamlit as st
from database import PlaylistSearch 

def show_playlist_page():
    # Page configuration
    st.set_page_config(page_title="tobbify - playlists", layout="wide")
    
    # Check if the user is logged in
    if not st.session_state.get("logged_in"):
        st.error("please log in first.")
        if st.button("login"):
            st.session_state["current_page"] = "login"
        return  # Do not display the rest of the page for non-logged-in users
    
    st.title("playlists")
    
    try:
        # Retrieve user playlists
        user_id = st.session_state.get("user_id")
        playlists = PlaylistSearch.get_user_playlists(user_id)
        
        if not playlists:
            st.write("you don't have any playlists yet.")
        else:
            # Display each playlist and its songs
            for playlist in playlists:
                st.subheader(f"playlist: {playlist['name']}")
                st.write(f"created on: {playlist['created_at']}")
                
                # Retrieve the songs in this playlist
                songs = PlaylistSearch.get_playlist_songs(playlist['playlist_id'])
                
                if not songs:
                    st.write("this playlist has no songs")
                else:
                    st.write("songs:")
                    for song in songs:
                        st.write(f" - {song['title']} (genre: {song['genre']})")
                
                st.write("---")  # Separator between playlists

        # Button to go back to the home page
        if st.button("home"):
            st.session_state["current_page"] = "home"
    
    except Exception as e:
        st.error(f"an error occurred: {e}")