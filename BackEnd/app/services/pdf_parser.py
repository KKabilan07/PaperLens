import PyPDF2
import io
from typing import Dict, List, Optional
import re


def extract_text_from_pdf(pdf_bytes: bytes) -> Dict:
    """
    Extract text and metadata from PDF bytes
    
    Returns:
        Dict with keys: text, num_pages, metadata
    """
    try:
        pdf_file = io.BytesIO(pdf_bytes)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        
        num_pages = len(pdf_reader.pages)
        text = ""
        
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        
        metadata = pdf_reader.metadata or {}
        
        return {
            "text": text,
            "num_pages": num_pages,
            "metadata": {
                "title": metadata.get("/Title", ""),
                "author": metadata.get("/Author", ""),
                "subject": metadata.get("/Subject", ""),
                "creator": metadata.get("/Creator", ""),
            },
            "word_count": len(text.split())
        }
    except Exception as e:
        raise Exception(f"Error parsing PDF: {str(e)}")


def extract_sections_from_text(text: str, max_section_length: int = 1000) -> List[Dict]:
    """
    Extract sections from PDF text using simple heuristics
    
    Args:
        text: Raw text from PDF
        max_section_length: Maximum characters per section
    
    Returns:
        List of section dicts with: section_name, content, page_numbers
    """
    sections = []
    
    # Split by common section patterns
    lines = text.split("\n")
    
    current_section = {
        "section_name": "Introduction",
        "content": "",
        "page_numbers": [],
        "start_line": 0
    }
    
    for i, line in enumerate(lines):
        line_stripped = line.strip()
        
        # Detect section headers (all caps, numbered, or common patterns)
        is_header = (
            (line_stripped.isupper() and len(line_stripped) > 3) or
            re.match(r"^[\d]+\.\s+", line_stripped) or
            re.match(r"^(Abstract|Introduction|Method|Results?|Discussion|Conclusion|References)", line_stripped, re.I)
        )
        
        if is_header and len(current_section["content"]) > 0:
            # Save previous section
            if current_section["content"].strip():
                sections.append({
                    "section_name": current_section["section_name"],
                    "content": current_section["content"].strip(),
                    "page_numbers": current_section["page_numbers"]
                })
            
            # Start new section
            current_section = {
                "section_name": line_stripped[:100],  # Limit name length
                "content": "",
                "page_numbers": [],
                "start_line": i
            }
        else:
            current_section["content"] += line + "\n"
            
            # Split large sections
            if len(current_section["content"]) > max_section_length:
                if current_section["content"].strip():
                    sections.append({
                        "section_name": current_section["section_name"],
                        "content": current_section["content"].strip(),
                        "page_numbers": current_section["page_numbers"]
                    })
                current_section = {
                    "section_name": f"{current_section['section_name']} (cont.)",
                    "content": "",
                    "page_numbers": [],
                    "start_line": i
                }
    
    # Add final section
    if current_section["content"].strip():
        sections.append({
            "section_name": current_section["section_name"],
            "content": current_section["content"].strip(),
            "page_numbers": current_section["page_numbers"]
        })
    
    return sections if sections else [
        {
            "section_name": "Full Text",
            "content": text.strip(),
            "page_numbers": list(range(1, int(text.count('\n') / 50) + 1))
        }
    ]


def parse_pdf(pdf_bytes: bytes) -> Dict:
    """
    Complete PDF parsing pipeline
    
    Returns:
        Dict with: text, num_pages, word_count, metadata, sections
    """
    # Extract raw text
    extraction_result = extract_text_from_pdf(pdf_bytes)
    
    # Extract sections
    sections = extract_sections_from_text(extraction_result["text"])
    
    return {
        "text": extraction_result["text"],
        "num_pages": extraction_result["num_pages"],
        "word_count": extraction_result["word_count"],
        "metadata": extraction_result["metadata"],
        "sections": sections
    }
