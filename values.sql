-- Genre Tablosu
INSERT INTO GENRE (name)
VALUES
    ('Rock'),
    ('Pop'),
    ('Jazz'),
    ('Classical'),
    ('Hip-Hop');

-- Performer Tablosu
INSERT INTO PERFORMER (performer_name)
VALUES
    ('The Beatles'),
    ('Taylor Swift'),
    ('Miles Davis'),
    ('Ludwig van Beethoven'),
	('irem'),
	('ezgi'),
	('inci'),
    ('Eminem');

-- Album Tablosu
INSERT INTO ALBUM (name, release_year)
VALUES
    ('Abbey Road', 1969),
    ('1989', 2014),
    ('Kind of Blue', 1959),
    ('Symphony No. 9', 1824),
    ('The Marshall Mathers LP', 2000);

-- User Tablosu
INSERT INTO "user" (username, email, passwd)
VALUES
    ('john_doe', 'john.doe@example.com', 'password123'),
    ('jane_smith', 'jane.smith@example.com', 'passw0rd'),
    ('alice', 'alice@example.com', 'alice123'),
    ('bob', 'bob@example.com', 'bobsecure'),
    ('charlie', 'charlie@example.com', 'charliepwd');

-- Subscription Tablosu
INSERT INTO "subscription" (subscription_type, start_date, end_date)
VALUES
    ('Free', '2024-01-01 00:00:00', NULL),
    ('Premium', '2024-01-01 00:00:00', '2024-12-31 23:59:59'),
    ('Family', '2024-01-01 00:00:00', '2024-12-31 23:59:59'),
    ('Student', '2024-01-01 00:00:00', '2024-06-30 23:59:59'),
    ('Trial', '2024-11-01 00:00:00', '2024-11-30 23:59:59');

-- Artist Tablosu
INSERT INTO ARTIST (artist_id, birth_date)
VALUES
    (2, '1989-12-13'),
    (3, '1926-05-26'),
    (4, '1770-12-17'),
    (5, '1972-10-17'),
	(6, '1770-12-17'),
	(7, '1770-12-17'),
	(8, '1770-12-17');

-- Artist_Group Tablosu
INSERT INTO ARTIST_GROUP (group_id, num_artist)
VALUES
    (1, 3);

-- Member Tablosu
INSERT INTO MEMBER (artist_id, group_id)
VALUES
    (5, 1),
	(6, 1),
	(7, 1);

-- Album_Performer Tablosu
INSERT INTO ALBUM_PERFORMER (album_id, performer_id)
VALUES
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5);

-- Song Tablosu
INSERT INTO SONG (title, duration, genre_id)
VALUES
    ('Come Together', 4.20, 1),
    ('Shake It Off', 3.39, 2),
    ('So What', 9.22, 3),
    ('Ode to Joy', 7.25, 4),
    ('Lose Yourself', 5.26, 5);

-- Album_Song Tablosu
INSERT INTO ALBUM_SONG (album_id, song_id, "position")
VALUES
    (1, 1, 1),
    (2, 2, 1),
    (3, 3, 1),
    (4, 4, 1),
    (5, 5, 1);

-- Song_Performer Tablosu
INSERT INTO SONG_PERFORMER (song_id, performer_id)
VALUES
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5);

-- Playlist Tablosu
INSERT INTO PLAYLIST (name, user_id)
VALUES
    ('Rock Classics', 1),
    ('Pop Hits', 2),
    ('Jazz Vibes', 3),
    ('Classical Favorites', 4),
    ('Rap Anthems', 5);

-- Playlist_Song Tablosu
INSERT INTO PLAYLIST_SONG (playlist_id, song_id, "position")
VALUES
    (1, 1, 1),
    (2, 2, 1),
    (3, 3, 1),
    (4, 4, 1),
    (5, 5, 1);

-- Concert Tablosu
INSERT INTO CONCERT (name, date, location, performer_id)
VALUES
    ('Beatles Reunion', '2024-12-01 20:00:00', '{"city": "Liverpool", "venue": "Cavern Club"}', 1),
    ('Taylor Live', '2024-11-15 19:00:00', '{"city": "Los Angeles", "venue": "Staples Center"}', 2),
    ('Jazz Night', '2024-10-20 21:00:00', '{"city": "New York", "venue": "Blue Note"}', 3),
    ('Beethoven Symphony', '2024-09-30 18:00:00', '{"city": "Vienna", "venue": "Musikverein"}', 4),
    ('Rap Fest', '2024-08-25 22:00:00', '{"city": "Detroit", "venue": "Fox Theatre"}', 5);

-- Concert_Song Tablosu
INSERT INTO CONCERT_SONG (concert_id, song_id)
VALUES
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5);

-- Listening_History Tablosu
INSERT INTO LISTENING_HISTORY (user_id, song_id, listened_at, duration)
VALUES
    (1, 1, '2024-11-20 12:30:00', 4.20),
    (2, 2, '2024-11-20 13:00:00', 3.39),
    (3, 3, '2024-11-20 14:15:00', 9.22),
    (4, 4, '2024-11-20 15:00:00', 7.25),
    (5, 5, '2024-11-20 16:45:00', 5.26);

-- Lyrics Tablosu
INSERT INTO LYRICS (song_id, content)
VALUES
    (1, 'Here come old flat top, he come grooving up slowly...'),
    (2, 'Cause the players gonna play, play, play...'),
    (3, 'Miles ahead, blue in green...'),
    (4, 'Freude, schöner Götterfunken...'),
    (5, 'You better lose yourself in the music, the moment...');