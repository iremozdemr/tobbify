import psycopg2
import streamlit as st

class DatabaseConnection:
    @staticmethod
    def connect_to_db():
        """establish a connection to the PostgreSQL database"""
        try:
            conn = psycopg2.connect(
                host="localhost",
                database="tobbify",
                user="postgres",
                password="2587"
            )
            return conn
        except psycopg2.Error as e:
            st.error(f"error connecting to the database: {e}")
            return None

class UserAuthentication:
    @staticmethod
    def login(username, password):
        """authenticate user credentials"""
        conn = DatabaseConnection.connect_to_db()
        if not conn:
            return False, None, None
        
        try:
            with conn.cursor() as cursor:
                query = """
                    SELECT user_id, username
                    FROM public.USER
                    WHERE username = %s AND passwd = %s
                """
                cursor.execute(query, (username, password))
                result = cursor.fetchone()
                
                if result:  # Eğer sonuç varsa
                    return True, result[1], result[0]
                else:  # Eğer sonuç yoksa
                    return False, None, None

        except psycopg2.Error as e:
            st.error(f"an error occurred: {e}")
            return False, None, None
        
        finally:
            conn.close()

class SongSearch:
    @staticmethod
    def search_songs(search_term):
        """search for songs and their artists in the database"""
        conn = DatabaseConnection.connect_to_db()
        if not conn:
            return []
        
        try:
            with conn.cursor() as cursor:
                # Search songs and join with artist table
                query = """
                    SELECT s.title, a.artist_name
                    FROM public.SONG s
                    INNER JOIN public.SONG_ARTIST sa ON s.song_id = sa.song_id
                    INNER JOIN public.ARTIST a ON sa.artist_id = a.artist_id
                    WHERE s.title ILIKE %s
                    LIMIT 5
                """
                cursor.execute(query, (f"%{search_term}%",))
                results = cursor.fetchall()
                
                # Format the results
                return ["{} by {}".format(title, artist_name) for title, artist_name in results]
        
        except psycopg2.Error as e:
            st.error(f"an error occurred: {e}")
            return []
        
        finally:
            conn.close()

class PlaylistSearch:
    @staticmethod
    def get_user_playlists(user_id):
        """retrieve all playlists for a specific user"""
        conn = DatabaseConnection.connect_to_db()
        if not conn:
            return []
        
        try:
            with conn.cursor() as cursor:
                query = """
                    SELECT playlist_id, name, created_at
                    FROM public.PLAYLIST
                    WHERE user_id = %s
                """
                cursor.execute(query, (user_id,))
                results = cursor.fetchall()
                
                # Format the results
                playlists = []
                for row in results:
                    playlists.append({
                        'playlist_id': row[0],
                        'name': row[1],
                        'created_at': row[2]
                    })
                return playlists
        except psycopg2.Error as e:
            st.error(f"An error occurred: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def get_playlist_songs(playlist_id):
        """retrieve all songs in a specific playlist"""
        conn = DatabaseConnection.connect_to_db()
        if not conn:
            return []
        
        try:
            with conn.cursor() as cursor:
                query = """
                    SELECT s.song_id, s.title, s.duration, g.name AS genre
                    FROM public.PLAYLIST_SONG ps
                    INNER JOIN public.SONG s ON ps.song_id = s.song_id
                    INNER JOIN public.GENRE g ON s.genre_id = g.genre_id
                    WHERE ps.playlist_id = %s
                """
                cursor.execute(query, (playlist_id,))
                results = cursor.fetchall()
                
                # Format the results
                songs = []
                for row in results:
                    songs.append({
                        'song_id': row[0],
                        'title': row[1],
                        'duration': row[2],
                        'genre': row[3]
                    })
                return songs
        except psycopg2.Error as e:
            st.error(f"an error occurred: {e}")
            return []
        finally:
            conn.close()