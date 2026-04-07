from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPBasicCredentials
from app.utils.security import get_current_user
from app.services.supabase_client import get_supabase

router = APIRouter()
security = HTTPBearer()


@router.get("/me")
async def get_current_user_info(credentials = Depends(security)):
    """
    Get current user information
    """
    try:
        user = get_current_user(credentials)
        supabase = get_supabase()
        
        # Optionally fetch additional user data from database
        try:
            user_response = supabase.table("users").select("*").eq(
                "id", user["user_id"]
            ).execute()
            
            if user_response.data:
                user_data = user_response.data[0]
                return {
                    "id": user_data.get("id"),
                    "email": user_data.get("email"),
                    "created_at": user_data.get("created_at"),
                    "updated_at": user_data.get("updated_at")
                }
        except:
            pass
        
        # Return basic user info from token
        return {
            "id": user["user_id"],
            "email": user.get("email", ""),
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Error fetching user info: {str(e)}"
        )


@router.post("/logout")
async def logout(credentials = Depends(security)):
    """
    Logout endpoint (mainly for frontend coordination)
    """
    return {
        "success": True,
        "message": "Logged out successfully. Clear token from localStorage on frontend."
    }


@router.get("/stats")
async def get_user_stats(credentials = Depends(security)):
    """
    Get user statistics
    """
    try:
        user = get_current_user(credentials)
        supabase = get_supabase()
        user_id = user["user_id"]
        
        # Count papers
        papers = supabase.table("papers").select("id", count="exact").eq(
            "user_id", user_id
        ).execute()
        
        # Count chats
        chats = supabase.table("chats").select("id", count="exact").eq(
            "user_id", user_id
        ).execute()
        
        papers_count = len(papers.data) if papers.data else 0
        chats_count = len(chats.data) if chats.data else 0
        
        return {
            "user_id": user_id,
            "papers_count": papers_count,
            "chats_count": chats_count,
            "email": user.get("email")
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching stats: {str(e)}"
        )