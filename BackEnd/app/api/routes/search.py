from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import HTTPBearer
from app.services.supabase_client import get_supabase
from app.utils.security import get_current_user
from llama_index.core import VectorStoreIndex, Settings
from llama_index.core.schema import TextNode
import json

router = APIRouter()
security = HTTPBearer()

@router.get("/semantic-search")
async def semantic_search(
    query: str = Query(..., min_length=1),
    credentials = Depends(security)
):
    """
    Perform semantic search across all papers uploaded by the current user
    """
    try:
        user = get_current_user(credentials)
        user_id = user["user_id"]
        supabase = get_supabase()
        
        # 1. Fetch user's papers
        papers_response = supabase.table("papers").select("id, title").eq("user_id", user_id).execute()
        papers = papers_response.data
        if not papers:
            return []
            
        paper_ids = [p["id"] for p in papers]
        paper_title_map = {p["id"]: p["title"] for p in papers}
        
        # 2. Fetch sections for all user papers
        # Limit total sections fetched to prevent memory issues for massive accounts (e.g. 500 max)
        sections_response = supabase.table("sections") \
            .select("paper_id, section_name, content, chunk_index, embedding") \
            .in_("paper_id", paper_ids) \
            .execute()
            
        sections = sections_response.data
        if not sections:
            return []
            
        # 3. Build in-memory VectorStoreIndex
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
                    "paper_title": paper_title_map.get(s["paper_id"], "Unknown Paper"),
                    "section_name": s.get("section_name", "Content"),
                    "chunk_index": s.get("chunk_index", 0)
                }
            )
            nodes.append(node)
            
        index = VectorStoreIndex(nodes)
        retriever = index.as_retriever(similarity_top_k=8)
        
        # 4. Perform retrieval
        nodes_with_score = retriever.retrieve(query)
        
        # 5. Build response
        results = []
        for nws in nodes_with_score:
            node = nws.node
            score = float(nws.score) if nws.score is not None else 0.0
            
            results.append({
                "paper_id": node.metadata.get("paper_id"),
                "paper_title": node.metadata.get("paper_title"),
                "section_name": node.metadata.get("section_name"),
                "chunk_index": node.metadata.get("chunk_index"),
                "content": node.text,
                "score": score
            })
            
        return results
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error performing semantic search: {str(e)}"
        )
