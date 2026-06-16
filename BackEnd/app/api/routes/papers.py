from fastapi import APIRouter, HTTPException, status, UploadFile, File, Depends, Response
from fastapi.security import HTTPBearer, HTTPBasicCredentials
from app.models.paper import PaperResponse, PaperUploadResponse, PaperWithSections
from app.services.supabase_client import get_supabase
from app.services.ingestion_service import ingest_paper
from app.utils.security import get_current_user
from app.models.paper import Section, Paper
import uuid
from datetime import datetime

router = APIRouter()
security = HTTPBearer()


@router.get("/", response_model=list[PaperResponse])
async def get_papers(credentials = Depends(security)):
    """
    Get all papers for the current user
    """
    try:
        user = get_current_user(credentials)
        user_id = user["user_id"]
        supabase = get_supabase()
        
        # Fetch papers from Supabase
        response = supabase.table("papers").select(
            "*, sections(count)"
        ).eq("user_id", user_id).execute()
        
        papers = response.data
        
        return [
            PaperResponse(
                id=paper["id"],
                title=paper["title"],
                description=paper.get("description"),
                word_count=paper.get("word_count"),
                page_count=paper.get("page_count"),
                created_at=paper.get("created_at"),
                sections_count=len(paper.get("sections", []))
            )
            for paper in papers
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching papers: {str(e)}"
        )


@router.post("/upload", response_model=PaperUploadResponse)
async def upload_paper(
    file: UploadFile = File(...),
    title: str = None,
    credentials = Depends(security)
):
    """
    Upload and parse a PDF paper
    """
    try:
        user = get_current_user(credentials)
        user_id = user["user_id"]
        
        # Validate file type - must be PDF
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only PDF files are allowed"
            )
        
        # Read file content
        contents = await file.read()
        
        if not contents:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Empty file"
            )
        
        # Validate file size - max 50MB
        MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB in bytes
        if len(contents) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File size exceeds maximum limit of 50MB. Your file is {len(contents) / (1024*1024):.2f}MB"
            )
        
        # Ingest using LlamaIndex ingestion service
        result = await ingest_paper(
            pdf_bytes=contents,
            file_name=file.filename,
            user_id=user_id,
            title=title
        )
        
        return PaperUploadResponse(
            success=result["success"],
            paper_id=result["paper_id"],
            title=result["title"],
            sections_count=result["sections_count"],
            word_count=result["word_count"],
            message=result["message"]
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error uploading paper: {str(e)}"
        )


@router.get("/{paper_id}", response_model=PaperWithSections)
async def get_paper(
    paper_id: str,
    credentials = Depends(security)
):
    """
    Get specific paper with all its sections
    """
    try:
        user = get_current_user(credentials)
        user_id = user["user_id"]
        supabase = get_supabase()
        
        # Fetch paper
        paper_response = supabase.table("papers").select("*").eq(
            "id", paper_id
        ).eq("user_id", user_id).execute()
        
        if not paper_response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Paper not found"
            )
        
        paper = paper_response.data[0]
        
        # Fetch sections
        sections_response = supabase.table("sections").select("*").eq(
            "paper_id", paper_id
        ).execute()
        
        sections = [
            Section(
                id=s["id"],
                paper_id=s["paper_id"],
                section_name=s["section_name"],
                content=s["content"],
                page_numbers=s.get("page_numbers", []),
                created_at=s.get("created_at")
            )
            for s in sections_response.data
        ]
        
        return PaperWithSections(
            id=paper["id"],
            user_id=paper["user_id"],
            title=paper["title"],
            description=paper.get("description"),
            file_path=paper.get("file_path"),
            word_count=paper.get("word_count"),
            page_count=paper.get("page_count"),
            created_at=paper.get("created_at"),
            updated_at=paper.get("updated_at"),
            sections=sections
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching paper: {str(e)}"
        )


@router.delete("/{paper_id}")
async def delete_paper(
    paper_id: str,
    credentials = Depends(security)
):
    """
    Delete a paper and its associated data
    """
    try:
        user = get_current_user(credentials)
        user_id = user["user_id"]
        supabase = get_supabase()
        
        # Verify paper belongs to user
        paper_response = supabase.table("papers").select("id, file_path").eq(
            "id", paper_id
        ).eq("user_id", user_id).execute()
        
        if not paper_response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Paper not found"
            )
        
        paper = paper_response.data[0]
        
        # Delete sections
        supabase.table("sections").delete().eq("paper_id", paper_id).execute()
        
        # Delete chats
        supabase.table("chats").delete().eq("paper_id", paper_id).execute()
        
        # Delete paper
        supabase.table("papers").delete().eq("id", paper_id).execute()
        
        # Delete file from storage
        if paper.get("file_path"):
            try:
                storage_path = paper["file_path"]
                if storage_path.startswith("papers/"):
                    storage_path = storage_path[len("papers/"):]
                supabase.storage.from_("papers").remove([storage_path])
            except:
                pass  # File might not exist
        
        return {
            "success": True,
            "message": f"Paper deleted successfully"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting paper: {str(e)}"
        )


@router.get("/{paper_id}/sections")
async def get_paper_sections(
    paper_id: str,
    credentials = Depends(security)
):
    """
    Get all sections of a paper
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
        
        # Fetch sections
        sections_response = supabase.table("sections").select("*").eq(
            "paper_id", paper_id
        ).execute()
        
        return {
            "paper_id": paper_id,
            "sections": sections_response.data
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching sections: {str(e)}"
        )


@router.post("/{paper_id}/compare")
async def compare_papers(
    paper_id: str,
    other_paper_id: str,
    credentials = Depends(security)
):
    """
    Compare two papers
    """
    try:
        supabase = get_supabase()
        user = get_current_user(credentials)
        user_id = user["user_id"]
        
        # Verify both papers belong to user
        papers_response = supabase.table("papers").select("id, title").eq(
            "user_id", user_id
        ).in_("id", [paper_id, other_paper_id]).execute()
        
        if len(papers_response.data) != 2:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="One or both papers not found"
            )
        
        papers = {p["id"]: p["title"] for p in papers_response.data}
        
        # Fetch content from sections
        sections1 = supabase.table("sections").select("content").eq(
            "paper_id", paper_id
        ).execute()
        
        sections2 = supabase.table("sections").select("content").eq(
            "paper_id", other_paper_id
        ).execute()
        
        content1 = " ".join([s["content"] for s in sections1.data])
        content2 = " ".join([s["content"] for s in sections2.data])
        
        return {
            "paper1": papers.get(paper_id),
            "paper2": papers.get(other_paper_id),
            "paper1_words": len(content1.split()),
            "paper2_words": len(content2.split()),
            "message": "Comparison analysis ready (AI analysis pending)"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error comparing papers: {str(e)}"
        )


@router.get("/{paper_id}/summary")
async def get_paper_summary(
    paper_id: str,
    credentials = Depends(security)
):
    """
    Get or generate cached structured summary of a paper
    """
    try:
        user = get_current_user(credentials)
        user_id = user["user_id"]
        supabase = get_supabase()
        
        # Verify paper belongs to user
        paper_res = supabase.table("papers").select("title").eq(
            "id", paper_id
        ).eq("user_id", user_id).execute()
        if not paper_res.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Paper not found"
            )
        
        # Check if summary section already exists
        summary_res = supabase.table("sections").select("content").eq(
            "paper_id", paper_id
        ).eq("section_name", "Summary").execute()
        
        if summary_res.data:
            return {"summary": summary_res.data[0]["content"]}
            
        # If not, generate summary using LLM
        # Fetch sections content
        sections_res = supabase.table("sections").select("content").eq(
            "paper_id", paper_id
        ).order("chunk_index", desc=False).execute()
        
        if not sections_res.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No paper content found to summarize"
            )
            
        # Combine text (up to ~8000 words to prevent token limit errors)
        combined_text = "\n\n".join([s["content"] for s in sections_res.data[:20]])
        
        prompt = (
            "You are a professional research assistant. Summarize the following research paper. "
            "You MUST provide a structured, clean, and comprehensive summary using exactly the following headers:\n\n"
            "## Problem Statement\n"
            "[Provide a detailed statement of the problem being solved]\n\n"
            "## Methodology\n"
            "[Detail the exact methodology, framework, and pipeline used]\n\n"
            "## Results\n"
            "[Describe key results, figures, statistics, and findings]\n\n"
            "## Limitations\n"
            "[List limitations of the work]\n\n"
            "## Future Work\n"
            "[Discuss future research directions]\n\n"
            "Make sure it is professional and uses markdown.\n\n"
            f"Paper Content:\n{combined_text}"
        )
        
        from llama_index.core import Settings
        response = await Settings.llm.acomplete(prompt)
        summary_text = response.text
        
        # Cache summary back to database as a special section
        supabase.table("sections").insert({
            "paper_id": paper_id,
            "section_name": "Summary",
            "content": summary_text,
            "chunk_index": -1
        }).execute()
        
        return {"summary": summary_text}
        
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating paper summary: {str(e)}"
        )


from fastapi.security import HTTPBearer
from app.utils.security import verify_jwt_token

security_optional = HTTPBearer(auto_error=False)

@router.get("/{paper_id}/pdf")
async def get_paper_pdf(
    paper_id: str,
    token: str = None,
    credentials = Depends(security_optional)
):
    """
    Retrieve and stream the PDF file for a paper
    """
    try:
        # Extract JWT token from header or query param
        jwt_token = None
        if credentials:
            jwt_token = credentials.credentials
        elif token:
            jwt_token = token
            
        if not jwt_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated"
            )
            
        payload = verify_jwt_token(jwt_token)
        user_id = payload.get("sub") or payload.get("user_id") or payload.get("userId")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload"
            )
            
        supabase = get_supabase()
        
        # Verify paper belongs to user
        paper_res = supabase.table("papers").select("file_path").eq(
            "id", paper_id
        ).eq("user_id", user_id).execute()
        
        if not paper_res.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Paper not found"
            )
            
        file_path = paper_res.data[0]["file_path"]
        if not file_path:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="PDF file path not found"
            )
            
        # Clean prefix mismatch if present
        if file_path.startswith("papers/"):
            file_path = file_path[len("papers/"):]
            
        # Download PDF bytes from Supabase storage
        try:
            pdf_bytes = supabase.storage.from_("papers").download(file_path)
        except Exception as storage_err:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Error retrieving PDF from storage: {str(storage_err)}"
            )
            
        return Response(content=pdf_bytes, media_type="application/pdf")
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching PDF: {str(e)}"
        )


from pydantic import BaseModel
from typing import List

class MultiPaperChatRequest(BaseModel):
    paper_ids: List[str]
    question: str


@router.post("/multi-chat")
async def multi_paper_chat(
    request: MultiPaperChatRequest,
    credentials = Depends(security)
):
    """
    Chat across multiple papers simultaneously using in-memory RAG
    """
    try:
        user = get_current_user(credentials)
        user_id = user["user_id"]
        supabase = get_supabase()
        
        # 1. Verify all papers belong to user
        papers_res = supabase.table("papers").select("id, title").in_(
            "id", request.paper_ids
        ).eq("user_id", user_id).execute()
        
        if len(papers_res.data) != len(request.paper_ids):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="One or more papers could not be found or do not belong to you"
            )
            
        paper_title_map = {p["id"]: p["title"] for p in papers_res.data}
        
        # 2. Get sections for all papers
        sections_res = supabase.table("sections").select(
            "paper_id, section_name, content, chunk_index, embedding"
        ).in_("paper_id", request.paper_ids).execute()
        
        sections = sections_res.data
        if not sections:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No content found in selected papers"
            )
            
        # 3. Create index in memory
        from llama_index.core.schema import TextNode
        from llama_index.core import VectorStoreIndex
        import json
        
        nodes = []
        for s in sections:
            embedding = s.get("embedding")
            if isinstance(embedding, str):
                try:
                    embedding = json.loads(embedding)
                except:
                    pass
                    
            node = TextNode(
                text=s["content"],
                embedding=embedding,
                metadata={
                    "paper_id": s["paper_id"],
                    "paper_title": paper_title_map.get(s["paper_id"], "Unknown"),
                    "section_name": s.get("section_name", "Content"),
                    "chunk_index": s.get("chunk_index", 0)
                }
            )
            nodes.append(node)
            
        index = VectorStoreIndex(nodes)
        
        # 4. RAG Query
        query_engine = index.as_query_engine(
            similarity_top_k=8,
            response_mode="compact"
        )
        
        response_obj = await query_engine.aquery(request.question)
        
        # 5. Extract sources
        sources = []
        if response_obj.source_nodes:
            for node in response_obj.source_nodes:
                p_title = node.metadata.get("paper_title", "Unknown")
                sec_name = node.metadata.get("section_name", "Content")
                source_label = f"{p_title} ({sec_name})"
                if source_label not in sources:
                    sources.append(source_label)
                    
        # Store chat in db (associate it with the first paper for listing, or handle separately.
        # Let's save it for each paper, or just save it without associating to a specific paper (paper_id=None).
        # Wait, the chats table schema might require a paper_id. Let's save it under the first paper_id but with a flag,
        # or just save it.
        chat_id = str(uuid.uuid4())
        chat_data = {
            "id": chat_id,
            "user_id": user_id,
            "paper_id": request.paper_ids[0] if request.paper_ids else None,
            "question": request.question,
            "answer": str(response_obj),
            "provider_used": Settings.llm.metadata.model_name,
            "sources": sources,
            "created_at": datetime.utcnow().isoformat()
        }
        
        try:
            supabase.table("chats").insert(chat_data).execute()
        except Exception as db_err:
            print(f"Database insert error for multi-chat: {str(db_err)}")
            
        return {
            "success": True,
            "answer": str(response_obj),
            "chat_id": chat_id,
            "provider_used": Settings.llm.metadata.model_name,
            "sources": sources
        }
        
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error in multi-paper chat: {str(e)}"
        )