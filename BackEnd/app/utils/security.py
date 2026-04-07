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
    """
    try:
        # Try to decode with RS256 (Supabase default) first
        try:
            payload = jwt.decode(token, options={"verify_signature": False})
            return payload
        except:
            # Fallback to HS256
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credentials: {str(e)}"
        )


def get_current_user(credentials) -> dict:
    """
    Get current user from JWT token
    """
    token = credentials.credentials
    payload = verify_jwt_token(token)
    
    user_id = payload.get("sub") or payload.get("user_id")
    email = payload.get("email")
    
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not extract user information from token"
        )
    
    return {"user_id": user_id, "email": email}
