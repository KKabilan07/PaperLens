from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPBasicCredentials
from app.models.chat import ChatResponse, QuestionRequest, QuestionResponse
from app.services.supabase_client import get_supabase
from app.services.query_service import query_paper
from app.utils.security import get_current_user
import uuid
from datetime import datetime

router = APIRouter()
security = HTTPBearer()


@router.post("/", response_model=QuestionResponse)
async def ask_question(
    request: QuestionRequest,
    credentials = Depends(security)
):
    """
    Ask a question about a specific paper using RAG (LlamaIndex)
    Retrieves relevant sections and generates contextual answer
    """
    try:
        user = get_current_user(credentials)
        user_id = user["user_id"]
        supabase = get_supabase()
        
        # Verify paper belongs to user
        paper_response = supabase.table("papers").select("title").eq(
            "id", request.paper_id
        ).eq("user_id", user_id).execute()
        
        if not paper_response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Paper not found"
            )
        
        # Generate RAG response (LlamaIndex query)
        try:
            rag_result = await query_paper(
                question=request.question,
                paper_id=request.paper_id
            )
        except Exception as rag_error:
            print(f"RAG Pipeline Error: {str(rag_error)}")
            import traceback
            traceback.print_exc()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"RAG Pipeline Error: {str(rag_error)}"
            )
        
        answer = rag_result.get("answer", "Error generating response")
        provider_used = rag_result.get("provider_used", None)
        sources = rag_result.get("sources", [])
        
        # Store chat in database
        chat_id = str(uuid.uuid4())
        chat_data = {
            "id": chat_id,
            "user_id": user_id,
            "paper_id": request.paper_id,
            "question": request.question,
            "answer": answer,
            "provider_used": provider_used,
            "sources": sources if sources else [],
            "created_at": datetime.utcnow().isoformat()
        }
        
        try:
            supabase.table("chats").insert(chat_data).execute()
        except Exception as db_error:
            print(f"Database insert error (non-critical): {str(db_error)}")
            # Don't fail if chat save fails - user still gets the answer
        
        return QuestionResponse(
            success=True,
            answer=answer,
            chat_id=chat_id,
            provider_used=provider_used,
            sources=sources
        )
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Chat Endpoint Error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing question: {str(e)}"
        )


@router.get("/history/{paper_id}", response_model=list[ChatResponse])
async def get_chat_history(
    paper_id: str,
    credentials = Depends(security)
):
    """
    Get chat history for a specific paper
    """
    try:
        user = get_current_user(credentials)
        user_id = user["user_id"]
        supabase = get_supabase()
        
        # Verify paper belongs to user
        paper_response = supabase.table("papers").select("id").eq(
            "id", paper_id
        ).eq("user_id", user_id).execute()
        
        if not paper_response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Paper not found"
            )
        
        # Fetch chat history
        chats_response = supabase.table("chats").select(
            "id, question, answer, paper_id, provider_used, sources, created_at"
        ).eq("paper_id", paper_id).order("created_at", desc=False).execute()
        
        return [
            ChatResponse(
                id=chat["id"],
                question=chat["question"],
                answer=chat["answer"],
                paper_id=chat["paper_id"],
                provider_used=chat.get("provider_used"),
                sources=chat.get("sources"),
                created_at=chat.get("created_at")
            )
            for chat in chats_response.data
        ]
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching chat history: {str(e)}"
        )


@router.get("/user/{paper_id}")
async def get_user_chats(
    paper_id: str,
    credentials = Depends(security)
):
    """
    Get all chats for a user related to a paper
    """
    try:
        user = get_current_user(credentials)
        user_id = user["user_id"]
        
        # Fetch chats
        supabase = get_supabase()
        chats_response = supabase.table("chats").select("*").eq(
            "user_id", user_id
        ).eq("paper_id", paper_id).order("created_at", desc=True).execute()
        
        return {
            "user_id": user_id,
            "paper_id": paper_id,
            "total_chats": len(chats_response.data),
            "chats": chats_response.data
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching chats: {str(e)}"
        )