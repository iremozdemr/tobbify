import random
from faker import Faker
import psycopg2
import json

def connect_to_db():
    """Establish a connection to the PostgreSQL database."""
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="TOBBify",
            user="postgres",
            password="4664"
        )
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to the database: {e}")
        return None

def insert_random_subscriptions(conn):
    """Insert random subscriptions into the subscription table with random dates."""
    cur = conn.cursor()
    fake = Faker()
    subscription_types = ['Free', 'Premium', 'Family']
    subscription_ids = []

    for sub_type in subscription_types:
        try:
            start_date = fake.date_between(start_date='-5y', end_date='-1y')  # 1-5 yıl önce
            end_date = fake.date_between(start_date=start_date, end_date='+3y')  # 1-3 yıl sonra
            cur.execute("""
                INSERT INTO subscription (subscription_type, start_date, end_date)
                VALUES (%s, %s, %s)
                RETURNING subscription_id
            """, (
                sub_type,
                start_date,
                end_date
            ))
            subscription_ids.append(cur.fetchone()[0])
        except psycopg2.Error as e:
            print(f"Error inserting subscription: {e}")
            conn.rollback()

    conn.commit()
    cur.close()
    return subscription_ids

def insert_random_users(conn, subscription_ids, num_users=50):
    """Insert random users into the user table with unique subscription_id."""
    fake = Faker()
    cur = conn.cursor()
    user_ids = []

    for _ in range(num_users):
        try:
            cur.execute("""
                INSERT INTO "user" (username, email, passwd, subscription_id)
                VALUES (%s, %s, %s, %s)
                RETURNING user_id
            """, (
                fake.user_name(),
                fake.email(),
                fake.password(),
                random.choice(subscription_ids)  # Assign a random subscription_id
            ))
            user_ids.append(cur.fetchone()[0])
        except psycopg2.Error as e:
            print(f"Error inserting user: {e}")
            conn.rollback()

    conn.commit()
    cur.close()
    return user_ids

def insert_random_playlists(conn, user_ids, song_ids, max_playlists_per_user=5, max_songs_per_playlist=10):
    """Insert random playlists and populate playlist_song table with random dates."""
    cur = conn.cursor()
    fake = Faker()
    playlist_ids = []

    for user_id in user_ids:
        num_playlists = random.randint(1, max_playlists_per_user)
        for _ in range(num_playlists):
            try:
                # Insert playlist with random creation date
                created_at = fake.date_time_between(start_date='-5y', end_date='now')
                cur.execute("""
                    INSERT INTO playlist (name, created_at, user_id)
                    VALUES (%s, %s, %s)
                    RETURNING playlist_id
                """, (f"Playlist {random.randint(1, 1000)}", created_at, user_id))
                playlist_id = cur.fetchone()[0]
                playlist_ids.append(playlist_id)

                # Add random songs to playlist with random added_at dates
                num_songs = random.randint(1, max_songs_per_playlist)
                selected_songs = random.sample(song_ids, num_songs)
                for position, song_id in enumerate(selected_songs, start=1):
                    added_at = fake.date_time_between(start_date=created_at, end_date='now')
                    cur.execute("""
                        INSERT INTO playlist_song (playlist_id, song_id, position, added_at)
                        VALUES (%s, %s, %s, %s)
                    """, (playlist_id, song_id, position, added_at))
            except psycopg2.Error as e:
                print(f"Error inserting playlist or songs: {e}")
                conn.rollback()

    conn.commit()
    cur.close()
    return playlist_ids

import json  # JSON formatı için gerekli

def insert_random_concerts(conn, artist_ids, num_concerts=30):
    """Insert random concerts into the concert table with proper JSON location."""
    fake = Faker()
    cur = conn.cursor()
    concert_ids = []

    for _ in range(num_concerts):
        try:
            concert_date = fake.date_between(start_date='-5y', end_date='now')
            location = json.dumps({  # JSON formatında location
                "city": fake.city(),
                "state": fake.state()
            })
            cur.execute("""
                INSERT INTO concert (name, date, location, artist_id)
                VALUES (%s, %s, %s, %s)
                RETURNING concert_id
            """, (
                fake.city() + " Music Fest",
                concert_date,
                location,  # JSON formatında location verisi
                random.choice(artist_ids)
            ))
            concert_ids.append(cur.fetchone()[0])
        except psycopg2.Error as e:
            print(f"Error inserting concert: {e}")
            conn.rollback()

    conn.commit()
    cur.close()
    return concert_ids


def insert_concert_songs(conn, concert_ids, song_ids):
    """Associate random songs with concerts."""
    cur = conn.cursor()

    for concert_id in concert_ids:
        num_songs = random.randint(1, 5)  # Each concert has 1-5 songs
        selected_songs = random.sample(song_ids, num_songs)
        for song_id in selected_songs:
            try:
                cur.execute("""
                    INSERT INTO concert_song (concert_id, song_id)
                    VALUES (%s, %s)
                """, (concert_id, song_id))
            except psycopg2.Error as e:
                print(f"Error associating song {song_id} with concert {concert_id}: {e}")
                conn.rollback()

    conn.commit()
    cur.close()

def insert_listening_history(conn, user_ids, song_ids, max_entries_per_user=20):
    """Insert random listening history for each user with random dates."""
    cur = conn.cursor()
    fake = Faker()

    for user_id in user_ids:
        num_entries = random.randint(1, max_entries_per_user)
        for _ in range(num_entries):
            try:
                listened_at = fake.date_time_between(start_date='-5y', end_date='now')
                cur.execute("""
                    INSERT INTO listening_history (user_id, song_id, listened_at, duration)
                    VALUES (%s, %s, %s, %s)
                """, (
                    user_id,
                    random.choice(song_ids),
                    listened_at,
                    random.randint(30, 300)  # Duration in seconds
                ))
            except psycopg2.Error as e:
                print(f"Error inserting listening history: {e}")
                conn.rollback()

    conn.commit()
    cur.close()

def get_ids(conn, table_name, id_column):
    """Retrieve all IDs from a specified table."""
    cur = conn.cursor()
    cur.execute(f"SELECT {id_column} FROM {table_name}")
    ids = [row[0] for row in cur.fetchall()]
    cur.close()
    return ids

def main():
    conn = connect_to_db()
    if not conn:
        return

    try:
        # Insert random subscriptions
        print("Inserting subscriptions...")
        subscription_ids = insert_random_subscriptions(conn)

        # Insert random users
        print("Inserting users...")
        user_ids = insert_random_users(conn, subscription_ids, num_users=50)

        # Get song and artist IDs
        song_ids = get_ids(conn, "song", "song_id")
        artist_ids = get_ids(conn, "artist", "artist_id")

        # Insert playlists and playlist songs
        print("Inserting playlists...")
        insert_random_playlists(conn, user_ids, song_ids)

        # Insert concerts and associate songs
        print("Inserting concerts...")
        concert_ids = insert_random_concerts(conn, artist_ids)
        insert_concert_songs(conn, concert_ids, song_ids)

        # Insert listening history
        print("Inserting listening history...")
        insert_listening_history(conn, user_ids, song_ids)

        print("Database population completed successfully!")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        conn.close()

if __name__ == "__main__":
    main()
