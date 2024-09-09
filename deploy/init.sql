CREATE SCHEMA IF NOT EXISTS content;

CREATE TABLE IF NOT EXISTS content.posts (
    id uuid PRIMARY KEY,
    rubrics TEXT,
    text TEXT,
    created_date TEXT
);