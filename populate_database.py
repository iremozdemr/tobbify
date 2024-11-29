import pandas as pd
import psycopg2
from psycopg2 import sql

def connect_to_db():
    """Establish a connection to the PostgreSQL database"""
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

def insert_genres(conn, genres):
    """Insert unique genres into the GENRE table"""
    cur = conn.cursor()
    genre_ids = {}
    
    for genre in genres:
        try:
            # First, try to see if the genre already exists
            cur.execute("SELECT genre_id FROM GENRE WHERE name = %s", (genre,))
            existing_genre = cur.fetchone()
            
            if existing_genre:
                # Genre already exists, use existing ID
                genre_ids[genre] = existing_genre[0]
            else:
                # Insert new genre
                cur.execute("""
                    INSERT INTO GENRE (name) 
                    VALUES (%s) 
                    RETURNING genre_id
                """, (genre,))
                genre_ids[genre] = cur.fetchone()[0]
        
        except psycopg2.Error as e:
            print(f"Error inserting genre {genre}: {e}")
            conn.rollback()
    
    conn.commit()
    cur.close()
    return genre_ids

def insert_artists(conn, artists):
    """Insert unique artists into the ARTIST table"""
    cur = conn.cursor()
    artist_ids = {}
    
    for artist in artists:
        try:
            # First, try to see if the artist already exists
            cur.execute("SELECT artist_id FROM ARTIST WHERE artist_name = %s", (artist,))
            existing_artist = cur.fetchone()
            
            if existing_artist:
                # Artist already exists, use existing ID
                artist_ids[artist] = existing_artist[0]
            else:
                # Insert new artist
                cur.execute("""
                    INSERT INTO ARTIST (artist_name) 
                    VALUES (%s) 
                    RETURNING artist_id
                """, (artist,))
                artist_ids[artist] = cur.fetchone()[0]
        
        except psycopg2.Error as e:
            print(f"Error inserting artist {artist}: {e}")
            conn.rollback()
    
    conn.commit()
    cur.close()
    return artist_ids

def insert_songs(conn, df, genre_ids, artist_ids):
    """Insert songs into the SONG table and associated data"""
    cur = conn.cursor()
    song_ids = {}
    
    for _, row in df.iterrows():
        try:
            # Insert song
            cur.execute("""
                INSERT INTO SONG (title, duration, genre_id) 
                VALUES (%s, %s, %s) 
                RETURNING song_id
            """, (
                row['track_name'], 
                row['len'], 
                genre_ids.get(row['genre'])
            ))
            song_id = cur.fetchone()[0]
            song_ids[row['track_name']] = song_id
            
            # Insert lyrics
            cur.execute("""
                INSERT INTO LYRICS (song_id, content) 
                VALUES (%s, %s)
            """, (song_id, row['lyrics']))
            
            # Insert song-artist relationship
            cur.execute("""
                INSERT INTO SONG_ARTIST (song_id, artist_id) 
                VALUES (%s, %s)
            """, (song_id, artist_ids[row['artist_name']]))
        
        except psycopg2.Error as e:
            print(f"Error inserting song {row['track_name']}: {e}")
            conn.rollback()
    
    conn.commit()
    cur.close()
    return song_ids

def insert_albums(conn, df, artist_ids, song_ids):
    """Insert albums and their song relationships"""
    cur = conn.cursor()
    album_ids = {}
    
    # Group by unique album names
    album_groups = df.groupby(['artist_name', 'release_date'])
    
    for (artist, release_date), group in album_groups:
        try:
            # Insert album
            cur.execute("""
                INSERT INTO ALBUM (name, release_year) 
                VALUES (%s, %s) 
                RETURNING album_id
            """, (f"{artist} - {release_date}", int(release_date)))
            album_id = cur.fetchone()[0]
            album_ids[(artist, release_date)] = album_id
            
            # Insert album-artist relationship
            cur.execute("""
                INSERT INTO ALBUM_ARTIST (album_id, artist_id) 
                VALUES (%s, %s)
            """, (album_id, artist_ids[artist]))
            
            # Insert album-song relationships
            for idx, track in enumerate(group['track_name'], 1):
                cur.execute("""
                    INSERT INTO ALBUM_SONG (album_id, song_id, "position") 
                    VALUES (%s, %s, %s)
                """, (album_id, song_ids[track], idx))
        
        except psycopg2.Error as e:
            print(f"Error inserting album for {artist} - {release_date}: {e}")
            conn.rollback()
    
    conn.commit()
    cur.close()
    return album_ids

def main():
    df = pd.read_csv('dataset.csv')
    
    # Database connection
    conn = connect_to_db()
    if not conn:
        return
    
    try:
        # Insert genres
        genre_ids = insert_genres(conn, df['genre'].unique())
        
        # Insert artists
        artist_ids = insert_artists(conn, df['artist_name'].unique())
        
        # Insert songs and lyrics
        song_ids = insert_songs(conn, df, genre_ids, artist_ids)
        
        # Insert albums
        insert_albums(conn, df, artist_ids, song_ids)
        
        print("Database population completed successfully!")
    
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        conn.close()

if __name__ == "__main__":
    main()