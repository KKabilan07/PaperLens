from fastapi import APIRouter, HTTPException, status, UploadFile, File, Depends
from fastapi.security import HTTPBearer, HTTPBasicCredentials
from app.models.paper import PaperResponse, PaperUploadResponse, PaperWithSections
from app.services.supabase_client import get_supabase
from app.services.pdf_parser import parse_pdf
from app.services.embedding_storage_service import process_pdf_to_embeddings
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
        supabase = get_supabase()
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
        
        # Parse PDF
        parsed_data = parse_pdf(contents)
        
        # Generate paper title
        paper_title = title or parsed_data["metadata"].get("title") or file.filename
        
        # Create paper record
        paper_id = str(uuid.uuid4())
        paper_data = {
            "id": paper_id,
            "user_id": user_id,
            "title": paper_title,
            "description": parsed_data["metadata"].get("subject", ""),
            "word_count": parsed_data["word_count"],
            "page_count": parsed_data["num_pages"],
            "file_path": f"papers/{user_id}/{paper_id}/{file.filename}",
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }
        
        # Insert paper into database
        supabase.table("papers").insert(paper_data).execute()
        
        # Store sections
        sections_created = 0
        for idx, section in enumerate(parsed_data["sections"]):
            section_id = str(uuid.uuid4())
            section_data = {
                "id": section_id,
                "paper_id": paper_id,
                "section_name": section["section_name"],
                "content": section["content"],
                "page_numbers": section.get("page_numbers", []),
                "created_at": datetime.utcnow().isoformat()
            }
            supabase.table("sections").insert(section_data).execute()
            sections_created += 1
        
        # Upload PDF file to storage
        file_path = f"{user_id}/{paper_id}/{file.filename}"
        supabase.storage.from_("papers").upload(file_path, contents)
        
        # Generate embeddings for RAG (async-like, but we'll do it synchronously for now)
        try:
            embedding_result = process_pdf_to_embeddings(contents, paper_id, paper_title)
            embedding_status = embedding_result.get("status", "unknown")
            total_chunks = embedding_result.get("total_chunks", 0)
        except Exception as e:
            embedding_status = "failed"
            total_chunks = 0
            print(f"Embedding generation failed: {str(e)}")
        
        return PaperUploadResponse(
            success=True,
            paper_id=paper_id,
            title=paper_title,
            sections_count=sections_created,
            word_count=parsed_data["word_count"],
            message=f"Paper '{paper_title}' uploaded successfully with {sections_created} sections. "
                    f"Embeddings: {total_chunks} chunks processed ({embedding_status})"
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
                supabase.storage.from_("papers").remove([paper["file_path"]])
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