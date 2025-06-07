CREATE TABLE users (
     id INT PRIMARY KEY,
     subscribe BOOLEAN DEFAULT false
)

INSERT INTO (id, subscribe) VALUES (1, false), (2, true)