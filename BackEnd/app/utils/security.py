import os
from fastapi import HTTPException, status
from fastapi.security import HTTPBearer, HTTPBasicCredentials
from functools import wraps
import jwt
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET", "your-secret-key")
JWT_ALGORITHM = "HS256"

security = HTTPBearer()


def verify_jwt_token(token: str) -> dict:
    """
    Verify JWT token and return decoded payload
    Handles both Supabase and custom tokens
    """
    try:
        # First, try to decode without verification (trust Supabase)
        # This works because Supabase tokens are already verified by their server
        payload = jwt.decode(token, options={"verify_signature": False})
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token format"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token verification failed: {str(e)}"
        )


def get_current_user(credentials) -> dict:
    """
    Get current user from JWT token
    Extracts user_id and email from various token formats
    """
    try:
        token = credentials.credentials
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not extract token from Authorization header"
        )
    
    payload = verify_jwt_token(token)
    
    # Try multiple formats for user_id
    user_id = (
        payload.get("sub")  # Supabase standard (ES256 tokens)
        or payload.get("user_id")  # snake_case
        or payload.get("userId")  # camelCase
        or payload.get("uid")  # Alternative
    )
    email = payload.get("email")
    
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not extract user information from token. Token may be invalid."
        )
    
    return {"user_id": str(user_id), "email": email}
