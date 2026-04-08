"""
Service for processing PDFs and storing embeddings in Supabase pgvector
Handles: extract → chunk → embed → store workflow
"""

from typing import List, Dict
from app.services.pdf_parser import extract_sections_from_text, extract_text_from_pdf
from app.services.embeddings_service import embed_texts
from app.services.supabase_client import get_supabase_client


def chunk_section(content: str, chunk_size: int = 500, overlap: int = 100) -> List[Dict]:
    """
    Chunk a section into smaller pieces with overlap
    
    Args:
        content: Section content
        chunk_size: Characters per chunk
        overlap: Overlap between chunks
    
    Returns:
        List of chunks with metadata
    """
    chunks = []
    sentences = content.split('. ')
    
    current_chunk = ""
    chunk_index = 0
    
    for sentence in sentences:
        if len(current_chunk) + len(sentence) < chunk_size:
            current_chunk += sentence + ". "
        else:
            if current_chunk:
                chunks.append({
                    "content": current_chunk.strip(),
                    "chunk_index": chunk_index
                })
                chunk_index += 1
            
            # Add overlap
            current_chunk = sentence + ". "
    
    # Add last chunk
    if current_chunk:
        chunks.append({
            "content": current_chunk.strip(),
            "chunk_index": chunk_index
        })
    
    return chunks


def process_pdf_to_embeddings(
    pdf_bytes: bytes,
    paper_id: str,
    paper_title: str
) -> Dict:
    """
    Complete PDF processing pipeline: extract → chunk → embed → store
    
    Args:
        pdf_bytes: PDF file content
        paper_id: Paper ID in database
        paper_title: Paper title
    
    Returns:
        Processing result with counts and status
    """
    try:
        # Step 1: Extract text and sections
        extraction_result = extract_text_from_pdf(pdf_bytes)
        sections = extract_sections_from_text(extraction_result["text"])
        
        supabase = get_supabase_client()
        total_chunks = 0
        
        # Step 2: Process each section
        for section in sections:
            section_name = section.get("section_name", "Unknown")
            content = section.get("content", "")
            
            if not content.strip():
                continue
            
            # Step 3: Chunk the section
            chunks = chunk_section(content)
            
            # Step 4: Generate embeddings for all chunks
            chunk_texts = [c["content"] for c in chunks]
            embeddings = embed_texts(chunk_texts)
            
            # Step 5: Prepare data for storage
            records_to_insert = []
            for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
                records_to_insert.append({
                    "paper_id": paper_id,
                    "section_name": section_name,
                    "content": chunk["content"],
                    "embedding": embedding,
                    "chunk_index": chunk["chunk_index"]
                })
            
            # Step 6: Store in Supabase
            if records_to_insert:
                response = supabase.table("sections").insert(records_to_insert).execute()
                total_chunks += len(records_to_insert)
        
        return {
            "status": "success",
            "paper_id": paper_id,
            "paper_title": paper_title,
            "sections_processed": len(sections),
            "total_chunks": total_chunks,
            "embedding_model": "all-MiniLM-L6-v2",
            "embedding_dimension": 384
        }
    
    except Exception as e:
        return {
            "status": "error",
            "paper_id": paper_id,
            "error": str(e)
        }


def delete_paper_embeddings(paper_id: str) -> Dict:
    """
    Delete all embeddings for a paper (cleanup)
    
    Args:
        paper_id: Paper ID to delete
    
    Returns:
        Deletion status
    """
    try:
        supabase = get_supabase_client()
        response = supabase.table("sections").delete().eq("paper_id", paper_id).execute()
        
        return {
            "status": "success",
            "paper_id": paper_id,
            "message": "All embeddings deleted"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }
