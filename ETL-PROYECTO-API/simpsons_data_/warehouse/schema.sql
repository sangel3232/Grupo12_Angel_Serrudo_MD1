
CREATE TABLE dim_character (
    character_id INT PRIMARY KEY,
    name TEXT,
    gender TEXT,
    occupation TEXT
);

CREATE TABLE dim_episode (
    episode_id INT PRIMARY KEY,
    name TEXT,
    season INT,
    air_date DATE
);

CREATE TABLE fact_episode_character (
    id SERIAL PRIMARY KEY,
    episode_id INT,
    character_id INT
);
