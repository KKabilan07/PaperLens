import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

# Initialize Supabase client only if credentials are available
supabase = None

def get_supabase():
    """Get Supabase client, initializing if needed"""
    global supabase
    
    if supabase is None:
        if not SUPABASE_URL or not SUPABASE_KEY:
            raise RuntimeError(
                "Supabase credentials not found. "
                "Please set SUPABASE_URL and SUPABASE_SERVICE_KEY environment variables."
            )
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    return supabase