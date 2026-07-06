-- Enable pgvector extension for AI similarity search
CREATE EXTENSION IF NOT EXISTS vector;

-- Papers table
CREATE TABLE IF NOT EXISTS papers (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    description TEXT,
    file_path VARCHAR,
    word_count INT4,
    page_count INT4,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Sections table (with vector embeddings)
CREATE TABLE IF NOT EXISTS sections (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    paper_id UUID NOT NULL REFERENCES papers(id) ON DELETE CASCADE,
    section_name TEXT NOT NULL,
    content TEXT NOT NULL,
    page_numbers INT4[], -- represented as _int4 in schema
    created_at TIMESTAMP DEFAULT NOW(),
    chunk_index INT4,
    embedding vector(768) -- 768 dimensions for models/gemini-embedding-001
);

-- Chats table for conversation history
CREATE TABLE IF NOT EXISTS chats (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    paper_id UUID NOT NULL REFERENCES papers(id) ON DELETE CASCADE,
    question TEXT NOT NULL,
    answer TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    provider_used VARCHAR,
    sources TEXT[] -- represented as _text in schema
);
