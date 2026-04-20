"""
Retrieval service for semantic search in paper sections using pgvector
Queries Supabase for contextually relevant sections
"""

from typing import List, Dict
from app.services.supabase_client import get_supabase
from app.services.embeddings_service import embed_text
from difflib import SequenceMatcher


def search_sections(
    query: str,
    paper_id: str,
    top_k: int = 10,
    threshold: float = 0.05
) -> List[Dict]:
    """
    Search for relevant sections in a paper using semantic similarity
    
    Args:
        query: User's question/query
        paper_id: ID of the paper to search in
        top_k: Number of top results to return
        threshold: Minimum similarity score (0-1)
    
    Returns:
        List of relevant sections with content, metadata, and similarity score
    """
    try:
        print(f"\n[Search] Query: {query}")
        print(f"[Search] Paper ID: {paper_id}")
        
        # Generate embedding for query
        print(f"[Search] Generating query embedding...")
        query_embedding = embed_text(query)
        print(f"[Search] Query embedding generated: {len(query_embedding)} dims")
        
        # Query Supabase pgvector
        print(f"[Search] Calling Supabase RPC: sections_similarity_search...")
        supabase = get_supabase()
        
        # Use pgvector similarity search
        response = supabase.rpc(
            'sections_similarity_search',
            {
                'query_embedding': query_embedding,
                'paper_id_param': paper_id,
                'top_k': top_k,
                'similarity_threshold': threshold
            }
        ).execute()
        
        print(f"[Search] RPC Response: {response}")
        results = response.data if response.data else []
        print(f"[Search] Found {len(results)} sections")
        
        return results
    
    except Exception as e:
        print(f"[Search] Error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise Exception(f"Error searching sections: {str(e)}")


def search_sections_across_papers(
    query: str,
    top_k: int = 10,
    threshold: float = 0.3
) -> List[Dict]:
    """
    Search for relevant sections across ALL papers (for multi-paper analysis)
    
    Args:
        query: User's question/query
        top_k: Number of top results to return
        threshold: Minimum similarity score
    
    Returns:
        List of relevant sections from all papers
    """
    try:
        query_embedding = embed_text(query)
        supabase = get_supabase()
        
        response = supabase.rpc(
            'sections_similarity_search_global',
            {
                'query_embedding': query_embedding,
                'top_k': top_k,
                'similarity_threshold': threshold
            }
        ).execute()
        
        return response.data if response.data else []
    
    except Exception as e:
        raise Exception(f"Error searching sections globally: {str(e)}")


def get_paper_context(
    query: str,
    paper_id: str,
    top_k: int = 5
) -> str:
    """
    Get context from paper sections for RAG pipeline
    Combines retrieved sections into a single context string
    
    Args:
        query: User's question
        paper_id: Paper ID to search
        top_k: Number of sections to retrieve
    
    Returns:
        Formatted context string ready for LLM
    """
    try:
        sections = search_sections(query, paper_id, top_k)
        
        if not sections:
            return "No relevant sections found in the paper."
        
        # Format sections as context
        context_parts = []
        for i, section in enumerate(sections, 1):
            section_name = section.get('section_name', 'Unknown Section')
            content = section.get('content', '')
            similarity = section.get('similarity', 0)
            
            context_parts.append(
                f"[Section {i}: {section_name} (Relevance: {similarity:.2%})]\n{content}"
            )
        
        return "\n\n".join(context_parts)
    
    except Exception as e:
        return f"Error retrieving context: {str(e)}"


def get_all_paper_sections(paper_id: str) -> str:
    """
    Get all unique sections from a paper (for summary/overview queries)
    
    Args:
        paper_id: Paper ID to retrieve sections for
    
    Returns:
        Formatted string with all sections and their content
    """
    try:
        supabase = get_supabase()
        
        # Query all sections from the paper
        response = supabase.table("sections") \
            .select("section_name, content, chunk_index") \
            .eq("paper_id", paper_id) \
            .order("chunk_index", desc=False) \
            .execute()
        
        if not response.data:
            return "No sections found in the paper."
        
        # Group by section name and combine content
        sections_dict = {}
        for record in response.data:
            section_name = record.get('section_name', 'Unknown')
            content = record.get('content', '')
            
            if section_name not in sections_dict:
                sections_dict[section_name] = ""
            sections_dict[section_name] += content + " "
        
        # Format all sections
        context_parts = []
        for section_name, content in sections_dict.items():
            context_parts.append(f"[Section: {section_name}]\n{content.strip()}")
        
        return "\n\n".join(context_parts)
    
    except Exception as e:
        print(f"[Error] get_all_paper_sections: {str(e)}")
        return f"Error retrieving sections: {str(e)}"


def get_paper_section_list(paper_id: str) -> List[str]:
    """
    Get list of all unique section names in a paper
    
    Args:
        paper_id: Paper ID to retrieve section names for
    
    Returns:
        List of unique section names
    """
    try:
        supabase = get_supabase()
        
        response = supabase.table("sections") \
            .select("section_name") \
            .eq("paper_id", paper_id) \
            .execute()
        
        if not response.data:
            return []
        
        # Get unique section names preserving order
        seen = set()
        section_names = []
        for record in response.data:
            section_name = record.get('section_name', '')
            if section_name and section_name not in seen:
                section_names.append(section_name)
                seen.add(section_name)
        
        return section_names
    
    except Exception as e:
        print(f"[Error] get_paper_section_list: {str(e)}")
        return []


def find_matching_section(query: str, paper_id: str, similarity_threshold: float = 0.5) -> str:
    """
    Find section name that matches the query using fuzzy matching
    Dynamically matches against actual section names in the paper
    Works with ANY section naming convention, not hardcoded
    
    Args:
        query: User's question/query
        paper_id: Paper ID
        similarity_threshold: Minimum similarity score (0-1) to consider a match
    
    Returns:
        Section name if found with good match, empty string otherwise
    """
    try:
        sections = get_paper_section_list(paper_id)
        if not sections:
            return ""
        
        query_lower = query.lower()
        best_match = ""
        best_score = 0
        
        # Extract key terms from query (words that might match section names)
        query_words = query_lower.split()
        
        print(f"[Section Match] Query words: {query_words}")
        print(f"[Section Match] Available sections: {sections}")
        
        # For each actual section in the paper
        for section in sections:
            section_lower = section.lower()
            section_words = section_lower.split()
            
            # Calculate similarity between query and section
            # Try matching individual words first (highest priority)
            word_match_score = 0
            for query_word in query_words:
                for section_word in section_words:
                    # If a word in the query matches a word in the section name
                    similarity = SequenceMatcher(None, query_word, section_word).ratio()
                    if similarity > word_match_score:
                        word_match_score = similarity
            
            # Also calculate overall string similarity
            overall_similarity = SequenceMatcher(None, query_lower, section_lower).ratio()
            
            # Prefer word matches, but also consider overall similarity
            final_score = max(word_match_score * 1.2, overall_similarity)  # Word matches get priority
            
            print(f"[Section Match] '{section}' - word_match: {word_match_score:.2f}, overall: {overall_similarity:.2f}, final: {final_score:.2f}")
            
            # Update best match if this is better
            if final_score > best_score:
                best_score = final_score
                best_match = section
        
        # Return match only if similarity is above threshold
        if best_score >= similarity_threshold:
            print(f"[Section Match] MATCHED: '{best_match}' with score {best_score:.2f}")
            return best_match
        else:
            print(f"[Section Match] No good match found (best score: {best_score:.2f}, threshold: {similarity_threshold})")
            return ""
    
    except Exception as e:
        print(f"[Error] find_matching_section: {str(e)}")
        import traceback
        traceback.print_exc()
        return ""


def get_section_by_name(paper_id: str, section_name: str, limit: int = 20) -> str:
    """
    Get all content from a specific section by name
    
    Args:
        paper_id: Paper ID
        section_name: Section name to retrieve
        limit: Max number of chunks to combine
    
    Returns:
        Formatted section content
    """
    try:
        supabase = get_supabase()
        
        # Query all chunks from this specific section
        response = supabase.table("sections") \
            .select("content, chunk_index") \
            .eq("paper_id", paper_id) \
            .eq("section_name", section_name) \
            .order("chunk_index", desc=False) \
            .limit(limit) \
            .execute()
        
        if not response.data:
            return ""
        
        # Combine all chunks
        content_parts = []
        for record in response.data:
            content = record.get('content', '')
            if content:
                content_parts.append(content)
        
        if not content_parts:
            return ""
        
        combined_content = "\n".join(content_parts)
        return f"[Section: {section_name}]\n{combined_content}"
    
    except Exception as e:
        print(f"[Error] get_section_by_name: {str(e)}")
        return ""
