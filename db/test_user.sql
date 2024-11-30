INSERT INTO "user" (user_id, username, email, passwd, subscription_id)
VALUES (1000, 'test', 'test@test.com', 'test123', 2);

INSERT INTO PLAYLIST (playlist_id, name, user_id)
VALUES (1000, 'TEST_PLAYLIST', 1000);

-- Rastgele 10 şarkıyı seçme
WITH RandomSongs AS (
    SELECT song_id
    FROM SONG
    ORDER BY RANDOM()
    LIMIT 10
)
-- Seçilen şarkıları playliste ekleme
INSERT INTO PLAYLIST_SONG (playlist_id, song_id, "position")
SELECT 1000, song_id, ROW_NUMBER() OVER ()
FROM RandomSongs;