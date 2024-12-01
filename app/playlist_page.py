import streamlit as st
from database import PlaylistSearch, DatabaseConnection

def create_playlist(user_id, playlist_name):
    """create a new playlist in the database."""
    conn = DatabaseConnection.connect_to_db()
    if not conn:
        st.error("error connecting to the database")
        return None
    
    try:
        with conn.cursor() as cursor:
            query = """
                insert into public.playlist (name, user_id)
                values (%s, %s)
                returning playlist_id;
            """
            cursor.execute(query, (playlist_name, user_id))
            conn.commit()
            playlist_id = cursor.fetchone()
            if playlist_id:
                return playlist_id[0]
            return None
    except Exception as e:
        st.error(f"error creating playlist: {e}")
        return None
    finally:
        conn.close()

def get_song_by_name(song_name):
    """retrieve songs by name from the database."""
    conn = DatabaseConnection.connect_to_db()
    if not conn:
        st.error("error connecting to the database")
        return []
    
    try:
        with conn.cursor() as cursor:
            query = """
                select song_id, title, duration
                from public.song
                where title ilike %s
                limit 10;
            """
            cursor.execute(query, (f"%{song_name}%",))
            results = cursor.fetchall()
            return [{"song_id": row[0], "title": row[1], "duration": row[2]} for row in results]
    except Exception as e:
        st.error(f"error fetching songs: {e}")
        return []
    finally:
        conn.close()

def add_song_to_playlist(playlist_id, song_id):
    """add a song to a playlist with a dynamic position."""
    conn = DatabaseConnection.connect_to_db()
    if not conn:
        st.error("error connecting to the database")
        return False
    
    try:
        with conn.cursor() as cursor:
            query_position = """
                select coalesce(max(position), 0) + 1 as next_position
                from public.playlist_song
                where playlist_id = %s;
            """
            cursor.execute(query_position, (playlist_id,))
            next_position = cursor.fetchone()[0]

            query_insert = """
                insert into public.playlist_song (playlist_id, song_id, position)
                values (%s, %s, %s);
            """
            cursor.execute(query_insert, (playlist_id, song_id, next_position))
            conn.commit()
            return True
    except Exception as e:
        st.error(f"error adding song to playlist: {e}")
        return False
    finally:
        conn.close()

def delete_playlist(playlist_id):
    """delete a playlist from the database."""
    conn = DatabaseConnection.connect_to_db()
    if not conn:
        st.error("error connecting to the database")
        return False
    
    try:
        with conn.cursor() as cursor:
            query_delete_songs = """
                delete from public.playlist_song
                where playlist_id = %s;
            """
            cursor.execute(query_delete_songs, (playlist_id,))
            
            query_delete_playlist = """
                delete from public.playlist
                where playlist_id = %s;
            """
            cursor.execute(query_delete_playlist, (playlist_id,))
            
            conn.commit()
            return True
    except Exception as e:
        st.error(f"error deleting playlist: {e}")
        return False
    finally:
        conn.close()

def show_playlist_page():
    st.set_page_config(page_title="tobbify playlists", layout="wide")
    
    css_style = """
    <style>
        body {
            background-color: #f0f2f5;
            font-family: arial, sans-serif;
        }
        h1 {
            color: #3498db;
        }
    </style>
    """
    st.markdown(css_style, unsafe_allow_html=True)
    st.markdown('<h1 class="title">my playlists</h1>', unsafe_allow_html=True)

    if not st.session_state.get("logged_in"):
        st.error("please log in first")
        if st.button("login"):
            st.session_state["current_page"] = "login"
            st.session_state["trigger_reload"] = True
        return

    try:
        user_id = st.session_state.get("user_id")
        playlists = PlaylistSearch.get_user_playlists(user_id)

        st.markdown('<h2>create a new playlist</h2>', unsafe_allow_html=True)
        new_playlist_name = st.text_input("enter playlist name")
        if st.button("create"):
            if new_playlist_name.strip():
                playlist_id = create_playlist(user_id, new_playlist_name.strip())
                if playlist_id:
                    st.success(f"playlist '{new_playlist_name}' created successfully!")
                    st.session_state["trigger_reload"] = True
            else:
                st.error("playlist name cannot be empty")

        if playlists:
            selected_playlist = st.selectbox(
                "select a playlist",
                [(playlist["playlist_id"], playlist["name"]) for playlist in playlists],
                format_func=lambda x: x[1]
            )
            selected_playlist_id = selected_playlist[0] if selected_playlist else None

            if selected_playlist_id:
                st.markdown('<h2>manage selected playlist</h2>', unsafe_allow_html=True)
                songs = PlaylistSearch.get_playlist_songs(selected_playlist_id)
                if songs:
                    display_songs = [{key: value for key, value in song.items() if key != 'song_id'} for song in songs]
                    st.table(display_songs)
                else:
                    st.write("this playlist is empty")

                song_name = st.text_input("search for a song")
                if song_name.strip():
                    search_results = get_song_by_name(song_name.strip())
                    if search_results:
                        song_options = {f"{song['title']} (duration: {song['duration']} mins)": song["song_id"] for song in search_results}
                        selected_song = st.selectbox("choose a song to add", options=song_options.keys())
                        if st.button("add song"):
                            song_id = song_options[selected_song]
                            success = add_song_to_playlist(selected_playlist_id, song_id)
                            if success:
                                st.success(f"'{selected_song}' added to the playlist successfully!")
                                st.session_state["trigger_reload"] = True
                    else:
                        st.write("no songs found.")

                if st.button("delete playlist"):
                    success = delete_playlist(selected_playlist_id)
                    if success:
                        st.success("playlist deleted successfully!")
                        st.session_state["trigger_reload"] = True

        if st.button("back to homepage"):
            st.session_state["current_page"] = "home"
            st.session_state["trigger_reload"] = True

    except Exception as e:
        st.error(f"an error occurred: {e}")

    if st.session_state.get("trigger_reload", False):
        st.session_state["trigger_reload"] = False
        st.session_state["reload"] = True  # Simulate reload