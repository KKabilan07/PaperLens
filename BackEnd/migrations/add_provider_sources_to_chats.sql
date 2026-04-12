-- Migration: Add provider_used and sources columns to chats table
-- This migration adds support for storing LLM provider information and paper sources
-- with each chat response for better tracking and attribution

-- Step 1: Add provider_used column
ALTER TABLE chats ADD COLUMN IF NOT EXISTS provider_used VARCHAR(50);

-- Step 2: Add sources column as array of text
ALTER TABLE chats ADD COLUMN IF NOT EXISTS sources TEXT[] DEFAULT '{}';

-- Step 3: Create index on provider_used for query performance
CREATE INDEX IF NOT EXISTS idx_chats_provider ON chats(provider_used);

-- Step 4: Add comment for documentation
COMMENT ON COLUMN chats.provider_used IS 'LLM provider used to generate the answer (gemini, claude, groq)';
COMMENT ON COLUMN chats.sources IS 'Array of source documents/sections used in the RAG response';

-- Verify the migration
-- SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'chats' ORDER BY ordinal_position;
