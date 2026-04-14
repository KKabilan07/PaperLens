"""
RAG (Retrieval Augmented Generation) Pipeline
Combines retrieval + multi-provider LLM generation for contextual answers
"""

from typing import Dict
from app.services.retrieval_service import get_paper_context
from app.services.llm_provider_service import generate_with_fallback
import traceback


def generate_rag_response(
    question: str,
    paper_id: str,
    paper_title: str,
    top_k: int = 5
) -> Dict[str, str]:
    """
    Generate answer using RAG pipeline with multi-provider LLM
    
    Args:
        question: User's question
        paper_id: Paper to search in
        paper_title: Title of the paper (for context in prompt)
        top_k: Number of sections to retrieve
    
    Returns:
        Dict with answer, sources, provider used, and status
    """
    try:
        print(f"\n=== RAG Pipeline Started ===")
        print(f"Question: {question}")
        print(f"Paper ID: {paper_id}")
        
        # Step 1: Retrieve relevant sections
        print(f"Step 1: Retrieving context...")
        context = get_paper_context(question, paper_id, top_k)
        print(f"Context retrieved: {len(context)} chars")
        
        if context.startswith("No relevant") or context.startswith("Error"):
            print(f"No relevant context found")
            return {
                "answer": "Could not find relevant sections in the paper. Try rephrasing your question.",
                "sources": [],
                "provider": None,
                "status": "failed"
            }
        
#         # Step 2: Build RAG prompt
#         print(f"Step 2: Building RAG prompt...")
#         rag_prompt = f"""You are an expert assistant analyzing a research paper.

# Paper Title: {paper_title}

# Based on the following sections from the paper, answer the user's question accurately and concisely.

# PAPER CONTEXT:
# {context}

# USER QUESTION: {question}

# Please provide a clear, accurate answer based only on the information in the paper. 
# If the answer is not in the provided sections, say "This information is not covered in the provided sections of the paper."""

        print("Step 2: Building RAG prompt...")

        rag_prompt = f"""
        You are a highly precise research assistant. Your task is to answer questions strictly based on the provided research paper context.

        ---------------------
        PAPER TITLE:
        {paper_title}
        ---------------------

        PAPER CONTEXT:
        {context}
        ---------------------

        USER QUESTION:
        {question}
        ---------------------

        INSTRUCTIONS:

        1. Answer ONLY using the provided context.
        2. Do NOT use prior knowledge or make assumptions.
        3. If the answer is not explicitly present, respond with:
        "This information is not covered in the provided sections of the paper."
        4. Be concise, clear, and technically accurate.
        5. If applicable, cite relevant phrases or sentences from the context.
        6. Avoid repetition and unnecessary explanation.
        7. If the question requires multiple points, present them in bullet form.

        OUTPUT FORMAT:

        Answer:
        <your answer here>

        (Optional) Supporting Evidence:
        - "<exact or paraphrased snippet from context>"
        """
        
        # Step 3: Generate answer using multi-provider LLM with fallback
        print(f"Step 3: Calling LLM generate_with_fallback...")
        result = generate_with_fallback(rag_prompt)
        print(f"LLM Result: {result}")
        
        final_response = {
            "answer": result.get("answer", "Error generating response"),
            "sources": [paper_title],
            "provider": result.get("provider_used"),
            "status": "success" if result.get("success") else "failed"
        }
        print(f"RAG Pipeline Complete: {final_response}")
        return final_response
    
    except Exception as e:
        error_msg = f"Error generating answer: {str(e)}"
        print(f"\n=== RAG Pipeline Error ===")
        print(error_msg)
        traceback.print_exc()
        return {
            "answer": error_msg,
            "sources": [],
            "provider": None,
            "status": "error"
        }


def compare_papers_rag(
    question: str,
    paper_ids: list,
    paper_titles: dict,  # {paper_id: title}
    top_k: int = 3
) -> Dict:
    """
    Compare papers using RAG - retrieve sections from multiple papers
    Uses multi-provider LLM for comparison
    
    Args:
        question: Comparison question
        paper_ids: List of paper IDs to compare
        paper_titles: Dict mapping paper_id to title
        top_k: Sections per paper
    
    Returns:
        Comparison answer with sources and provider info
    """
    try:
        contexts = {}
        for paper_id in paper_ids:
            title = paper_titles.get(paper_id, f"Paper {paper_id}")
            context = get_paper_context(question, paper_id, top_k)
            contexts[paper_id] = {"title": title, "context": context}
        
        # Build comparison prompt
        context_text = ""
        for paper_id, data in contexts.items():
            context_text += f"\n\n{data['title']}:\n{data['context']}"
        
        comparison_prompt = f"""You are expert at comparing research papers.

Based on the following sections from multiple papers, answer this comparison question:

{context_text}

COMPARISON QUESTION: {question}

Provide a structured comparison highlighting:
1. Similarities
2. Differences
3. How the papers complement each other"""
        
        result = generate_with_fallback(comparison_prompt)
        
        return {
            "answer": result.get("answer", "Error comparing papers"),
            "sources": list(contexts.values()),
            "provider": result.get("provider_used"),
            "status": "success" if result.get("success") else "failed"
        }
    
    except Exception as e:
        return {
            "answer": f"Error comparing papers: {str(e)}",
            "sources": [],
            "provider": None,
            "status": "error"
        }
