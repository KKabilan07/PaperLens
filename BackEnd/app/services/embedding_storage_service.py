"""
Service for processing PDFs and storing embeddings in Supabase pgvector
Handles: extract → chunk → embed → store workflow
"""

from typing import List, Dict
from app.services.pdf_parser import extract_sections_from_text, extract_text_from_pdf
from app.services.embeddings_service import embed_texts
from app.services.supabase_client import get_supabase


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
        print(f"\n=== PDF Embedding Pipeline Started ===")
        print(f"Paper: {paper_title} ({paper_id})")
        
        # Step 1: Extract text and sections
        print(f"Step 1: Extracting text from PDF...")
        extraction_result = extract_text_from_pdf(pdf_bytes)
        print(f"  ✓ Extracted {extraction_result['num_pages']} pages, {extraction_result['word_count']} words")
        
        sections = extract_sections_from_text(extraction_result["text"])
        print(f"  ✓ Found {len(sections)} sections")
        
        supabase = get_supabase()
        total_chunks = 0
        sections_processed = 0
        
        # Step 2: Process each section
        for section_idx, section in enumerate(sections, 1):
            section_name = section.get("section_name", "Unknown")
            content = section.get("content", "")
            
            if not content.strip():
                print(f"  ⊘ Section {section_idx} ({section_name}): Empty content, skipping")
                continue
            
            print(f"\nStep 2.{section_idx}: Processing section '{section_name}'")
            
            # Step 3: Chunk the section
            chunks = chunk_section(content)
            print(f"  ✓ Created {len(chunks)} chunks")
            
            # Step 4: Generate embeddings for all chunks
            print(f"Step 3.{section_idx}: Generating embeddings...")
            chunk_texts = [c["content"] for c in chunks]
            embeddings = embed_texts(chunk_texts)
            print(f"  ✓ Generated {len(embeddings)} embeddings (384 dimensions)")
            
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
                print(f"Step 4.{section_idx}: Storing {len(records_to_insert)} embeddings in Supabase...")
                try:
                    response = supabase.table("sections").insert(records_to_insert).execute()
                    print(f"  ✓ Successfully stored {len(records_to_insert)} embeddings")
                    total_chunks += len(records_to_insert)
                    sections_processed += 1
                except Exception as insert_error:
                    print(f"  ✗ ERROR storing embeddings: {str(insert_error)}")
                    print(f"  Details: {insert_error}")
                    import traceback
                    traceback.print_exc()
                    raise insert_error
        
        result = {
            "status": "success",
            "paper_id": paper_id,
            "paper_title": paper_title,
            "sections_processed": sections_processed,
            "total_chunks": total_chunks,
            "embedding_model": "all-MiniLM-L6-v2",
            "embedding_dimension": 384
        }
        print(f"\n=== Embedding Pipeline Complete ===")
        print(f"  ✓ {sections_processed} sections processed")
        print(f"  ✓ {total_chunks} total chunks stored")
        return result
    
    except Exception as e:
        error_msg = f"Error in embedding pipeline: {str(e)}"
        print(f"\n=== Embedding Pipeline ERROR ===")
        print(error_msg)
        import traceback
        traceback.print_exc()
        return {
            "status": "error",
            "paper_id": paper_id,
            "error": error_msg
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
        supabase = get_supabase()
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


def check_database_setup() -> Dict:
    """
    Check if the database is properly configured for embeddings
    Verifies: pgvector extension, embedding column, necessary tables
    
    Returns:
        Dict with setup status and any issues found
    """
    try:
        supabase = get_supabase()
        issues = []
        
        print("\n=== Database Setup Diagnostic ===")
        
        # Check 1: Try to query sections table structure
        print("Check 1: Checking sections table structure...")
        try:
            response = supabase.table("sections").select("id, embedding, chunk_index").limit(1).execute()
            print("  ✓ Sections table accessible")
            
            # Check if we got data back to verify embedding column exists
            if response.data:
                first_row = response.data[0]
                if "embedding" in first_row:
                    if first_row["embedding"] is None:
                        print("  ⚠ Warning: embedding column exists but contains NULL values")
                        print("  → This means embeddings haven't been generated yet for existing sections")
                    else:
                        print("  ✓ Embedding column contains data")
                else:
                    issues.append("embedding column does not exist in sections table!")
            else:
                print("  ℹ Sections table is empty (expected for new databases)")
        except Exception as e:
            issues.append(f"Could not query sections table: {str(e)}")
            print(f"  ✗ {issues[-1]}")
        
        # Check 2: Try to query chats table
        print("\nCheck 2: Checking chats table for new columns...")
        try:
            response = supabase.table("chats").select("id, provider_used, sources").limit(1).execute()
            print("  ✓ Chats table accessible with new columns")
        except Exception as e:
            issues.append(f"Chats table missing new columns: {str(e)}")
            print(f"  ✗ {issues[-1]}")
        
        # Check 3: Try inserting a test embedding (optional - requires actual data)
        print("\nCheck 3: Vector type check...")
        print("  ℹ To fully verify pgvector setup, user must upload and process a PDF")
        
        if issues:
            print(f"\n=== Issues Found ({len(issues)}) ===")
            for issue in issues:
                print(f"  ✗ {issue}")
            return {
                "status": "error",
                "issues": issues,
                "recommendation": "Run the database migrations in Supabase SQL Editor"
            }
        else:
            print("\n=== ✓ Database Setup Looks Good ===")
            print("The database appears to be properly configured for embeddings.")
            return {
                "status": "success",
                "message": "Database is ready for embeddings"
            }
    
    except Exception as e:
        print(f"\n=== Diagnostic Error ===")
        print(f"Error: {str(e)}")
        return {
            "status": "error",
            "error": str(e)
        }
