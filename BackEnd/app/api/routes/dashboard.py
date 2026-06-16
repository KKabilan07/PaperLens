from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from app.services.supabase_client import get_supabase
from app.utils.security import get_current_user

router = APIRouter()
security = HTTPBearer()

@router.get("/stats")
async def get_dashboard_stats(credentials = Depends(security)):
    """
    Get dashboard metrics for current user
    """
    try:
        user = get_current_user(credentials)
        user_id = user["user_id"]
        supabase = get_supabase()
        
        # 1. Get papers count & sum of words
        papers_response = supabase.table("papers").select("word_count").eq("user_id", user_id).execute()
        papers_count = len(papers_response.data)
        
        total_words = sum([p.get("word_count") or 0 for p in papers_response.data])
        
        # 2. Get questions asked (chats count)
        chats_response = supabase.table("chats").select("id", count="exact").eq("user_id", user_id).execute()
        # Fallback if count is not returned directly
        chats_count = len(chats_response.data) if chats_response.data else 0
        
        return {
            "papers_uploaded": papers_count,
            "questions_asked": chats_count,
            "words_indexed": total_words
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching dashboard stats: {str(e)}"
        )

@router.get("/recent-papers")
async def get_recent_papers(credentials = Depends(security)):
    """
    Get 5 most recently uploaded papers
    """
    try:
        user = get_current_user(credentials)
        user_id = user["user_id"]
        supabase = get_supabase()
        
        response = supabase.table("papers") \
            .select("id, title, page_count, word_count, created_at") \
            .eq("user_id", user_id) \
            .order("created_at", desc=True) \
            .limit(5) \
            .execute()
            
        return response.data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching recent papers: {str(e)}"
        )

@router.get("/recent-chats")
async def get_recent_chats(credentials = Depends(security)):
    """
    Get 5 most recent chats
    """
    try:
        user = get_current_user(credentials)
        user_id = user["user_id"]
        supabase = get_supabase()
        
        # Get chats
        chats_response = supabase.table("chats") \
            .select("id, question, answer, paper_id, created_at") \
            .eq("user_id", user_id) \
            .order("created_at", desc=True) \
            .limit(5) \
            .execute()
            
        chats = chats_response.data
        if not chats:
            return []
            
        # Get associated paper titles
        paper_ids = list(set([c["paper_id"] for c in chats if c.get("paper_id")]))
        if paper_ids:
            papers_response = supabase.table("papers").select("id, title").in_("id", paper_ids).execute()
            paper_map = {p["id"]: p["title"] for p in papers_response.data}
        else:
            paper_map = {}
            
        for c in chats:
            c["paper_title"] = paper_map.get(c.get("paper_id"), "Unknown Paper")
            
        return chats
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching recent chats: {str(e)}"
        )
