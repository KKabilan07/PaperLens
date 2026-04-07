# PaperLens API Quick Reference

**Base URL:** `http://localhost:8000/api/v1`

**Authentication:** All endpoints require `Authorization: Bearer {jwt_token}` header

## Health Endpoints

### Check Service Health
```
GET /health/
Response: { "status": "ok", "service": "PaperLens API", "version": "1.0.0" }
```

### Check Service Readiness
```
GET /health/ready
Response: { "ready": true, "service": "PaperLens API" }
```

---

## Authentication Endpoints

### Get Current User
```
GET /auth/me
Response: { "id": "uuid", "email": "user@example.com", "created_at": "iso-date" }
```

### Get User Statistics
```
GET /auth/stats
Response: { "user_id": "uuid", "papers_count": 5, "chats_count": 23, "email": "user@example.com" }
```

### Logout
```
POST /auth/logout
Response: { "success": true, "message": "Logged out successfully. Clear token from localStorage on frontend." }
```

---

## Paper Endpoints

### List All Papers
```
GET /papers/
Response: [
  {
    "id": "uuid",
    "title": "Paper Title",
    "description": "Optional description",
    "word_count": 5000,
    "page_count": 10,
    "created_at": "iso-date",
    "sections_count": 5
  }
]
```

### Upload Paper
```
POST /papers/upload
Content-Type: multipart/form-data
Parameters:
  - file (required): PDF file
  - title (optional): Custom title for paper

Response: {
  "success": true,
  "paper_id": "uuid",
  "title": "Paper Title",
  "sections_count": 5,
  "word_count": 5000,
  "message": "Paper 'Title' uploaded successfully with 5 sections"
}
```

### Get Paper with Sections
```
GET /papers/{paper_id}
Response: {
  "id": "uuid",
  "user_id": "uuid",
  "title": "Paper Title",
  "description": "Optional",
  "file_path": "storage/path",
  "word_count": 5000,
  "page_count": 10,
  "created_at": "iso-date",
  "updated_at": "iso-date",
  "sections": [
    {
      "id": "uuid",
      "paper_id": "uuid",
      "section_name": "Introduction",
      "content": "Section text...",
      "page_numbers": [1, 2],
      "created_at": "iso-date"
    }
  ]
}
```

### Get Paper Sections Only
```
GET /papers/{paper_id}/sections
Response: {
  "paper_id": "uuid",
  "sections": [
    {
      "id": "uuid",
      "paper_id": "uuid",
      "section_name": "Section Name",
      "content": "Content...",
      "page_numbers": [1, 2],
      "created_at": "iso-date"
    }
  ]
}
```

### Delete Paper
```
DELETE /papers/{paper_id}
Response: {
  "success": true,
  "message": "Paper deleted successfully"
}
```

### Compare Two Papers
```
POST /papers/{paper_id}/compare?other_paper_id={other_id}
Response: {
  "paper1": "Title 1",
  "paper2": "Title 2",
  "paper1_words": 5000,
  "paper2_words": 6000,
  "message": "Comparison analysis ready (AI analysis pending)"
}
```

---

## Chat Endpoints

### Ask Question About Paper
```
POST /chat/
Content-Type: application/json
Body: {
  "question": "What is this paper about?",
  "paper_id": "uuid"
}

Response: {
  "success": true,
  "answer": "AI-generated response based on paper content...",
  "chat_id": "uuid"
}
```

### Get Chat History for Paper
```
GET /chat/history/{paper_id}
Response: [
  {
    "id": "uuid",
    "question": "Your question?",
    "answer": "Generated answer...",
    "paper_id": "uuid",
    "created_at": "iso-date"
  }
]
```

### Get User's Chats for Paper
```
GET /chat/user/{paper_id}
Response: {
  "user_id": "uuid",
  "paper_id": "uuid",
  "total_chats": 5,
  "chats": [
    {
      "id": "uuid",
      "user_id": "uuid",
      "paper_id": "uuid",
      "question": "Question text",
      "answer": "Answer text",
      "created_at": "iso-date"
    }
  ]
}
```

---

## Error Responses

All errors follow this format:
```json
{
  "detail": "Error description"
}
```

### Common Status Codes
- `400` - Bad request (invalid input, missing fields)
- `401` - Unauthorized (missing or invalid JWT token)
- `403` - Forbidden (no access to resource)
- `404` - Not found (resource doesn't exist)
- `500` - Server error (internal error)

### Example Errors
```json
{ "detail": "Paper not found" }
{ "detail": "Token expired" }
{ "detail": "Could not validate credentials" }
{ "detail": "Error uploading paper: Invalid PDF format" }
```

---

## Request Headers

All requests should include:
```
Authorization: Bearer {jwt_token}
Content-Type: application/json  (except file uploads use multipart/form-data)
```

## Frontend Integration Example

```javascript
// Get JWT token from localStorage (set by AuthContext)
const token = localStorage.getItem('sb-access-token');

// Example: Upload a paper
const fileInput = document.querySelector('input[type="file"]');
const formData = new FormData();
formData.append('file', fileInput.files[0]);
formData.append('title', 'My Research Paper');

const response = await fetch('http://localhost:8000/api/v1/papers/upload', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`
  },
  body: formData
});

const result = await response.json();
console.log('Paper uploaded:', result.paper_id);

// Example: Ask a question
const response = await fetch('http://localhost:8000/api/v1/chat/', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    question: 'What are the main findings?',
    paper_id: result.paper_id
  })
});

const chat = await response.json();
console.log('Answer:', chat.answer);
```

---

## Testing with cURL

### Upload Paper
```bash
curl -X POST http://localhost:8000/api/v1/papers/upload \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -F "file=@research.pdf" \
  -F "title=Research Paper"
```

### Get Papers
```bash
curl http://localhost:8000/api/v1/papers/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Ask Question
```bash
curl -X POST http://localhost:8000/api/v1/chat/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"question":"What is this about?","paper_id":"uuid"}'
```

### Get User Stats
```bash
curl http://localhost:8000/api/v1/auth/stats \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

---

## WebUI Endpoints

- **Swagger UI (Interactive):** `http://localhost:8000/docs`
- **ReDoc (Read-only):** `http://localhost:8000/redoc`
- **OpenAPI JSON:** `http://localhost:8000/openapi.json`

These provide full interactive API documentation with try-it-out capability.
