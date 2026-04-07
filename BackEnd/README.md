# PaperLens Backend API

## Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Copy `.env.example` to `.env` and fill in your configuration:
```bash
cp .env.example .env
```

### 3. Setup Database Schema
Run the SQL in `database_schema.sql` in your Supabase SQL editor

### 4. Run the Server
```bash
# On Unix/Linux/Mac
./run.sh

# On Windows
run.bat

# Or directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API Documentation

Once running, visit:
- API Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Endpoints

### Health Check
- `GET /api/v1/health/` - Health check
- `GET /api/v1/health/ready` - Readiness check

### Authentication
- `GET /api/v1/auth/me` - Get current user info
- `POST /api/v1/auth/logout` - Logout
- `GET /api/v1/auth/stats` - Get user statistics

### Papers
- `GET /api/v1/papers/` - List all user papers
- `POST /api/v1/papers/upload` - Upload a PDF paper
- `GET /api/v1/papers/{paper_id}` - Get paper with sections
- `GET /api/v1/papers/{paper_id}/sections` - Get paper sections
- `DELETE /api/v1/papers/{paper_id}` - Delete paper
- `POST /api/v1/papers/{paper_id}/compare` - Compare two papers

### Chat
- `POST /api/v1/chat/` - Ask a question about a paper
- `GET /api/v1/chat/history/{paper_id}` - Get chat history
- `GET /api/v1/chat/user/{paper_id}` - Get user's chats for a paper

## Project Structure

```
BackEnd/
├── app/
│   ├── main.py              # FastAPI application
│   ├── api/
│   │   ├── api.py           # Router configuration
│   │   └── routes/
│   │       ├── health.py    # Health check endpoints
│   │       ├── auth.py      # Authentication endpoints
│   │       ├── papers.py    # Paper management endpoints
│   │       └── chat.py      # Chat endpoints
│   ├── core/
│   │   └── config.py        # Configuration
│   ├── models/
│   │   ├── user.py          # User models
│   │   ├── paper.py         # Paper models
│   │   └── chat.py          # Chat models
│   ├── services/
│   │   ├── supabase_client.py   # Supabase client
│   │   ├── pdf_parser.py        # PDF parsing
│   │   ├── explainer.py         # AI explanation service
│   │   └── summarizer.py        # Summarization service
│   └── utils/
│       └── security.py      # JWT verification
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
├── database_schema.sql     # Database schema
├── run.sh                  # Unix/Linux startup script
└── run.bat                 # Windows startup script
```

## Key Features

### JWT Authentication
All endpoints (except health) require JWT token in Authorization header:
```
Authorization: Bearer {jwt_token}
```

### Paper Upload
- PDF parsing with section extraction
- Automatic metadata extraction
- File storage in Supabase Storage
- Database indexing for fast queries

### Chat System
- Question answering based on paper content
- Chat history persistence
- Context-aware responses

### Paper Comparison
- Side-by-side analysis
- Word count comparison
- Common topic extraction

## Security

- JWT token validation on all protected endpoints
- Row-level security (RLS) policies in database
- CORS middleware for frontend integration
- User isolation - users can only access their own data

## Error Handling

All endpoints return proper HTTP status codes:
- `200` - Success
- `400` - Bad request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not found
- `500` - Server error

## Future Enhancements

- [ ] Integration with OpenAI for better AI responses
- [ ] Advanced paper comparison algorithms
- [ ] Collaborative features
- [ ] Export to various formats
- [ ] Full-text search
- [ ] Batch processing
