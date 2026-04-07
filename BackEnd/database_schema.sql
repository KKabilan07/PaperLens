-- PaperLens Database Schema
-- This SQL should be run in your Supabase PostgreSQL database

-- Users table (managed by Supabase Auth)
-- Supabase automatically creates this

-- Papers table
CREATE TABLE IF NOT EXISTS papers (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    file_path VARCHAR(512),
    word_count INTEGER,
    page_count INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(id, user_id)
);

-- Sections table
CREATE TABLE IF NOT EXISTS sections (
    id UUID PRIMARY KEY,
    paper_id UUID NOT NULL REFERENCES papers(id) ON DELETE CASCADE,
    section_name VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    page_numbers INTEGER[],
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Chats table
CREATE TABLE IF NOT EXISTS chats (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    paper_id UUID NOT NULL REFERENCES papers(id) ON DELETE CASCADE,
    question TEXT NOT NULL,
    answer TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_papers_user_id ON papers(user_id);
CREATE INDEX IF NOT EXISTS idx_sections_paper_id ON sections(paper_id);
CREATE INDEX IF NOT EXISTS idx_chats_user_id ON chats(user_id);
CREATE INDEX IF NOT EXISTS idx_chats_paper_id ON chats(paper_id);
CREATE INDEX IF NOT EXISTS idx_chats_created_at ON chats(created_at DESC);

-- Enable Row Level Security (RLS)
ALTER TABLE papers ENABLE ROW LEVEL SECURITY;
ALTER TABLE sections ENABLE ROW LEVEL SECURITY;
ALTER TABLE chats ENABLE ROW LEVEL SECURITY;

-- Papers RLS Policies
CREATE POLICY "Users can view their own papers" ON papers
    FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own papers" ON papers
    FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own papers" ON papers
    FOR UPDATE
    USING (auth.uid() = user_id);

CREATE POLICY "Users can delete their own papers" ON papers
    FOR DELETE
    USING (auth.uid() = user_id);

-- Sections RLS Policies
CREATE POLICY "Users can view sections of their papers" ON sections
    FOR SELECT
    USING (
        paper_id IN (
            SELECT id FROM papers WHERE user_id = auth.uid()
        )
    );

CREATE POLICY "Users can insert sections to their papers" ON sections
    FOR INSERT
    WITH CHECK (
        paper_id IN (
            SELECT id FROM papers WHERE user_id = auth.uid()
        )
    );

-- Chats RLS Policies
CREATE POLICY "Users can view their own chats" ON chats
    FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own chats" ON chats
    FOR INSERT
    WITH CHECK (auth.uid() = user_id);

-- Storage bucket policy for papers
INSERT INTO storage.buckets (id, name, public) 
VALUES ('papers', 'papers', false)
ON CONFLICT (id) DO NOTHING;
