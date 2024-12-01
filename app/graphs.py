import streamlit as st
import matplotlib.pyplot as plt
from database import DatabaseConnection

def show_visualization_page():
    st.set_page_config(page_title="tobbify stats", layout="wide")

    st.markdown(
        """
        <style>
        body {
            background-color: #f0f2f6;
        }
        h1 {
            color: #3498db;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<h1>tobbify stats</h1>", unsafe_allow_html=True)

    conn = DatabaseConnection.connect_to_db()
    if not conn:
        st.error("failed to connect to the database")
        return

    try:
        with conn.cursor() as cursor:
            # Genre distribution
            cursor.execute("SELECT g.name, COUNT(s.song_id) FROM GENRE g JOIN SONG s ON g.genre_id = s.genre_id GROUP BY g.name;")
            genre_data = cursor.fetchall()
            genres, song_counts = zip(*genre_data)

            # Concerts per artist
            cursor.execute("""
                SELECT a.artist_name, COUNT(c.concert_id) 
                FROM ARTIST a 
                LEFT JOIN CONCERT c ON a.artist_id = c.artist_id 
                GROUP BY a.artist_name ORDER BY COUNT(c.concert_id) DESC LIMIT 5;
            """)
            concert_data = cursor.fetchall()
            concert_artists, concert_counts = zip(*concert_data)

            # Top artists
            cursor.execute("""
                SELECT a.artist_name, COUNT(lh.song_id) 
                FROM ARTIST a 
                JOIN SONG_ARTIST sa ON a.artist_id = sa.artist_id 
                JOIN LISTENING_HISTORY lh ON sa.song_id = lh.song_id 
                GROUP BY a.artist_name ORDER BY COUNT(lh.song_id) DESC LIMIT 5;
            """)
            artist_data = cursor.fetchall()
            artists, listen_counts = zip(*artist_data)

            # Subscription data
            cursor.execute("""
                SELECT s.subscription_type, COUNT(u.user_id) 
                FROM SUBSCRIPTION s 
                LEFT JOIN "user" u ON s.subscription_id = u.subscription_id 
                GROUP BY s.subscription_type;
            """)
            subscription_data = cursor.fetchall()
            subscription_types, user_counts = zip(*subscription_data)

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("genre distribution")
                fig, ax = plt.subplots(figsize=(6, 4))
                ax.bar(genres, song_counts, color="skyblue")
                ax.set_xlabel("genres")
                ax.set_ylabel("number of songs")
                ax.set_title("number of songs per genre")
                st.pyplot(fig)

                st.subheader("subscription distribution")
                fig, ax = plt.subplots(figsize=(6, 4))
                ax.bar(subscription_types, user_counts, color="orange")
                ax.set_xlabel("subscription type")
                ax.set_ylabel("number of users")
                ax.set_title("number of users per subscription type")
                st.pyplot(fig)

            with col2:
                st.subheader("concerts per artist")
                fig, ax = plt.subplots(figsize=(6, 4))
                ax.barh(concert_artists, concert_counts, color="purple")
                ax.set_xlabel("number of concerts")
                ax.set_ylabel("artist")
                ax.set_title("top 5 artists by concerts")
                st.pyplot(fig)

                st.subheader("top artists")
                fig, ax = plt.subplots(figsize=(6, 4))
                ax.pie(listen_counts, labels=artists, autopct='%1.1f%%', startangle=90)
                ax.set_title("top 5 artists by number of listens")
                st.pyplot(fig)
                
    except Exception as e:
        st.error(f"an error occurred: {e}")
    finally:
        conn.close()