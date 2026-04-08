-- Supabase SQL Functions for pgvector Similarity Search
-- Copy these into your Supabase SQL Editor and run them

-- Function 1: Search sections in a specific paper
CREATE OR REPLACE FUNCTION sections_similarity_search(
    query_embedding vector(384),
    paper_id_param uuid,
    top_k int DEFAULT 5,
    similarity_threshold float DEFAULT 0.3
)
RETURNS TABLE (
    id bigint,
    paper_id uuid,
    section_name text,
    content text,
    chunk_index int,
    similarity float
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        s.id,
        s.paper_id,
        s.section_name,
        s.content,
        s.chunk_index,
        (1 - (s.embedding <=> query_embedding)) as similarity
    FROM sections s
    WHERE s.paper_id = paper_id_param
        AND (1 - (s.embedding <=> query_embedding)) > similarity_threshold
    ORDER BY s.embedding <=> query_embedding
    LIMIT top_k;
END;
$$ LANGUAGE plpgsql;


-- Function 2: Search sections across all papers (multi-paper analysis)
CREATE OR REPLACE FUNCTION sections_similarity_search_global(
    query_embedding vector(384),
    top_k int DEFAULT 10,
    similarity_threshold float DEFAULT 0.3
)
RETURNS TABLE (
    id bigint,
    paper_id uuid,
    section_name text,
    content text,
    chunk_index int,
    similarity float
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        s.id,
        s.paper_id,
        s.section_name,
        s.content,
        s.chunk_index,
        (1 - (s.embedding <=> query_embedding)) as similarity
    FROM sections s
    WHERE (1 - (s.embedding <=> query_embedding)) > similarity_threshold
    ORDER BY s.embedding <=> query_embedding
    LIMIT top_k;
END;
$$ LANGUAGE plpgsql;


-- Function 3: Get sections by paper (for bulk retrieval)
CREATE OR REPLACE FUNCTION get_paper_sections(
    paper_id_param uuid
)
RETURNS TABLE (
    id bigint,
    section_name text,
    chunk_count int,
    total_chars int
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        s.id,
        s.section_name,
        COUNT(*)::int as chunk_count,
        SUM(LENGTH(s.content))::int as total_chars
    FROM sections s
    WHERE s.paper_id = paper_id_param
    GROUP BY s.id, s.section_name
    ORDER BY s.section_name;
END;
$$ LANGUAGE plpgsql;


-- Important: Create pgvector extension in Supabase
-- Run this in Supabase SQL Editor:
CREATE EXTENSION IF NOT EXISTS vector;

-- Create index on embedding for faster searches
CREATE INDEX ON sections USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

-- Alternative: HNSW index (better for larger datasets)
-- CREATE INDEX ON sections USING hnsw (embedding vector_cosine_ops);
