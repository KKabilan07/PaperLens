-- Supabase Database Schema Migration
-- Add pgvector support to sections table

-- 1. Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- 2. Update sections table to include embedding vector
-- If sections table already exists, add the embedding column:
ALTER TABLE sections ADD COLUMN IF NOT EXISTS embedding vector(384);

-- 3. Create indexes for faster similarity search
CREATE INDEX IF NOT EXISTS sections_embedding_idx ON sections USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

-- 4. Create table if it doesn't exist (for fresh setup)
CREATE TABLE IF NOT EXISTS sections (
    id BIGSERIAL PRIMARY KEY,
    paper_id UUID NOT NULL REFERENCES papers(id) ON DELETE CASCADE,
    section_name TEXT NOT NULL,
    content TEXT NOT NULL,
    embedding vector(384) NOT NULL,
    chunk_index INT DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);


    