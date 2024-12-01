DROP INDEX IF EXISTS idx_song_title;

EXPLAIN ANALYZE 
SELECT s.duration
FROM SONG AS s
WHERE s.title = 'cry';

CREATE INDEX idx_song_title ON SONG(title);

EXPLAIN ANALYZE 
SELECT s.duration
FROM SONG AS s
WHERE s.title = 'cry';

CREATE EXTENSION IF NOT EXISTS pg_trgm;

CREATE INDEX idx_song_title ON public.SONG (title);

CREATE INDEX idx_artist_name ON public.ARTIST (artist_name);

CREATE INDEX idx_song_title_gin ON public.SONG USING GIN (title gin_trgm_ops);

CREATE INDEX idx_lyrics_song_id ON lyrics (song_id);

CREATE INDEX idx_song_song_id ON song (song_id);

CREATE INDEX idx_song_title_gin ON song USING GIN (title gin_trgm_ops);

CREATE INDEX idx_genre_name ON public.GENRE (name);

CREATE INDEX idx_song_song_id ON public.SONG (song_id);

CREATE INDEX idx_song_artist_song_id ON public.SONG_ARTIST (song_id);