import streamlit as st
from database import PlaylistSearch 

def show_playlist_page():
    st.set_page_config(page_title="TOBBify - Çalma Listeleri", layout="wide")
    
    # Check if the user is logged in
    if not st.session_state.get("logged_in"):
        st.error("Lütfen önce giriş yapın.")
        if st.button("Giriş Yap"):
            st.session_state["current_page"] = "login"
            st.experimental_rerun()
        return
    
    st.title("Çalma Listeleri")
    
    try:
        # Retrieve playlists for the current user
        user_id = st.session_state.get("user_id")
        playlists = PlaylistSearch.get_user_playlists(user_id)
        
        if not playlists:
            st.write("Henüz çalma listesi yok.")
        else:
            # Display each playlist and its songs
            for playlist in playlists:
                st.subheader(f"Playlist: {playlist['name']}")
                st.write(f"Oluşturulma Tarihi: {playlist['created_at']}")
                
                # Retrieve songs for this playlist
                songs = PlaylistSearch.get_playlist_songs(playlist['playlist_id'])
                
                if not songs:
                    st.write("Bu çalma listesi için şarkı yok.")
                else:
                    st.write("Şarkılar:")
                    for song in songs:
                        st.write(f" - {song['title']} (Genre: {song['genre']})")
                
                st.write("---")  # Separator between playlists

        # Add a button to go back to the home page
        if st.button("Ana Sayfa"):
            st.session_state["current_page"] = "home"
            st.experimental_rerun()
    
    except Exception as e:
        st.error(f"An error occurred: {e}")