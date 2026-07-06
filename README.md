# PaperLens

PaperLens is an AI-powered academic paper analysis and collaboration platform. It allows researchers to upload PDF papers, parse and index them using advanced document parsing (LlamaParse), perform RAG-based (Retrieval-Augmented Generation) chat querying over documents, and view real-time research metrics on a modern dashboard.

---

## 🔗 Live Deployments

* **Frontend Web App (Vercel):** [https://paperlens-research.vercel.app/](https://paperlens-research.vercel.app/)
* **Backend API (Render):** [https://paperlens-research.onrender.com](https://paperlens-research.onrender.com)

---

## 🛠️ Tech Stack

### Frontend
* **Core Framework:** React 18 (Vite SPA)
* **Routing:** React Router v6
* **State & Authentication:** Supabase Auth (OAuth Google Sign-In & Email/Password)
* **Styling & Design:** Vanilla CSS with custom design tokens, modern typography, glassmorphism, and responsive layouts
* **Icons:** Lucide React

### Backend
* **Web Framework:** FastAPI (Python 3.10+)
* **AI & Retrieval System (RAG):** LlamaIndex
* **Large Language Model (LLM):** Gemini API (via LlamaIndex Gemini Integration)
* **Document Parsing:** LlamaParse (advanced layout-aware PDF ingestion)
* **Database & Storage:** Supabase (PostgreSQL database & object storage for PDF files)
* **Authentication Verification:** Supabase JWT Verification middleware

---

## 📂 Project Structure

```text
PaperLens/
├── FrontEnd/                 # React Frontend (Vite)
│   ├── src/
│   │   ├── Components/       # Reusable UI components (Sidebar, etc.)
│   │   ├── context/          # Authentication and global contexts
│   │   ├── lib/              # Client initializations (Supabase client)
│   │   ├── pages/            # Page components (Dashboard, LoginPage, etc.)
│   │   ├── styles/           # CSS files and global variables
│   │   ├── utils/            # Utility modules (API fetch helper, services)
│   │   ├── App.css
│   │   ├── App.jsx           # Main routing & application entry
│   │   └── main.jsx
│   ├── index.html
│   ├── package.json
│   ├── vercel.json           # Vercel SPA routing configuration
│   └── vite.config.js
│
├── BackEnd/                  # FastAPI Backend
│   ├── app/
│   │   ├── api/
│   │   │   ├── routes/       # API endpoints (auth, chat, dashboard, papers)
│   │   │   └── api.py        # Centralized router definition
│   │   ├── core/             # Configuration & security settings
│   │   ├── models/           # Data schemas and Pydantic validation models
│   │   ├── services/         # Core business logic (LlamaIndex, LLM, ingestion)
│   │   ├── utils/            # Helper utilities
│   │   └── main.py           # Application entry point & CORS configuration
│   ├── Dockerfile            # Containerization configuration
│   ├── requirements.txt      # Python dependencies
│   └── .dockerignore
└── README.md                 # Project documentation
```

---

## 🚀 Key Features

* **Secure Authentication:** User management through Supabase Auth including email sign-in and Google OAuth.
* **Smart Dashboard:** Visualization of research summary stats (papers uploaded, questions asked, words indexed) and recent activities.
* **Advanced Document Parsing:** Uses LlamaParse to extract content from complex tables, mathematical formulas, and layouts in scientific papers.
* **Interactive RAG Chat:** Chat directly with your uploaded papers using Gemini API for context-rich Q&A and summarizing.
* **Paper Repository:** Structured list of all uploaded papers with search capabilities, document preview, and details.

---

## ⚙️ Environment Configuration

### Frontend (`FrontEnd/.env`)
Create a `.env` file in the `FrontEnd` directory:
```env
VITE_SUPABASE_URL=your_supabase_url
VITE_SUPABASE_ANON_KEY=your_supabase_anon_key
VITE_API_URL=http://localhost:8000 # Set to https://paperlens-research.onrender.com for production
```

### Backend (`BackEnd/.env`)
Create a `.env` file in the `BackEnd` directory:
```env
SUPABASE_URL=your_supabase_url
SUPABASE_SERVICE_KEY=your_supabase_service_role_key
SUPABASE_JWT_SECRET=your_supabase_jwt_secret
GEMINI_API_KEY=your_gemini_api_key
LLAMA_PARSE_KEY=your_llamaparse_api_key
```

---

## 💻 Local Development Setup

### Backend Setup
1. Navigate to the `BackEnd` folder:
   ```bash
   cd BackEnd
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the development server:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

#### Running Backend with Docker
Alternatively, you can build and run the backend using Docker:
1. Build the Docker image:
   ```bash
   docker build -t paperlens-backend .
   ```
2. Run the Docker container (passing env variables via a `.env` file):
   ```bash
   docker run -p 8000:8000 --env-file .env paperlens-backend
   ```


### Frontend Setup
1. Navigate to the `FrontEnd` folder:
   ```bash
   cd ../FrontEnd
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run the development server:
   ```bash
   npm run dev
   ```
4. Open [http://localhost:5173](http://localhost:5173) in your browser.
