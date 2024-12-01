import psycopg2
import streamlit as st
import random
from datetime import datetime

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
    def register(username, password, email):
        conn = DatabaseConnection.connect_to_db()
        if not conn:
            st.error("error connecting to the database")
            return False
        
        try:
            with conn.cursor() as cursor:
                query = """
                    INSERT INTO "user" (username, passwd, email, subscription_id)
                    VALUES (%s, %s, %s, %s);
                """
                cursor.execute(query, (username, password, email, 1))  # subscription_id = 1
                conn.commit()
                return True
        except Exception as e:
            st.error(f"error registering user: {e}")
            return False
        finally:
            conn.close()

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

class UserSubscription:
    @staticmethod
    def get_subscription_details(user_id):
        """
        Fetch subscription details for a given user ID.
        """
        conn = DatabaseConnection.connect_to_db()
        if not conn:
            return None

        try:
            with conn.cursor() as cursor:
                query = """
                    SELECT s.subscription_id, s.subscription_type, s.start_date, s.end_date
                    FROM "user" u
                    JOIN subscription s ON u.subscription_id = s.subscription_id
                    WHERE u.user_id = %s
                """
                cursor.execute(query, (user_id,))
                result = cursor.fetchone()

                # Sonuç varsa döndür
                if result:
                    return {
                        "subscription_id": result[0],
                        "subscription_type": result[1],
                        "start_date": result[2],
                        "end_date": result[3],
                    }
                return None
        except psycopg2.Error as e:
            st.error(f"An error occurred: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def update_subscription_type(subscription_id, new_type):
        """
        Update the subscription type for a given subscription ID.
        """
        conn = DatabaseConnection.connect_to_db()
        if not conn:
            return False

        try:
            with conn.cursor() as cursor:
                query = "SELECT subscription_id FROM public.SUBSCRIPTION WHERE subscription_id = %s"
                cursor.execute(query, (subscription_id,))
                existing_subscription = cursor.fetchone()
                
                if not existing_subscription:
                    st.error("Subscription ID does not exist.")
                    return False  


                query = "UPDATE public.SUBSCRIPTION SET subscription_type = %s WHERE subscription_id = %s"
                cursor.execute(query, (new_type, subscription_id))
                conn.commit()
                return True  # Başarılı olduğunda True döner
        except psycopg2.Error as e:
            st.error(f"An error occurred while updating subscription: {e}")
            return False  # Hata durumunda False döner
        finally:
            conn.close()



class SongRecommendation:
    def get_recommendations_by_mood_and_location(mood, location, limit=5):
        mood_to_genre = {
            "cheerful": ["pop", "reggae"],
            "melancholy": ["blues", "country"],
            "calm": ["jazz", "reggae"],
            "energetic": ["rock", "hip hop"],
            "romantic": ["jazz", "blues"]
        }
        
        location_to_genre = {
            "çim amfi": ["pop", "reggae", "rock"],
            "fuaye": ["pop", "hip hop", "rock"],
            "kütüphane": ["jazz", "blues", "country"],
            "etü mutfak": ["blues", "jazz", "reggae"]
        }
        
        # Mood ve mekan için ortak türleri bul
        mood_genres = set(mood_to_genre.get(mood.lower(), []))
        location_genres = set(location_to_genre.get(location.lower(), []))
        common_genres = list(mood_genres & location_genres)
        
        if not common_genres:
            st.warning("No matching genres for this mood and location.")
            return []
        
        conn = DatabaseConnection.connect_to_db()
        if not conn:
            return []
        
        try:
            with conn.cursor() as cursor:
                # SQL sorgusu
                query = """
                    SELECT s.title, a.artist_name, g.name AS genre
                    FROM public.SONG s
                    INNER JOIN public.SONG_ARTIST sa ON s.song_id = sa.song_id
                    INNER JOIN public.ARTIST a ON sa.artist_id = a.artist_id
                    INNER JOIN public.GENRE g ON s.genre_id = g.genre_id
                    WHERE g.name = ANY(%s)
                    ORDER BY RANDOM()
                    LIMIT %s
                """
                cursor.execute(query, (common_genres, limit))
                results = cursor.fetchall()
                
                return [
                    {"title": title, "artist": artist_name, "genre": genre}
                    for title, artist_name, genre in results
                ]
        except psycopg2.Error as e:
            st.error(f"An error occurred: {e}")
            return []
        finally:
            conn.close()
