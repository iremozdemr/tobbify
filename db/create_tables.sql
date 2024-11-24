-- VERİTABANI OLUŞTUR
-- CREATE DATABASE tobbify;

-- VERİTABANINA BAĞLAN
-- \c tobbify;

-- TABLOLARI OLUŞTUR

-- SUBSCRIPTION TABLOSU
CREATE TABLE "subscription" (
    subscription_id SERIAL PRIMARY KEY,
    subscription_type VARCHAR(200) NOT NULL,
    start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP
);

-- USER TABLOSU
CREATE TABLE "user" (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(200) UNIQUE NOT NULL,
    email VARCHAR(200) UNIQUE NOT NULL,
    passwd VARCHAR(200) NOT NULL,
    subscription_id INT,
    FOREIGN KEY (subscription_id) REFERENCES "subscription"(subscription_id)
);

-- ARTIST TABLOSU
CREATE TABLE ARTIST (
    artist_id SERIAL PRIMARY KEY,
    artist_name VARCHAR(200) NOT NULL
);

-- ALBUM TABLOSU
CREATE TABLE ALBUM (
    album_id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    release_year INT 
);

-- ALBUM_ARTIST TABLOSU
CREATE TABLE ALBUM_ARTIST (
    album_id INT NOT NULL,
    artist_id INT NOT NULL,
    PRIMARY KEY (album_id, artist_id),
    FOREIGN KEY (album_id) REFERENCES ALBUM(album_id),
    FOREIGN KEY (artist_id) REFERENCES ARTIST(artist_id)
);

-- GENRE TABLOSU
CREATE TABLE GENRE (
    genre_id SERIAL PRIMARY KEY,
    name VARCHAR(200) UNIQUE NOT NULL
);

-- SONG TABLOSU
CREATE TABLE SONG (
    song_id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    duration REAL,
    genre_id INT,
    FOREIGN KEY (genre_id) REFERENCES GENRE(genre_id)
);

-- ALBUM_SONG TABLOSU
CREATE TABLE ALBUM_SONG (
    album_id INT NOT NULL,
    song_id INT NOT NULL,
    "position" INT,
    PRIMARY KEY (album_id, song_id),
    FOREIGN KEY (album_id) REFERENCES ALBUM(album_id),
    FOREIGN KEY (song_id) REFERENCES SONG(song_id)
);

-- SONG_ARTIST TABLOSU
CREATE TABLE SONG_ARTIST (
    song_id INT NOT NULL,
    artist_id INT NOT NULL,
    PRIMARY KEY (song_id, artist_id),
    FOREIGN KEY (song_id) REFERENCES SONG(song_id),
    FOREIGN KEY (artist_id) REFERENCES ARTIST(artist_id)
);

-- PLAYLIST TABLOSU
CREATE TABLE PLAYLIST (
    playlist_id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES "user"(user_id)
);

-- PLAYLIST_SONG TABLOSU
CREATE TABLE PLAYLIST_SONG (
    playlist_id INT NOT NULL,
    song_id INT NOT NULL,
    "position" INT,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (playlist_id, song_id),
    FOREIGN KEY (playlist_id) REFERENCES PLAYLIST(playlist_id),
    FOREIGN KEY (song_id) REFERENCES SONG(song_id)
);

-- LISTENING_HISTORY TABLOSU
CREATE TABLE LISTENING_HISTORY (
    user_id INT NOT NULL,
    song_id INT NOT NULL,
    listened_at TIMESTAMP NOT NULL,
    duration REAL,
    PRIMARY KEY (user_id, listened_at),
    FOREIGN KEY (user_id) REFERENCES "user"(user_id),
    FOREIGN KEY (song_id) REFERENCES SONG(song_id)
);

-- CONCERT TABLOSU
CREATE TABLE CONCERT (
    concert_id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    date TIMESTAMP,
    location JSON,
    artist_id INT,
    FOREIGN KEY (artist_id) REFERENCES ARTIST(artist_id)
);

-- CONCERT_SONG TABLOSU
CREATE TABLE CONCERT_SONG (
    concert_id INT NOT NULL,
    song_id INT NOT NULL,
    PRIMARY KEY (concert_id, song_id),
    FOREIGN KEY (concert_id) REFERENCES CONCERT(concert_id),
    FOREIGN KEY (song_id) REFERENCES SONG(song_id)
);

-- LYRICS TABLOSU
CREATE TABLE LYRICS (
    lyrics_id SERIAL PRIMARY KEY,
    song_id INT NOT NULL,
    content TEXT NOT NULL,
    FOREIGN KEY (song_id) REFERENCES SONG(song_id)
);