import os
from dotenv import load_dotenv

load_dotenv()

# Supabase Configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET", "your-secret-key")

# API Configuration
API_TITLE = "PaperLens API"
API_VERSION = "1.0.0"

# Storage Configuration
STORAGE_BUCKET = "papers"
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

# AI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Database Configuration
DATABASE_URL = os.getenv("DATABASE_URL")
