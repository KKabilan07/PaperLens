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
        
        # Clean up extracted text - remove common PDF artifacts
        text = _clean_pdf_text(text)
        
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


def _clean_pdf_text(text: str) -> str:
    """
    Clean up PDF-extracted text by removing common artifacts
    """
    lines = text.split("\n")
    cleaned_lines = []
    
    for line in lines:
        stripped = line.strip()
        
        # Skip common PDF header/footer patterns
        if stripped and not any([
            # Email addresses and URLs (common in headers/footers)
            re.match(r"^\S+@\S+\.\S+$", stripped),
            # Page numbers and metadata
            re.match(r"^(Page \d+|pp\. \d+|\d+\s*$)", stripped),
            # Common footer text
            re.match(r"^(www\.|http|doi:|Available online)", stripped, re.I),
            # Received/Accepted dates in metadata format
            re.match(r"^(Received|Accepted|Available online|Published)\s+", stripped, re.I),
            # Journal name patterns (single line, all caps or title case)
            (stripped.isupper() and 8 < len(stripped) < 100 and re.match(r"^[A-Z\s&-]+$", stripped) and stripped.count(" ") <= 3),
            # Author affiliation patterns (numbers with superscripts or letters followed by keywords)
            re.match(r"^[a-z]+(Department|Faculty|University|Institute)", stripped, re.I),
        ]):
            cleaned_lines.append(line)
    
    # Join lines and normalize whitespace
    cleaned_text = "\n".join(cleaned_lines)
    
    # Remove multiple consecutive newlines (keep max 2)
    cleaned_text = re.sub(r"\n\n\n+", "\n\n", cleaned_text)
    
    return cleaned_text


def extract_sections_from_text(text: str, max_section_length: int = 5000) -> List[Dict]:
    """
    Extract sections from PDF text using improved heuristics
    
    Args:
        text: Raw text from PDF
        max_section_length: Maximum characters per section before splitting (for very large sections)
    
    Returns:
        List of section dicts with: section_name, content, page_numbers
    """
    sections = []
    lines = text.split("\n")
    
    current_section = {
        "section_name": "Start",
        "content": "",
        "page_numbers": [],
    }
    
    def is_section_header(line: str) -> bool:
        """
        Detect if a line is likely a section header
        """
        line_stripped = line.strip()
        
        # Skip empty lines and very short lines
        if len(line_stripped) < 2:
            return False
        
        # Pattern 1: Numbered sections like "1.", "1.1", "2. Section Name"
        if re.match(r"^[\d]+(\.\d+)*\.\s+\w", line_stripped):
            return True
        
        # Pattern 2: Common academic paper sections (including variations)
        academic_sections = r"^(abstract|introduction|related\s+work|literature\s+review|method|methodology|approach|results|findings|discussion|conclusion|conclusions|references|acknowledgment|acknowledgements|appendix|future\s+work|keywords)"
        if re.match(academic_sections, line_stripped, re.IGNORECASE):
            return True
        
        # Pattern 3: ALL CAPS headers (but not too long, usually < 80 chars)
        # Also require at least 4 characters and not all digits
        if (line_stripped.isupper() and 
            len(line_stripped) > 3 and 
            len(line_stripped) < 80 and
            line_stripped.count(" ") <= 5 and
            not line_stripped.replace(" ", "").isdigit()):
            return True
        
        # Pattern 4: Short lines that end with a colon and contain multiple capital letters
        # (but not if it looks like author names or affiliations)
        if (line_stripped.endswith(":") and 
            len(line_stripped) < 60 and 
            sum(1 for c in line_stripped if c.isupper()) >= 2 and
            not re.match(r"^[A-Z][\w\s]*[,.]?\s*$", line_stripped)):  # Exclude author-like lines
            return True
        
        return False
    
    for i, line in enumerate(lines):
        # Check if this line is a header
        if is_section_header(line):
            # Save previous section if it has content
            if current_section["content"].strip():
                sections.append({
                    "section_name": current_section["section_name"],
                    "content": current_section["content"].strip(),
                    "page_numbers": current_section["page_numbers"]
                })
            
            # Start new section
            current_section = {
                "section_name": line.strip()[:100],
                "content": "",
                "page_numbers": [],
            }
        else:
            # Add content to current section
            current_section["content"] += line + "\n"
            
            # If section gets too large, split it into continuation
            if len(current_section["content"]) > max_section_length:
                # Save current large section
                sections.append({
                    "section_name": current_section["section_name"],
                    "content": current_section["content"].strip(),
                    "page_numbers": current_section["page_numbers"]
                })
                
                # Start continuation
                current_section = {
                    "section_name": f"{current_section['section_name']} (cont.)",
                    "content": "",
                    "page_numbers": [],
                }
    
    # Add final section
    if current_section["content"].strip():
        sections.append({
            "section_name": current_section["section_name"],
            "content": current_section["content"].strip(),
            "page_numbers": current_section["page_numbers"]
        })
    
    # If no sections were detected, return the whole text as one section
    if not sections:
        return [
            {
                "section_name": "Full Text",
                "content": text.strip(),
                "page_numbers": []
            }
        ]
    
    return sections


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
