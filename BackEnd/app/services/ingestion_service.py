import os
import tempfile
from datetime import datetime
import uuid
from typing import Dict
from llama_index.core import Document, Settings
from llama_index.core.node_parser import SentenceSplitter
from app.services.supabase_client import get_supabase
from app.core.config import LLAMA_PARSE_KEY

async def ingest_paper(
    pdf_bytes: bytes,
    file_name: str,
    user_id: str,
    title: str = None
) -> Dict:
    """
    Ingest a PDF paper using LlamaIndex:
    1. Parse PDF using LlamaParse (if key present) or standard PDFReader
    2. Save paper record to Supabase
    3. Chunk content using SentenceSplitter
    4. Generate 768-dimensional embeddings using Gemini's embedding-001 model
    5. Save chunks to 'sections' table
    """
    supabase = get_supabase()
    paper_id = str(uuid.uuid4())
    
    # Save PDF to a temp file for loaders/parsers
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_pdf:
        temp_pdf.write(pdf_bytes)
        temp_pdf_path = temp_pdf.name
        
    try:
        documents = []
        # Try LlamaParse first if key is present
        if LLAMA_PARSE_KEY:
            try:
                from llama_parse import LlamaParse
                parser = LlamaParse(
                    api_key=LLAMA_PARSE_KEY,
                    result_type="text"
                )
                documents = await parser.aload_data(temp_pdf_path)
            except Exception as pe:
                print(f"LlamaParse error, falling back to PDFReader: {str(pe)}")
                
        # Fallback to standard PDFReader
        if not documents:
            from llama_index.readers.file import PDFReader
            reader = PDFReader()
            documents = reader.load_data(temp_pdf_path)
            
        # Get page and word counts
        page_count = len(documents)
        total_text = " ".join([doc.text for doc in documents])
        word_count = len(total_text.split())
        
        # Determine paper title
        paper_title = title or file_name
        
        # 2. Insert Paper record
        paper_data = {
            "id": paper_id,
            "user_id": user_id,
            "title": paper_title,
            "description": file_name,
            "word_count": word_count,
            "page_count": page_count,
            "file_path": f"papers/{user_id}/{paper_id}/{file_name}",
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }
        supabase.table("papers").insert(paper_data).execute()
        
        # 3. Chunk the documents
        splitter = SentenceSplitter(chunk_size=500, chunk_overlap=100)
        nodes = splitter.get_nodes_from_documents(documents)
        
        # 4. Generate embeddings & prepare records for insertion
        records_to_insert = []
        for idx, node in enumerate(nodes):
            # Generate embedding using global LlamaIndex Settings (Gemini embedding-001)
            embedding = Settings.embed_model.get_text_embedding(node.text)
            
            # Determine a section name
            section_name = node.metadata.get("section_name", "Content")
            if section_name == "Content":
                if idx < len(nodes) * 0.1:
                    section_name = "Abstract/Introduction"
                elif idx > len(nodes) * 0.9:
                    section_name = "Conclusion"
            
            records_to_insert.append({
                "paper_id": paper_id,
                "section_name": section_name,
                "content": node.text,
                "embedding": embedding,
                "chunk_index": idx
            })
            
        # 5. Insert sections
        if records_to_insert:
            supabase.table("sections").insert(records_to_insert).execute()
            
        # 6. Upload PDF file to Supabase storage
        file_path = f"{user_id}/{paper_id}/{file_name}"
        try:
            supabase.storage.from_("papers").upload(file_path, pdf_bytes)
        except Exception as se:
            print(f"Non-critical: Error uploading to Supabase storage: {str(se)}")
            
        return {
            "success": True,
            "paper_id": paper_id,
            "title": paper_title,
            "sections_count": len(records_to_insert),
            "word_count": word_count,
            "message": f"Paper '{paper_title}' processed and ingested successfully using LlamaIndex with Gemini embedding-001."
        }
        
    finally:
        if os.path.exists(temp_pdf_path):
            os.remove(temp_pdf_path)