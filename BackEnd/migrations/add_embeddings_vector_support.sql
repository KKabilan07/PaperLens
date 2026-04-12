-- Migration: Add embedding vector support to sections table
-- This migration adds the pgvector extension and embedding column to the sections table

-- Step 1: Enable pgvector extension (if not already enabled)
CREATE EXTENSION IF NOT EXISTS vector;

-- Step 2: Modify sections table to use BIGSERIAL IDs and add embedding column
-- Note: If you already have data, we need to handle this carefully
-- Option A: If sections table is empty, just alter the ID type and add embedding
ALTER TABLE IF EXISTS sections 
  ADD COLUMN IF NOT EXISTS embedding vector(384),
  ADD COLUMN IF NOT EXISTS chunk_index INTEGER DEFAULT 0;

-- Step 3: Create index on embedding column for faster searches (HNSW is best for large datasets)
CREATE INDEX IF NOT EXISTS idx_sections_embedding 
  ON sections USING hnsw (embedding vector_cosine_ops);

-- Alternative: IVFFlat index (good for medium-sized datasets)
-- CREATE INDEX IF NOT EXISTS idx_sections_embedding 
--   ON sections USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

-- Step 4: Update composite index for paper_id + embedding
CREATE INDEX IF NOT EXISTS idx_sections_paper_embedding 
  ON sections(paper_id) INCLUDE (embedding);

-- Note: If you need to drop and recreate the sections table with proper schema:
-- This would lose all existing data, so only do this if you're starting fresh

-- Step 5: Verify the schema
-- SELECT column_name, data_type FROM information_schema.columns 
-- WHERE table_name = 'sections' ORDER BY ordinal_position;

-- Step 6: Check indexes
-- SELECT indexname FROM pg_indexes WHERE tablename = 'sections';
