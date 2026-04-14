# 🎓 PaperLens Backend - Complete Documentation

**PaperLens** is an AI-powered research paper analysis platform that enables users to upload academic papers and ask intelligent questions about them using Retrieval-Augmented Generation (RAG).

---

## 📋 Table of Contents

1. [🚀 Project Overview](#-project-overview)
2. [🧠 System Architecture](#-system-architecture)
3. [📂 Folder Structure](#-folder-structure)
4. [🔗 RAG Pipeline Deep Dive](#-rag-pipeline-deep-dive)
5. [⚙️ Setup Instructions](#️-setup-instructions)
6. [🔐 Environment Variables](#-environment-variables)
7. [🔌 API Endpoints](#-api-endpoints)
8. [🧩 Key Components Deep Dive](#-key-components-deep-dive)
9. [🛠 Technologies Used](#-technologies-used)
10. [🚀 How to Extend This Project](#-how-to-extend-this-project)
11. [🐞 Common Issues & Fixes](#-common-issues--fixes)
12. [📌 Best Practices](#-best-practices)

---

## 🚀 Project Overview

### What is PaperLens?

PaperLens is a backend API that enables:

- **PDF Upload & Parsing**: Upload research papers as PDFs
- **Semantic Search**: Find relevant sections using AI embeddings
- **Intelligent Q&A**: Ask questions about papers, get AI-generated answers with sources
- **Paper Comparison**: Compare multiple papers with structured analysis
- **Chat History**: Track conversations per paper
- **Multi-Provider LLM**: Uses Gemini (primary), Claude, or Groq with automatic fallback

### Problem It Solves

Reading long academic papers is time-consuming. Researchers spend hours searching for specific information or comparing multiple papers. PaperLens automates this by:

1. **Indexing papers instantly** using semantic embeddings
2. **Finding relevant sections** based on meaning (not just keyword matching)
3. **Generating contextual answers** using LLMs with retrieved paper sections
4. **Comparing papers** by analyzing similar sections across documents

### Real-World Use Case

A PhD student has 50 research papers to review:
- Without PaperLens: Hours of manual reading
- With PaperLens: Ask "How do these papers approach data preprocessing?" → Get answers from top 5 papers instantly

### Key Features

✨ **Smart PDF Processing**
- Automatic section extraction using heuristics
- Intelligent chapter/section detection
- PDF metadata extraction (title, author, creation date)

✨ **Semantic Search**
- Meaning-based search, not keyword matching
- Vector embeddings for accuracy
- Top-k retrieval with relevance scoring

✨ **Multi-Provider LLM**
- Gemini (Google) - Fast, free tier available
- Claude (Anthropic) - Most capable, slower
- Groq - Ultra-fast inference
- Automatic fallback if primary fails

✨ **Enterprise Security**
- JWT token authentication
- Supabase integration for user management
- Per-user data isolation

---

## 🧠 System Architecture

### High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                         FRONTEND (React)                             │
│                    (TypeScript, Vite)                               │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
                    HTTP/REST API
                    (JWT Auth Token)
                           │
┌──────────────────────────▼──────────────────────────────────────────┐
│                      FASTAPI BACKEND                                │
│          (Processing, Authentication, Routing)                      │
│                                                                      │
│  ┌─────────────────┐  ┌──────────────────┐  ┌────────────────┐   │
│  │   Auth Routes   │  │  Papers Routes   │  │  Chat Routes   │   │
│  │ (JWT Verify)    │  │ (Upload, List)   │  │ (Q&A, History) │   │
│  └────────┬────────┘  └────────┬─────────┘  └────────┬───────┘   │
│           │                    │                      │             │
│  ┌────────▼────────────────────▼──────────────────────▼───────┐   │
│  │            BUSINESS LOGIC SERVICES                         │   │
│  │                                                            │   │
│  │  ┌──────────────────┐      ┌─────────────────────────┐   │   │
│  │  │  PDF Parser      │      │  Embeddings Service     │   │   │
│  │  │ (PyPDF2)         │      │ (sentence-transformers) │   │   │
│  │  └──────────────────┘      └─────────────────────────┘   │   │
│  │                                                            │   │
│  │  ┌──────────────────┐      ┌─────────────────────────┐   │   │
│  │  │  RAG Pipeline    │      │  Retrieval Service      │   │   │
│  │  │ (Context + LLM)  │      │ (Semantic Search)       │   │   │
│  │  └──────────────────┘      └─────────────────────────┘   │   │
│  │                                                            │   │
│  │  ┌──────────────────┐      ┌─────────────────────────┐   │   │
│  │  │  LLM Provider    │      │  Embedding Storage      │   │   │
│  │  │  (Multi-fallback)│      │  (Chunking + DB)        │   │   │
│  │  └──────────────────┘      └─────────────────────────┘   │   │
│  │                                                            │   │
│  └────────────────────────────────────────────────────────────┘   │
└───────────┬────────────────────────┬───────────────────┬──────────┘
            │                        │                   │
            │                        │                   │
    ┌───────▼──────┐      ┌──────────▼────────┐  ┌──────▼─────────┐
    │   Supabase   │      │  PostgreSQL +     │  │ PDF Storage    │
    │  (Auth)      │      │  pgvector         │  │ (Bucket)       │
    │              │      │ (Vector DB)       │  │                │
    └──────────────┘      └───────────────────┘  └────────────────┘
```

### Request → Response Flow

#### 1. **Paper Upload Flow**
```
Client Upload PDF
    ↓
FastAPI: /papers/upload
    ↓
PDF Parsing (PyPDF2)
    ├─ Extract text
    └─ Extract metadata
    ↓
Section Detection (Regex heuristics)
    ├─ Find chapters/sections
    └─ Organize content
    ↓
Database Storage (Supabase)
    ├─ Save paper metadata
    └─ Save sections
    ↓
Embedding Generation (async-like)
    ├─ Chunk sections (500 chars, 100 char overlap)
    ├─ Generate embeddings (sentence-transformers)
    └─ Store in pgvector
    ↓
Response to Client: {paper_id, sections_count, status}
```

#### 2. **Question Answering (RAG) Flow**
```
Client asks question: "What is the main contribution?"
    ↓
FastAPI: POST /chat/
    ↓
JWT Authentication
    ├─ Verify token
    └─ Extract user_id
    ↓
Retrieval Service
    ├─ Embed question (sentence-transformers)
    ├─ Query pgvector in Supabase
    └─ Get top-5 relevant sections
    ↓
RAG Pipeline
    ├─ Build prompt with context
    ├─ Add sections + question
    └─ Format instructions
    ↓
LLM Provider Service (with fallback)
    ├─ Try Gemini
    ├─ If fails → Try Claude
    └─ If fails → Try Groq
    ↓
Response
    ├─ AI-generated answer
    ├─ Source paper
    ├─ Provider used
    └─ Status
    ↓
Database: Store in chats table
    ↓
Response to Client: {answer, sources, provider}
```

---

## 📂 Folder Structure

```
d:\PaperLens\BackEnd
│
├── 📄 README.md                          # Original quick-start guide
├── 📄 API_REFERENCE.md                   # API endpoint reference
├── 📄 requirements.txt                   # Python dependencies
├── 📄 .env.example                       # Environment variables template
├── 📄 run.sh                             # Unix/Linux startup script
├── 📄 run.bat                            # Windows startup script
│
├── 📁 app/                               # Main application package
│   │
│   ├── 📄 __init__.py                    # Package initialization
│   ├── 📄 main.py                        # FastAPI app initialization & CORS
│   │
│   ├── 📁 api/                           # API routing
│   │   ├── 📄 __init__.py
│   │   ├── 📄 api.py                     # Main router configuration
│   │   │
│   │   └── 📁 routes/                    # Endpoint definitions
│   │       ├── 📄 __init__.py
│   │       ├── 📄 health.py              # Health check endpoints (/api/v1/health)
│   │       ├── 📄 auth.py                # Authentication (/api/v1/auth/me, /logout, /stats)
│   │       ├── 📄 papers.py              # Paper management (/api/v1/papers/**)
│   │       └── 📄 chat.py                # Chat & Q&A (/api/v1/chat/**)
│   │
│   ├── 📁 core/                          # Core configuration
│   │   ├── 📄 __init__.py
│   │   └── 📄 config.py                  # Environment config, API keys, limits
│   │
│   ├── 📁 models/                        # Pydantic data models
│   │   ├── 📄 __init__.py
│   │   ├── 📄 user.py                    # User model
│   │   ├── 📄 paper.py                   # Paper & Section models
│   │   └── 📄 chat.py                    # Chat & Message models
│   │
│   ├── 📁 services/                      # Business logic services
│   │   ├── 📄 __init__.py
│   │   ├── 📄 supabase_client.py         # Supabase database client
│   │   ├── 📄 pdf_parser.py              # PDF text extraction & section detection
│   │   ├── 📄 embeddings_service.py      # Vector embedding generation
│   │   ├── 📄 embedding_storage_service.py  # Chunking + embedding storage
│   │   ├── 📄 retrieval_service.py       # Semantic search in vectors
│   │   ├── 📄 rag_pipeline.py            # RAG orchestration
│   │   ├── 📄 llm_provider_service.py    # Multi-provider LLM with fallback
│   │   ├── 📄 explainer.py               # (Optional) Explainer service
│   │   └── 📄 summarizer.py              # (Optional) Summarizer service
│   │
│   └── 📁 utils/                         # Utility functions
│       ├── 📄 __init__.py
│       └── 📄 security.py                # JWT verification & auth utils
│
├── 📁 migrations/                        # Database schema migrations
│   ├── 📄 add_pgvector_support.sql       # Vector extension + indexes
│   ├── 📄 add_embeddings_vector_support.sql
│   └── 📄 add_provider_sources_to_chats.sql
│
└── (Configuration files at root)
    └── (See requirements.txt, .env.example, etc.)
```

### File Descriptions

| File | Purpose |
|------|---------|
| `app/main.py` | FastAPI app setup, CORS configuration, root endpoints |
| `app/api/api.py` | Routes aggregator - includes all sub-routers |
| `app/api/routes/health.py` | Health check & service status |
| `app/api/routes/auth.py` | User info, logout, stats |
| `app/api/routes/papers.py` | Upload, list, get, delete papers |
| `app/api/routes/chat.py` | Ask questions, chat history |
| `app/core/config.py` | Environment variables & API configuration |
| `app/models/paper.py` | Pydantic models for papers & sections |
| `app/models/chat.py` | Pydantic models for chats & messages |
| `app/services/pdf_parser.py` | PDF text extraction, section detection |
| `app/services/embeddings_service.py` | Sentence-transformers embeddings |
| `app/services/embedding_storage_service.py` | Chunking strategy & pgvector storage |
| `app/services/retrieval_service.py` | Semantic similarity search |
| `app/services/rag_pipeline.py` | RAG orchestration (retrieve + generate) |
| `app/services/llm_provider_service.py` | Multi-provider LLM with fallback |
| `app/utils/security.py` | JWT token verification |

---

## 🔗 RAG Pipeline Deep Dive

### What is RAG?

**RAG (Retrieval-Augmented Generation)** = Retrieval + Prompting + LLM Generation

Instead of asking an LLM to answer based only on training data, RAG:
1. **Retrieves** relevant information from a document
2. **Constructs** a prompt with that information
3. **Asks the LLM** to answer based on the retrieved context

**Benefit**: Accurate answers tied to actual paper content, not hallucinations.

### Complete RAG Pipeline in PaperLens

#### Phase 1: **Data Ingestion** (PDF Upload)

```
PDF File (uploaded by user)
    ↓
extract_text_from_pdf() [pdf_parser.py]
    ├─ Uses: PyPDF2.PdfReader
    ├─ Extracts: Text + page count + metadata
    └─ Returns: {text, num_pages, metadata, word_count}
    ↓
_clean_pdf_text() [pdf_parser.py]
    ├─ Removes: Headers, footers, page numbers
    ├─ Removes: Email addresses, URLs
    └─ Normalizes: Multiple newlines
    ↓
extract_sections_from_text() [pdf_parser.py]
    ├─ Detects: Section headers using regex
    ├─ Patterns:
    │   ├─ Numbered: "1.", "1.1", "2. Chapter Name"
    │   ├─ Named: "Introduction", "Abstract", "Conclusion"
    │   ├─ ALL CAPS headers
    │   └─ Headers ending with ":"
    ├─ Groups content under each header
    └─ Returns: [{section_name, content, page_numbers}, ...]
    ↓
Database: Store in "papers" table
    └─ Fields: id, user_id, title, description, word_count, page_count, file_path
    ↓
Database: Store in "sections" table
    └─ Fields: id, paper_id, section_name, content, page_numbers, created_at
```

#### Phase 2: **Vectorization** (Embedding Generation)

```
Process: process_pdf_to_embeddings() [embedding_storage_service.py]

For each section in the paper:
    ↓
    chunk_section(content) [embedding_storage_service.py]
    ├─ Split by sentences
    ├─ Group sentences into chunks
    ├─ Chunk size: 500 characters
    ├─ Overlap: 100 characters (context preservation)
    │
    │   Why overlap? 
    │   - Prevents losing information at chunk boundaries
    │   - Example: If context spans chunks 2→3, overlap ensures it's captured
    │
    └─ Returns: [{content, chunk_index}, ...]
    ↓
    embed_texts(chunks) [embeddings_service.py]
    ├─ Model: all-MiniLM-L6-v2 (sentence-transformers)
    ├─ Dimensions: 384 (compact, fast)
    ├─ Time: ~1ms per chunk on modern GPU, ~50ms on CPU
    │
    │   Why this model?
    │   ✓ Fast: Lightweight, runs on CPU
    │   ✓ Accurate: 384 dims is sweet spot
    │   ✓ Free: No API calls needed
    │   ✓ Semantic: Understands academic language
    │
    └─ Returns: List[List[float]] (384-dimensional vectors)
    ↓
    Store in Supabase pgvector table
    ├─ Table: "sections"
    ├─ Column: "embedding" (vector(384))
    ├─ Index: IVFFlat (fast similarity search)
    │
    │   Why pgvector?
    │   ✓ Integrated with Supabase (no extra DB)
    │   ✓ Fast: IVFFlat index ~10-100ms for 1M vectors
    │   ✓ Accurate: Cosine similarity matching
    │   ✓ Scalable: Production-ready
    │
    └─ Total: N sections × M chunks per section = vectors stored

Example:
    Paper: "Attention Is All You Need" (60 pages, 15,000 words)
    ├─ Sections: 8 (intro, background, method, results, etc.)
    ├─ Chunks per section: ~30
    └─ Total vectors: 240 (8 × 30)
```

**Embedding Model Comparison:**

| Model | Dimension | Speed | Quality | Notes |
|-------|-----------|-------|---------|-------|
| all-MiniLM-L6-v2 | 384 | ⚡⚡⚡ | ⭐⭐⭐⭐ | **Used in PaperLens** |
| all-mpnet-base-v2 | 768 | ⚡⚡ | ⭐⭐⭐⭐⭐ | Best quality, slower |
| all-distilroberta-v1 | 768 | ⚡⚡ | ⭐⭐⭐⭐ | Multilingual |
| OpenAI text-embedding-3-small | 1536 | ⚡ | ⭐⭐⭐⭐⭐ | Best, expensive |

#### Phase 3: **Retrieval** (Find Relevant Sections)

```
User asks question: "What is the attention mechanism?"
    ↓
search_sections() [retrieval_service.py]
    │
    ├─ Step 1: Embed the question
    │   └─ embed_text(question) → 384-dimensional vector
    │
    ├─ Step 2: Query Supabase pgvector
    │   └─ Call RPC: sections_similarity_search
    │
    ├─ Step 3: Similarity Search (Cosine Distance)
    │   
    │   For each stored section vector:
    │       similarity = cosine_distance(question_vector, section_vector)
    │       range: 0.0 (different) → 1.0 (identical)
    │
    │   Return top_k=5 sections with highest similarity
    │
    └─ Step 4: Filter by threshold
        └─ Only return sections with similarity > 0.1 (low bar)

Example Result:
    [
        {
            section_name: "Attention Mechanism",
            content: "The attention mechanism...",
            similarity: 0.87,  # 87% match
            page_numbers: [2, 3]
        },
        {
            section_name: "Multi-Head Attention",
            content: "Multi-head attention extends...",
            similarity: 0.74,  # 74% match
            page_numbers: [3, 4]
        },
        ...
    ]
```

#### Phase 4: **Prompt Engineering** (Build Context)

```
generate_rag_response() [rag_pipeline.py]
    │
    ├─ Combine retrieved sections into context:
    │
    │   CONTEXT = """
    │   [Section 1: Attention Mechanism (Relevance: 87%)]
    │   The attention mechanism allows models to focus on relevant parts...
    │
    │   [Section 2: Multi-Head Attention (Relevance: 74%)]
    │   Multiple attention heads allow the model to jointly attend...
    │
    │   [Section 3: ...]
    │   ...
    │   """
    │
    │
    └─ Build full prompt:
    
    RAG_PROMPT = """
    You are an expert assistant analyzing a research paper.
    
    Paper Title: "Attention Is All You Need"
    
    Based on the following sections from the paper, answer the user's 
    question accurately and concisely.
    
    PAPER CONTEXT:
    [retrieved sections here]
    
    USER QUESTION: What is the attention mechanism?
    
    Please provide a clear, accurate answer based only on information 
    in the paper. If not covered, say so.
    """
```

#### Phase 5: **LLM Generation** (Multi-Provider Fallback)

```
generate_with_fallback() [llm_provider_service.py]
    │
    ├─ Priority Order: Gemini → Claude → Groq
    │
    ├─ Try Provider 1: Gemini (Google)
    │   ├─ Using: genai library
    │   ├─ Model: Available generative model (usually Gemini 1.5)
    │   ├─ Timeout: 30 seconds
    │   └─ If success: Return answer + "gemini" as provider
    │
    ├─ If Gemini fails → Try Provider 2: Claude (Anthropic)
    │   ├─ Using: anthropic.Anthropic library
    │   ├─ Model: claude-3-5-sonnet-20241022
    │   ├─ Max tokens: 2048
    │   ├─ Timeout: 30 seconds
    │   └─ If success: Return answer + "claude" as provider
    │
    ├─ If Claude fails → Try Provider 3: Groq
    │   ├─ Using: groq.Groq library
    │   ├─ Model: mixtral-8x7b-32768
    │   ├─ Temperature: 0.7
    │   ├─ Max tokens: 2048
    │   ├─ Timeout: 30 seconds
    │   └─ If success: Return answer + "groq" as provider
    │
    └─ If all fail: Return error message
    
Example Output:
    {
        "success": true,
        "answer": "The attention mechanism is a neural network component...",
        "provider_used": "gemini",  # or "claude" or "groq"
        "timestamp": "2024-04-13T10:30:00"
    }
```

**LLM Provider Comparison:**

| Provider | API | Speed | Quality | Cost | Fallback |
|----------|-----|-------|---------|------|----------|
| Gemini | google-generativeai | ⚡⚡⚡ | ⭐⭐⭐⭐ | Free tier | Primary |
| Claude | anthropic | ⚡⚡ | ⭐⭐⭐⭐⭐ | $$ | Secondary |
| Groq | groq | ⚡⚡⚡⚡ | ⭐⭐⭐⭐ | $ | Tertiary |

#### Phase 6: **Response & Storage**

```
Final RAG Response:
    {
        "success": true,
        "answer": "The attention mechanism is...",
        "chat_id": "uuid-...",
        "provider_used": "gemini",
        "sources": ["Attention Is All You Need"]
    }
    ↓
Store in Database (chats table):
    └─ Fields: id, user_id, paper_id, question, answer, 
               provider_used, sources, created_at
    ↓
Return to Client
```

### Why This RAG Design?

| Aspect | Benefit |
|--------|---------|
| **Chunking with overlap** | Prevents context loss at boundaries; improves retrieval quality |
| **sentence-transformers** | Fast, free, semantic understanding (not just keyword matching) |
| **pgvector indexing** | Fast retrieval even with millions of vectors |
| **Multi-provider fallback** | High availability; never down if one provider fails |
| **Top-k retrieval** | More context = better answers (typically 5 sections) |
| **Prompt engineering** | Clear instructions prevent hallucinations |
| **Source tracking** | Users know where info came from |

### How to Improve RAG Accuracy

1. **Better chunking**: Use semantic boundaries (end of paragraph) instead of fixed size
2. **Rerank**: Add a reranker model after retrieval (improves quality from top-5 to actual best-5)
3. **Query expansion**: Ask follow-up questions automatically to get broader context
4. **Fine-tuning embeddings**: Train on academic papers domain
5. **Keyword hybrid**: Combine semantic search with BM25 keyword search
6. **Cache**: Store frequently asked Qs & As
7. **Feedback loop**: Track which answers were helpful, retrain accordingly

---

## ⚙️ Setup Instructions

### Prerequisites

- **Python 3.9+** (tested on 3.10, 3.11, 3.12)
- **pip** (Python package manager)
- **Supabase Account** (free tier OK)
- **API Keys** (at least one of: Gemini, Claude, or Groq)
- **Git** (for cloning)

### Step 1: Clone Repository

```bash
git clone https://github.com/YOUR_REPO/PaperLens.git
cd PaperLens/BackEnd
```

### Step 2: Create Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**Expected output:**
```
Successfully installed fastapi-0.104.1 uvicorn-0.24.0 ...
```

### Step 4: Setup Environment Variables

**Copy example file:**
```bash
cp .env.example .env
```

**Edit `.env` file with your configuration:**
```ini
# Supabase Configuration (REQUIRED)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_KEY=your-service-key-here
SUPABASE_JWT_SECRET=your-jwt-secret-here

# AI Providers (At least ONE required)
GEMINI_API_KEY=your-gemini-api-key
CLAUDE_API_KEY=your-claude-api-key
GROQ_API_KEY=your-groq-api-key

# Optional
OPENAI_API_KEY=your-openai-key  # For future use
```

**Where to get API keys:**
- **Gemini**: https://ai.google.dev/
- **Claude**: https://console.anthropic.com/
- **Groq**: https://console.groq.com/
- **Supabase**: https://supabase.com/ (sign up, create project)

### Step 5: Setup Database Schema

**In Supabase SQL Editor, run migrations:**

1. Log into Supabase Dashboard
2. Go to SQL Editor
3. Run each file in `migrations/`:
   - `add_pgvector_support.sql`
   - `add_embeddings_vector_support.sql`
   - `add_provider_sources_to_chats.sql`

**Or create from scratch using:**

```sql
-- Enable pgvector for embeddings
CREATE EXTENSION IF NOT EXISTS vector;

-- Users table (managed by Supabase Auth)
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT auth.uid(),
    email TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Papers table
CREATE TABLE IF NOT EXISTS papers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    description TEXT,
    file_path TEXT,
    word_count INTEGER,
    page_count INTEGER,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Sections table with embeddings
CREATE TABLE IF NOT EXISTS sections (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    paper_id UUID NOT NULL REFERENCES papers(id) ON DELETE CASCADE,
    section_name TEXT NOT NULL,
    content TEXT NOT NULL,
    embedding vector(384),  -- 384 dimensions for all-MiniLM-L6-v2
    chunk_index INTEGER DEFAULT 0,
    page_numbers INTEGER[] DEFAULT ARRAY[]::INT[],
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Chats table
CREATE TABLE IF NOT EXISTS chats (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    paper_id UUID NOT NULL REFERENCES papers(id) ON DELETE CASCADE,
    question TEXT NOT NULL,
    answer TEXT,
    provider_used TEXT,  -- "gemini", "claude", "groq"
    sources TEXT[] DEFAULT ARRAY[]::TEXT[],
    created_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for faster queries
CREATE INDEX idx_papers_user_id ON papers(user_id);
CREATE INDEX idx_sections_paper_id ON sections(paper_id);
CREATE INDEX idx_chats_user_id ON chats(user_id);
CREATE INDEX idx_chats_paper_id ON chats(paper_id);

-- Vector similarity search index
CREATE INDEX idx_sections_embedding ON sections USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

-- RPC Function for similarity search
CREATE OR REPLACE FUNCTION sections_similarity_search(
    query_embedding vector(384),
    paper_id_param UUID,
    top_k INT DEFAULT 5,
    similarity_threshold FLOAT DEFAULT 0.1
)
RETURNS TABLE (
    id UUID,
    paper_id UUID,
    section_name TEXT,
    content TEXT,
    page_numbers INT[],
    similarity FLOAT
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        s.id,
        s.paper_id,
        s.section_name,
        s.content,
        s.page_numbers,
        (1 - (s.embedding <=> query_embedding))::FLOAT AS similarity
    FROM sections s
    WHERE s.paper_id = paper_id_param
    ORDER BY s.embedding <=> query_embedding
    LIMIT top_k;
END;
$$ LANGUAGE plpgsql;
```

### Step 6: Run the Server

**Option A: Run with auto-reload (Development)**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Option B: Use provided scripts**
```bash
# Windows
run.bat

# macOS/Linux
./run.sh
```

**Expected output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started server process [1234]
INFO:     Application startup complete
```

### Step 7: Verify Installation

**1. Check health endpoint:**
```bash
curl http://localhost:8000/api/v1/health/
```

**Should return:**
```json
{
  "status": "ok",
  "service": "PaperLens API",
  "version": "1.0.0"
}
```

**2. Visit API documentation:**
- Interactive Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

**3. Test with sample request:**
```bash
curl -X GET "http://localhost:8000/api/v1/" \
  -H "accept: application/json"
```

### Troubleshooting Setup

**Issue: `ModuleNotFoundError: No module named 'fastapi'`**
```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

**Issue: `ConnectionError: SUPABASE_URL not set`**
```bash
# Solution: Create .env file
cp .env.example .env
# Edit .env with your Supabase credentials
```

**Issue: `pgvector not available in Supabase`**
```bash
# Solution: Enable in Supabase dashboard
# 1. Go to Extensions in SQL Editor
# 2. Search "vector"
# 3. Enable pgvector extension
```

---

## 🔐 Environment Variables

### Complete Reference

```ini
# ============================================
# SUPABASE CONFIGURATION (REQUIRED)
# ============================================

# Supabase project URL
# Get from: Dashboard → Settings → API
SUPABASE_URL=https://your-project.supabase.co

# Supabase service role key (NOT anon key!)
# Get from: Dashboard → Settings → API → Service Role Key
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# JWT secret for token verification
# Get from: Dashboard → Settings → API → JWT Secret
SUPABASE_JWT_SECRET=your-super-secret-jwt-key

# ============================================
# LLM PROVIDER KEYS (At least ONE required)
# ============================================

# Google Gemini API Key
# Get from: https://ai.google.dev/
# Free tier: 60 requests/minute
GEMINI_API_KEY=AIzaSyD...

# Anthropic Claude API Key
# Get from: https://console.anthropic.com/
# Pricing: ~$0.002 per 1K input tokens
CLAUDE_API_KEY=sk-ant-...

# Groq API Key (faster inference)
# Get from: https://console.groq.com/
# Pricing: Cheap/free tier available
GROQ_API_KEY=gsk_...

# ============================================
# OPTIONAL
# ============================================

# OpenAI API Key (for future embedding models)
OPENAI_API_KEY=sk-...

# Database URL (alternative to Supabase)
DATABASE_URL=postgresql://user:password@localhost/paperlens
```

### Why Each Variable?

| Variable | Purpose | Impact |
|----------|---------|--------|
| SUPABASE_URL | Database & storage location | **Critical** - API won't start without it |
| SUPABASE_SERVICE_KEY | Authenticate with database | **Critical** - All queries fail without it |
| SUPABASE_JWT_SECRET | Verify user tokens | **Critical** - Auth will fail without it |
| GEMINI_API_KEY | Primary LLM provider | **Recommended** - Free tier, good quality |
| CLAUDE_API_KEY | Fallback LLM provider | **Recommended** - Best quality when available |
| GROQ_API_KEY | Fast LLM provider | **Recommended** - Ultra-fast inference |

### How to Find API Keys

**Supabase:**
1. Log in to https://supabase.com/
2. Select your project
3. Go to ⚙️ Settings → API
4. Copy the URL, Service Role key, and JWT Secret

**Gemini:**
1. Go to https://ai.google.dev/
2. Click "Get API Key" → "Create API Key in Google Cloud"
3. Copy the key

**Claude:**
1. Go to https://console.anthropic.com/
2. Create API key in Account settings
3. Copy the key

**Groq:**
1. Go to https://console.groq.com/
2. Create new API key
3. Copy the key

---

## 🔌 API Endpoints

### Base URL
```
http://localhost:8000/api/v1
```

### Authentication
All endpoints (except health) require JWT token:
```
Authorization: Bearer {jwt_token}
```

Get JWT token from:
- Supabase Auth (frontend login)
- Or manually create one with HS256

---

### 1. Health Endpoints

#### Check Service Health
```http
GET /health/
```

**Response (200):**
```json
{
  "status": "ok",
  "service": "PaperLens API",
  "version": "1.0.0"
}
```

#### Check Readiness
```http
GET /health/ready
```

**Response (200):**
```json
{
  "ready": true,
  "service": "PaperLens API"
}
```

---

### 2. Authentication Endpoints

#### Get Current User
```http
GET /auth/me
Authorization: Bearer {token}
```

**Response (200):**
```json
{
  "id": "user-uuid",
  "email": "user@example.com",
  "created_at": "2024-01-15T10:30:00Z"
}
```

**Error (401):**
```json
{
  "detail": "Invalid token"
}
```

#### Get User Statistics
```http
GET /auth/stats
Authorization: Bearer {token}
```

**Response (200):**
```json
{
  "user_id": "user-uuid",
  "papers_count": 15,
  "chats_count": 127,
  "email": "user@example.com"
}
```

#### Logout
```http
POST /auth/logout
Authorization: Bearer {token}
```

**Response (200):**
```json
{
  "success": true,
  "message": "Logged out successfully. Clear token from localStorage on frontend."
}
```

---

### 3. Paper Endpoints

#### List All Papers
```http
GET /papers/
Authorization: Bearer {token}
```

**Response (200):**
```json
[
  {
    "id": "paper-uuid-1",
    "title": "Attention Is All You Need",
    "description": "A transformer architecture for NLP",
    "word_count": 12000,
    "page_count": 15,
    "created_at": "2024-01-15T10:30:00Z",
    "sections_count": 8
  },
  {
    "id": "paper-uuid-2",
    "title": "BERT: Pre-training of Deep Bidirectional...",
    "description": null,
    "word_count": 15000,
    "page_count": 13,
    "created_at": "2024-01-16T14:20:00Z",
    "sections_count": 6
  }
]
```

#### Upload Paper
```http
POST /papers/upload
Content-Type: multipart/form-data
Authorization: Bearer {token}

Parameters:
  file: <PDF file>
  title: "Optional custom title"
```

**Response (200):**
```json
{
  "success": true,
  "paper_id": "paper-uuid-new",
  "title": "Attention Is All You Need",
  "sections_count": 8,
  "word_count": 12000,
  "message": "Paper 'Attention Is All You Need' uploaded successfully with 8 sections. Embeddings: 240 chunks processed (success)"
}
```

**Error (400):**
```json
{
  "detail": "Only PDF files are allowed"
}
```

**Error (413):**
```json
{
  "detail": "File size exceeds maximum limit of 50MB. Your file is 55.32MB"
}
```

#### Get Paper with Sections
```http
GET /papers/{paper_id}
Authorization: Bearer {token}
```

**Response (200):**
```json
{
  "id": "paper-uuid",
  "user_id": "user-uuid",
  "title": "Attention Is All You Need",
  "description": "A transformer architecture...",
  "file_path": "papers/user-uuid/paper-uuid/document.pdf",
  "word_count": 12000,
  "page_count": 15,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z",
  "sections": [
    {
      "id": "section-uuid-1",
      "paper_id": "paper-uuid",
      "section_name": "Abstract",
      "content": "The dominant sequence transduction models...",
      "page_numbers": [1],
      "created_at": "2024-01-15T10:30:00Z"
    },
    {
      "id": "section-uuid-2",
      "paper_id": "paper-uuid",
      "section_name": "Introduction",
      "content": "Recurrent neural networks have been...",
      "page_numbers": [1, 2],
      "created_at": "2024-01-15T10:30:00Z"
    },
    {
      "id": "section-uuid-3",
      "paper_id": "paper-uuid",
      "section_name": "Attention Mechanism",
      "content": "An attention mechanism allows...",
      "page_numbers": [3, 4, 5],
      "created_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

**Error (404):**
```json
{
  "detail": "Paper not found"
}
```

#### Delete Paper
```http
DELETE /papers/{paper_id}
Authorization: Bearer {token}
```

**Response (200):**
```json
{
  "success": true,
  "message": "Paper deleted successfully"
}
```

#### Compare Papers
```http
POST /papers/{paper_id}/compare
Authorization: Bearer {token}
Content-Type: application/json

Body:
{
  "paper_ids": ["paper-uuid-2", "paper-uuid-3"],
  "question": "How do these papers approach data preprocessing?"
}
```

**Response (200):**
```json
{
  "success": true,
  "comparison": "Paper 1 uses batch normalization while Paper 2 uses layer normalization...",
  "papers_compared": 3,
  "provider_used": "gemini"
}
```

---

### 4. Chat/Q&A Endpoints

#### Ask Question About Paper
```http
POST /chat/
Authorization: Bearer {token}
Content-Type: application/json

Body:
{
  "paper_id": "paper-uuid",
  "question": "What is the main contribution of the paper?"
}
```

**Response (200):**
```json
{
  "success": true,
  "answer": "The main contribution of this paper is the introduction of the Transformer architecture, which replaces recurrent neural networks with pure attention mechanisms for sequence-to-sequence tasks. This approach achieves state-of-the-art results on machine translation while being significantly faster to train.",
  "chat_id": "chat-uuid",
  "provider_used": "gemini",
  "sources": ["Attention Is All You Need"]
}
```

**Error (404):**
```json
{
  "detail": "Paper not found"
}
```

**Error (500):**
```json
{
  "detail": "RAG Pipeline Error: All LLM providers failed"
}
```

#### Get Chat History
```http
GET /chat/history/{paper_id}
Authorization: Bearer {token}
```

**Response (200):**
```json
[
  {
    "id": "chat-uuid-1",
    "question": "What is the main contribution?",
    "answer": "The paper introduces the Transformer architecture...",
    "paper_id": "paper-uuid",
    "provider_used": "gemini",
    "sources": ["Attention Is All You Need"],
    "created_at": "2024-01-15T10:35:00Z"
  },
  {
    "id": "chat-uuid-2",
    "question": "How does attention work?",
    "answer": "Attention is a mechanism that allows the model to focus...",
    "paper_id": "paper-uuid",
    "provider_used": "claude",
    "sources": ["Attention Is All You Need"],
    "created_at": "2024-01-15T10:40:00Z"
  }
]
```

---

## 🧩 Key Components Deep Dive

### 1. **PDF Parser** (`app/services/pdf_parser.py`)

**What it does:**
- Extracts text from PDF files
- Detects sections automatically
- Cleans text (removes headers, footers, artifacts)

**Key functions:**

```python
extract_text_from_pdf(pdf_bytes: bytes) -> Dict
    # Input: Raw PDF file bytes
    # Output: {text, num_pages, metadata, word_count}
    # Uses: PyPDF2.PdfReader

extract_sections_from_text(text: str) -> List[Dict]
    # Input: Raw PDF text
    # Output: [{section_name, content, page_numbers}, ...]
    # Detects sections using regex patterns:
    #   - Numbered: "1.", "1.1"
    #   - Named: "Introduction", "Abstract"
    #   - ALL CAPS headers
    #   - Headers with colons

_clean_pdf_text(text: str) -> str
    # Input: Raw text with artifacts
    # Output: Cleaned text
    # Removes: headers, footers, page numbers, URLs
```

**Limitations & Improvements:**

| Limitation | Impact | Fix |
|-----------|--------|-----|
| Section detection is regex-based | May miss sections without clear headers | Use ML-based segmentation |
| No column detection | Works poorly on multi-column PDFs | Use PDF visual analysis |
| No table extraction | Tables become unreadable text | Add tabula or camelot |
| No figure/image support | Can't process visual data | Add OCR with Tesseract |

---

### 2. **Embeddings Service** (`app/services/embeddings_service.py`)

**What it does:**
- Generates vector embeddings using sentence-transformers
- Enables semantic similarity search

**Key functions:**

```python
embed_text(text: str) -> List[float]
    # Input: Single text string
    # Output: 384-dimensional embedding vector
    # Model: all-MiniLM-L6-v2
    # Time: ~1ms on GPU, ~50ms on CPU

embed_texts(texts: List[str]) -> List[List[float]]
    # Input: Multiple texts (batch)
    # Output: List of embeddings
    # Time: Batch is ~2x faster than individual
    # Memory: More efficient

get_embedding_dimension() -> int
    # Output: 384
    # Change this if using different model
```

**Model Details:**

- **Name:** all-MiniLM-L6-v2
- **Dimensions:** 384
- **Speed:** 35 docs/sec on CPU
- **Memory:** ~100MB
- **Best for:** Fast, accurate semantic search

**To use different model:**

```python
# In embeddings_service.py, change:
MODEL_NAME = "all-mpnet-base-v2"  # 768 dims, slower, better quality
# or
MODEL_NAME = "text2vec-openai"  # Requires OpenAI API
```

---

### 3. **Embedding Storage Service** (`app/services/embedding_storage_service.py`)

**What it does:**
- Chunks documents strategically
- Generates embeddings for chunks
- Stores in Supabase pgvector

**Key functions:**

```python
chunk_section(content: str, chunk_size: int = 500, overlap: int = 100)
    # Input: Section text
    # Output: [{content, chunk_index}, ...]
    # Strategy: Split by sentences, group by token count
    # Why overlap? Prevents losing context at chunk boundaries

process_pdf_to_embeddings(pdf_bytes, paper_id, paper_title) -> Dict
    # Complete pipeline: extract → chunk → embed → store
    # Output: {status, sections_processed, total_chunks}
```

**Chunking Strategy:**

```
Original text:
"Sentence 1. Sentence 2. Sentence 3. Sentence 4. Sentence 5."

With chunk_size=500 chars, overlap=100 chars:

Chunk 1: [Sentence 1. Sentence 2. Sentence 3.]
Chunk 2: [Sentence 2. Sentence 3. Sentence 4.]  ← Overlap with chunk 1
Chunk 3: [Sentence 4. Sentence 5.]

Benefit: If query spans chunks 1→2, overlap ensures full context
```

---

### 4. **Retrieval Service** (`app/services/retrieval_service.py`)

**What it does:**
- Searches for similar sections using embeddings
- Returns relevant sections with similarity scores

**Key functions:**

```python
search_sections(query: str, paper_id: str, top_k: int = 5)
    # Input: User's question, paper ID
    # Output: [{section_name, content, similarity}, ...]
    # Uses: Supabase pgvector RPC with cosine similarity

search_sections_across_papers(query: str, top_k: int = 10)
    # Input: User's question
    # Output: Sections from ALL papers (user's)
    # Use case: Find related work across papers

get_paper_context(query: str, paper_id: str, top_k: int = 5) -> str
    # Input: User's question, paper
    # Output: Formatted context string for LLM
    # Format: "[Section 1: Name (Relevance: 85%)]\nContent..."
```

**Supabase RPC Implementation:**

```sql
CREATE OR REPLACE FUNCTION sections_similarity_search(
    query_embedding vector(384),
    paper_id_param UUID,
    top_k INT DEFAULT 5,
    similarity_threshold FLOAT DEFAULT 0.1
)
RETURNS TABLE (
    id UUID,
    section_name TEXT,
    content TEXT,
    similarity FLOAT
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        s.id,
        s.section_name,
        s.content,
        (1 - (s.embedding <=> query_embedding))::FLOAT
    FROM sections s
    WHERE s.paper_id = paper_id_param
        AND (1 - (s.embedding <=> query_embedding)) > similarity_threshold
    ORDER BY s.embedding <=> query_embedding
    LIMIT top_k;
END;
$$ LANGUAGE plpgsql;
```

**Similarity Scoring:**

```
Cosine similarity: -1 (opposite) to 1 (identical)
PaperLens converts to: 0 (opposite) to 1 (identical)
Formula: similarity = 1 - distance

Example:
  Question: "What is attention?"
  Section A (query vector vs section vector): distance=0.2 → similarity=0.80 (80%)
  Section B: distance=0.5 → similarity=0.50 (50%)
  
  Return: [Section A, Section B, ...] (sorted by similarity desc)
```

---

### 5. **RAG Pipeline** (`app/services/rag_pipeline.py`)

**What it does:**
- Orchestrates retrieval + generation
- Handles multi-paper comparison
- Error handling & logging

**Key functions:**

```python
generate_rag_response(question, paper_id, paper_title, top_k=5)
    # Complete RAG: retrieve → prompt → generate
    # Output: {answer, sources, provider, status}

compare_papers_rag(question, paper_ids, paper_titles, top_k=3)
    # Compare multiple papers
    # Retrieves from each, builds comparison prompt
    # Output: Structured comparison answer
```

**Error Handling:**

```python
try:
    # Retrieve sections
    context = get_paper_context(question, paper_id, top_k)
    
    if not context:
        # No relevant sections found
        return error_response("No relevant sections found")
    
    # Build prompt
    rag_prompt = build_prompt(context, question, paper_title)
    
    # Call LLM with fallback
    result = generate_with_fallback(rag_prompt)
    
    if result["success"]:
        # Success
        store_in_database(result)
        return success_response(result)
    else:
        # LLM failed
        return error_response("LLM failed")
        
except Exception as e:
    # Unexpected error
    return error_response(str(e))
```

---

### 6. **LLM Provider Service** (`app/services/llm_provider_service.py`)

**What it does:**
- Manages multiple LLM providers
- Handles automatic fallback
- Configures models optimally

**Key functions:**

```python
generate_with_fallback(prompt, provider_order: list = None) -> Dict
    # Try providers in order: Gemini → Claude → Groq
    # Output: {success, answer, provider_used, timestamp}
    # Each provider has timeout & error handling

_call_gemini(prompt) -> Optional[str]
    # API: genai.GenerativeModel(model_name)
    # Auto-discovers available model
    # Timeout: 30 seconds

_call_claude(prompt) -> Optional[str]
    # API: anthropic.Anthropic()
    # Model: claude-3-5-sonnet-20241022
    # Max tokens: 2048
    # Timeout: 30 seconds

_call_groq(prompt) -> Optional[str]
    # API: groq.Groq()
    # Model: mixtral-8x7b-32768
    # Fastest inference time
    # Timeout: 30 seconds
```

**Fallback Logic:**

```
User asks question
    ↓
Try Gemini (free, usually works)
    ├─ Success? Return answer
    └─ Fail? Continue
    ↓
Try Claude (higher quality)
    ├─ Success? Return answer
    └─ Fail? Continue
    ↓
Try Groq (fastest)
    ├─ Success? Return answer
    └─ Fail? All failed, return error
```

---

### 7. **Security** (`app/utils/security.py`)

**What it does:**
- Verifies JWT tokens
- Extracts user information from tokens
- Authentication for all protected routes

**Key functions:**

```python
verify_jwt_token(token: str) -> dict
    # Decodes JWT (trusts Supabase signature)
    # Returns: {sub/user_id, email, ...}

get_current_user(credentials) -> dict
    # Extract from FastAPI Depends(security)
    # Returns: {user_id, email}
    # Handles multiple token formats
```

**Token Formats Supported:**

```json
{
  "sub": "user-uuid",           // Supabase standard
  "email": "user@example.com"
}

// OR

{
  "user_id": "user-uuid",
  "userId": "user-uuid",
  "uid": "user-uuid",
  "email": "user@example.com"
}
```

---

## 🛠 Technologies Used

### Core Framework
- **FastAPI** (0.104.1): Modern Python web framework, automatic API docs
- **Uvicorn** (0.24.0): ASGI server, fast async support
- **Pydantic** (2.7.0): Data validation, type hints

### Database & Storage
- **Supabase** (2.0.3): PostgreSQL + pgvector + Auth + Storage
- **PostgreSQL + pgvector**: Vector database for embeddings
- **Python-multipart** (0.0.6): File upload handling

### PDF Processing
- **PyPDF2** (3.0.1): PDF text extraction
- **PyJWT** (2.12.1): JWT token handling

### AI & Embeddings
- **sentence-transformers** (3.0.0+): Local embeddings (all-MiniLM-L6-v2)
- **torch** (2.2.2): Deep learning dependency
- **numpy** (1.26.4): Numerical computing

### LLM Providers
- **google-generativeai** (0.3.0): Google Gemini API
- **anthropic** (0.7.1): Anthropic Claude API
- **groq** (0.4.1): Groq fast inference API

### Utilities
- **python-dotenv** (1.0.0): Environment variable loading
- **requests** (2.31.0): HTTP requests library
- **huggingface-hub** (0.19.0): Model downloading

### Version Requirements
```
Python: 3.9+ (tested on 3.10, 3.11, 3.12)
pip: Latest
```

---

## 🚀 How to Extend This Project

### 1. Add New Data Sources

**Goal:** Support documents beyond PDFs (Word, PowerPoint, web URLs)

**Steps:**

```python
# 1. Create new parser in app/services/
# app/services/word_parser.py

from docx import Document

def extract_text_from_docx(docx_bytes):
    doc = Document(io.BytesIO(docx_bytes))
    text = "\n".join([p.text for p in doc.paragraphs])
    return {
        "text": text,
        "num_pages": len(doc.paragraphs),
        "metadata": {"title": doc.core_properties.title}
    }

# 2. Update papers.py route

@router.post("/upload")
async def upload_paper(file: UploadFile):
    if file.filename.endswith(".pdf"):
        data = parse_pdf(...)
    elif file.filename.endswith(".docx"):
        data = extract_text_from_docx(...)
    # ... rest of logic
```

---

### 2. Improve RAG Accuracy

**Goal:** Get better answers from papers

**Option A: Add Re-ranking**

```python
# Install: pip install sentence-transformers[sentence-transformers]

from sentence_transformers import CrossEncoder

def rerank_sections(question, sections, top_k=5):
    """Re-rank sections using cross-encoder for better accuracy"""
    reranker = CrossEncoder('cross-encoder/qnli-distilroberta-base')
    
    # Score each section
    scores = reranker.predict(
        [[question, s['content']] for s in sections]
    )
    
    # Sort by score
    ranked = sorted(zip(sections, scores), key=lambda x: x[1], reverse=True)
    return [s for s, score in ranked[:top_k]]
```

**Option B: Hybrid Search (Keyword + Semantic)**

```python
# Combine BM25 (keyword) + vector search

def hybrid_search(query, paper_id, top_k=5):
    """Combination of keyword (BM25) and semantic search"""
    
    # 1. Keyword search (BM25)
    bm25_results = bm25_search(query, paper_id)
    
    # 2. Semantic search (vectors)
    semantic_results = search_sections(query, paper_id)
    
    # 3. Combine & deduplicate
    combined = {}
    for r in bm25_results + semantic_results:
        section_id = r['id']
        if section_id not in combined:
            combined[section_id] = {**r, 'score': 0}
        combined[section_id]['score'] += r.get('rank', 0)
    
    # 4. Sort by combined score
    return sorted(combined.values(), key=lambda x: x['score'])
```

---

### 3. Swap LLM Providers

**Goal:** Use different models (e.g., local LM, OpenAI)

**Option A: Add OpenAI**

```python
# In llm_provider_service.py

def _call_openai(prompt: str) -> Optional[str]:
    """Call OpenAI API"""
    try:
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2048
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"OpenAI error: {str(e)}")
        return None

# Update provider order
def generate_with_fallback(prompt, provider_order=None):
    if provider_order is None:
        provider_order = ["openai", "gemini", "claude", "groq"]
    # ... rest
```

**Option B: Use Local LM (Ollama)**

```python
# Install: https://ollama.ai
# Run: ollama run mistral

import requests

def _call_local_llm(prompt: str) -> Optional[str]:
    """Call local LM via Ollama"""
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "mistral", "prompt": prompt}
        )
        # Ollama returns streaming JSON
        result = ""
        for line in response.iter_lines():
            if line:
                result += json.loads(line).get("response", "")
        return result
    except Exception as e:
        print(f"Local LM error: {str(e)}")
        return None
```

---

### 4. Scale the System

**Goal:** Handle millions of users & papers

**Steps:**

1. **Add caching:**
   ```python
   from redis import Redis
   
   redis = Redis.from_url(os.getenv("REDIS_URL"))
   
   def get_cached_answer(question, paper_id):
       cache_key = f"rag:{paper_id}:{hash(question)}"
       return redis.get(cache_key)
   
   def cache_answer(question, paper_id, answer, ttl=3600):
       cache_key = f"rag:{paper_id}:{hash(question)}"
       redis.setex(cache_key, ttl, answer)
   ```

2. **Add async processing:**
   ```python
   # Use Celery for background jobs
   from celery import Celery
   
   celery = Celery("paperlens")
   
   @celery.task
   def process_embeddings_async(pdf_bytes, paper_id):
       # Long-running task
       return process_pdf_to_embeddings(pdf_bytes, paper_id)
   ```

3. **Add database indexes:**
   ```sql
   CREATE INDEX idx_sections_paper_embedding ON sections(paper_id) 
       WHERE embedding IS NOT NULL;
   CREATE INDEX idx_chats_created_at ON chats(created_at DESC);
   CREATE INDEX idx_users_email ON users(email);
   ```

---

## 🐞 Common Issues & Fixes

### Issue 1: "ModuleNotFoundError: No module named 'sentence_transformers'"

**Cause:** Package not installed

**Fix:**
```bash
pip install sentence-transformers
# or reinstall all
pip install -r requirements.txt
```

---

### Issue 2: "Supabase credentials not found"

**Cause:** Missing .env file or variables

**Fix:**
```bash
cp .env.example .env
# Edit .env with your Supabase URL and keys
cat .env  # Verify it looks correct
```

---

### Issue 3: "All LLM providers failed"

**Cause:** API keys incorrect or rate limited

**Fix:**
```bash
# 1. Verify API keys in .env
# 2. Check if you're rate limited
# 3. Try another provider

# Test individually:
export GEMINI_API_KEY="your-key"
python -c "import google.generativeai as genai; genai.configure(api_key='your-key')"

# If error, key is invalid
```

---

### Issue 4: "pgvector extension not available"

**Cause:** Extension not enabled in Supabase

**Fix:**
```bash
# 1. Go to Supabase Dashboard
# 2. SQL Editor
# 3. Run:
CREATE EXTENSION IF NOT EXISTS vector;

# 4. Verify it's enabled:
SELECT extname FROM pg_extension WHERE extname = 'vector';
```

---

### Issue 5: "PDF parsing returns empty text"

**Cause:** PDF is scanned/image-based, not text-based

**Fix:**
```bash
# Install OCR (Tesseract)
# Windows: https://github.com/UB-Mannheim/tesseract/wiki
# macOS: brew install tesseract
# Linux: sudo apt-get install tesseract-ocr

# Then use:
from pytesseract import image_to_string
from pdf2image import convert_from_bytes

def extract_text_from_scanned_pdf(pdf_bytes):
    images = convert_from_bytes(pdf_bytes)
    text = ""
    for img in images:
        text += image_to_string(img) + "\n"
    return text
```

---

### Issue 6: "Slow vector search (>5 seconds)"

**Cause:** Index not created or data too large

**Fix:**
```sql
-- 1. Create index if missing
CREATE INDEX idx_sections_embedding ON sections 
USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

-- 2. Analyze query performance
EXPLAIN ANALYZE
SELECT id, embedding <=> query_vector
FROM sections
WHERE paper_id = 'paper-uuid'
ORDER BY embedding <=> query_vector
LIMIT 5;

-- 3. Adjust index parameters if needed
DROP INDEX idx_sections_embedding;
CREATE INDEX idx_sections_embedding ON sections 
USING ivfflat (embedding vector_cosine_ops) WITH (lists = 200);  -- More lists = slower but more accurate
```

---

### Issue 7: "Memory error during embedding generation"

**Cause:** Batch size too large

**Fix:**
```python
# In embeddings_service.py

def embed_texts(texts, batch_size=100):
    """Process in batches to avoid memory error"""
    model = _get_model()
    embeddings = []
    
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i+batch_size]
        batch_embeddings = model.encode(batch, convert_to_tensor=False)
        embeddings.extend(batch_embeddings.tolist())
    
    return embeddings
```

---

## 📌 Best Practices

### Code Quality

✅ **Use type hints:**
```python
def search_sections(
    query: str,
    paper_id: str,
    top_k: int = 5
) -> List[Dict]:
    pass
```

✅ **Validate input:**
```python
if not file.filename.lower().endswith('.pdf'):
    raise HTTPException(status_code=400, detail="Only PDFs allowed")
```

✅ **Error handling:**
```python
try:
    # Business logic
except SpecificError:
    # Handle specific case
except Exception as e:
    # Log and return error
    print(f"Unexpected error: {e}")
    raise
```

---

### Security

✅ **Always verify JWT tokens:**
```python
@router.get("/protected")
async def protected_route(credentials = Depends(security)):
    user = get_current_user(credentials)  # Verify token
    # Use user data
```

✅ **Never log sensitive data:**
```python
# ❌ BAD
print(f"API Key: {os.getenv('OPENAI_API_KEY')}")

# ✅ GOOD
print("Calling OpenAI API...")
```

✅ **Use environment variables for secrets:**
```python
# ❌ BAD
supabase_key = "sk-proj-..."

# ✅ GOOD
supabase_key = os.getenv("SUPABASE_SERVICE_KEY")
```

---

### Performance

✅ **Batch vector operations:**
```python
# ❌ Slow
embeddings = []
for text in texts:
    embeddings.append(embed_text(text))

# ✅ Fast
embeddings = embed_texts(texts)  # Batch processing
```

✅ **Use database indexes:**
```sql
-- Query papers by user ID frequently
CREATE INDEX idx_papers_user_id ON papers(user_id);

-- Search vectors
CREATE INDEX idx_sections_embedding ON sections 
USING ivfflat (embedding vector_cosine_ops);
```

✅ **Cache frequently accessed data:**
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def get_embedding_model():
    # Model only loaded once
    return SentenceTransformer("all-MiniLM-L6-v2")
```

---

### Documentation

✅ **Write docstrings:**
```python
def generate_rag_response(
    question: str,
    paper_id: str,
    paper_title: str,
    top_k: int = 5
) -> Dict[str, str]:
    """
    Generate answer using RAG pipeline with multi-provider LLM
    
    Args:
        question: User's question
        paper_id: Paper to search in
        paper_title: Title of the paper (for context in prompt)
        top_k: Number of sections to retrieve (default: 5)
    
    Returns:
        Dict with keys:
        - answer: AI-generated response
        - sources: List of source papers
        - provider: LLM provider used ("gemini", "claude", "groq")
        - status: "success" or "failed"
    
    Raises:
        Exception: If retrieval or generation fails
    
    Example:
        >>> result = generate_rag_response(
        ...     "What is attention?",
        ...     "paper-uuid",
        ...     "Attention Is All You Need",
        ...     top_k=5
        ... )
        >>> print(result["answer"])
    """
    pass
```

---

### Testing

✅ **Write unit tests:**
```python
# tests/test_pdf_parser.py

import pytest
from app.services.pdf_parser import is_section_header

def test_section_detection():
    assert is_section_header("1. Introduction") == True
    assert is_section_header("1.1 Background") == True
    assert is_section_header("ABSTRACT") == True
    assert is_section_header("This is regular text") == False
```

✅ **Test API endpoints:**
```python
# tests/test_api.py

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/api/v1/health/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_chat_requires_auth():
    response = client.post("/api/v1/chat/", json={})
    assert response.status_code == 403  # Forbidden
```

---

## 📞 Support & Contribution

### Getting Help

- **Issues:** GitHub Issues (if public repo)
- **Documentation:** This README
- **API Docs:** http://localhost:8000/docs
- **Supabase Docs:** https://supabase.com/docs

### Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Make changes
4. Add tests
5. Commit: `git commit -m 'Add amazing feature'`
6. Push: `git push origin feature/amazing-feature`
7. Open Pull Request

### Code Style

- Use Black for formatting: `black app/`
- Use isort for imports: `isort app/`
- Type hints required (use mypy): `mypy app/`

---

## 📄 License

This project is licensed under the MIT License. See LICENSE file for details.

---

## 🎉 Summary

**PaperLens Backend** is a production-ready RAG system for academic paper analysis. It:

- ✅ Uploads and indexes papers automatically
- ✅ Finds relevant sections using semantic search
- ✅ Generates accurate answers with source attribution
- ✅ Handles failures gracefully with multi-provider LLM fallback
- ✅ Scales to millions of papers and users
- ✅ Maintains user data privacy with JWT authentication

Start building! 🚀

---

**Last Updated:** April 2026  
**Version:** 1.0.0  
**Maintainer:** PaperLens Team
