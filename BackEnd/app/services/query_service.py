from typing import Dict, List
from llama_index.core import VectorStoreIndex, Document, Settings
from app.services.supabase_client import get_supabase

async def query_paper(question: str, paper_id: str) -> Dict:
    """
    Query a specific paper using an in-memory LlamaIndex VectorStoreIndex.
    Retrieves the paper sections/chunks from Supabase, builds the index,
    and runs the query engine.
    """
    supabase = get_supabase()
    
    # 1. Fetch paper chunks from database
    response = supabase.table("sections") \
        .select("content, section_name, chunk_index, embedding") \
        .eq("paper_id", paper_id) \
        .order("chunk_index", desc=False) \
        .execute()
        
    if not response.data:
        return {
            "answer": "This paper has no sections/chunks loaded in the database. Please re-upload it.",
            "sources": [],
            "provider_used": Settings.llm.metadata.model_name,
            "status": "failed"
        }
        
    # 2. Convert database records to LlamaIndex TextNodes with pre-computed embeddings
    from llama_index.core.schema import TextNode
    import json
    nodes = []
    for record in response.data:
        embedding = record.get("embedding")
        if isinstance(embedding, str):
            try:
                embedding = json.loads(embedding)
            except:
                pass
                
        node = TextNode(
            text=record["content"],
            embedding=embedding,
            metadata={
                "section_name": record.get("section_name", "Content"),
                "chunk_index": record.get("chunk_index", 0)
            }
        )
        nodes.append(node)
        
    # 3. Create an in-memory VectorStoreIndex from these nodes
    index = VectorStoreIndex(nodes)
    
    # Determine if the query is asking for a summary
    question_lower = question.lower()
    is_summary_query = any(kw in question_lower for kw in ["summarize", "summary", "overview", "key points", "main findings"])
    
    # 4. Create Query Engine with appropriate settings
    if is_summary_query:
        query_engine = index.as_query_engine(
            similarity_top_k=min(15, len(nodes)),
            response_mode="tree_summarize"
        )
    else:
        query_engine = index.as_query_engine(
            similarity_top_k=5,
            response_mode="compact"
        )
        
    # 5. Execute query
    response_obj = await query_engine.aquery(question)
    
    # 6. Extract source nodes for citation
    sources = []
    if response_obj.source_nodes:
        for node in response_obj.source_nodes:
            section_name = node.metadata.get("section_name", "Content")
            # Avoid duplicating source section names in list
            if section_name not in sources:
                sources.append(section_name)
                
    return {
        "success": True,
        "answer": str(response_obj),
        "provider_used": Settings.llm.metadata.model_name,
        "sources": sources,
        "status": "success"
    }