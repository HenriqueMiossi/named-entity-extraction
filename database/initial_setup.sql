CREATE DATABASE IF NOT EXISTS vector_db;
CREATE EXTENSION vector;

CREATE TABLE IF NOT EXISTS vector_db.articles (
    id bigserial PRIMARY KEY,
    embedding vector(3)
);