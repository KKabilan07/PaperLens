"""
Retrieval service for semantic search in paper sections using pgvector
Queries Supabase for contextually relevant sections
"""

from typing import List, Dict
from app.services.supabase_client import get_supabase
from app.services.embeddings_service import embed_text


def search_sections(
    query: str,
    paper_id: str,
    top_k: int = 5,
    threshold: float = 0.1
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
