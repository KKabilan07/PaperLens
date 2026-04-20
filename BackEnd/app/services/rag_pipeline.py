"""
RAG (Retrieval Augmented Generation) Pipeline
Combines retrieval + multi-provider LLM generation for contextual answers
Intelligently routes queries based on type: summary, list sections, specific topic, or general
"""

from typing import Dict
from app.services.retrieval_service import (
    get_paper_context, 
    get_all_paper_sections,
    get_paper_section_list,
    find_matching_section,
    get_section_by_name
)
from app.services.llm_provider_service import generate_with_fallback
import traceback
import re


def classify_query_type(question: str) -> str:
    """
    Classify the type of query to route to appropriate handler
    
    Returns: 'summary', 'list_sections', 'specific_section', or 'general'
    """
    question_lower = question.lower().strip()
    
    # Summary queries
    summary_keywords = [
        r'\bsummarize\b', r'\bsummary\b', r'\boverall\b', 
        r'\bwhat is the paper\b', r'\bpaper overview\b',
        r'\btell me about the paper\b', r'\bwhat does the paper\b',
        r'\bkey points\b', r'\bmain findings\b', r'\bwhole paper\b'
    ]
    
    for keyword in summary_keywords:
        if re.search(keyword, question_lower):
            return 'summary'
    
    # List sections queries
    list_keywords = [
        r'\blist.*sections\b', r'\bwhat sections\b', r'\bshow.*sections\b',
        r'\bget.*sections\b', r'\btable of contents\b', r'\bchapters\b',
        r'\ball sections\b', r'\bavailable sections\b'
    ]
    
    for keyword in list_keywords:
        if re.search(keyword, question_lower):
            return 'list_sections'
    
    # Specific section queries
    section_keywords = [
        r'\bintroduction\b', r'\babstract\b', r'\bconclusion\b',
        r'\bmethod\b', r'\bresults\b', r'\bdiscussion\b',
        r'\brelated work\b', r'\breferences\b', r'\bappendix\b'
    ]
    
    for keyword in section_keywords:
        if re.search(keyword, question_lower):
            return 'specific_section'
    
    return 'general'


def generate_rag_response(
    question: str,
    paper_id: str,
    paper_title: str,
    top_k: int = 5
) -> Dict[str, str]:
    """
    Generate answer using RAG pipeline with multi-provider LLM
    Intelligently routes queries based on type
    
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
        
        # Classify the query type
        query_type = classify_query_type(question)
        print(f"Query Type: {query_type}")
        
        # Step 1: Retrieve context based on query type
        print(f"Step 1: Retrieving context ({query_type} mode)...")
        
        if query_type == 'summary':
            # Get all sections for summary
            context = get_all_paper_sections(paper_id)
            rag_prompt = f"""
        You are a research paper summarization expert. Provide a comprehensive summary of the paper.

        ---------------------
        PAPER TITLE:
        {paper_title}
        ---------------------

        PAPER CONTENT:
        {context}
        ---------------------

        USER QUESTION:
        {question}
        ---------------------

        INSTRUCTIONS:
        1. Provide a comprehensive overview of the entire paper
        2. Include key sections, main findings, and contributions
        3. Be clear and well-structured
        4. Organize by major sections if applicable
        5. Highlight the most important information

        OUTPUT FORMAT:
        Answer:
        <comprehensive summary here>
        """
        
        elif query_type == 'list_sections':
            # Get all section names
            sections = get_paper_section_list(paper_id)
            if not sections:
                return {
                    "answer": "No sections found in the paper.",
                    "sources": [paper_title],
                    "provider": None,
                    "status": "failed"
                }
            
            sections_text = "\n".join([f"- {s}" for s in sections])
            rag_prompt = f"""
        You are a helpful assistant. The user is asking for a list of sections in the paper.

        PAPER TITLE:
        {paper_title}

        AVAILABLE SECTIONS:
        {sections_text}

        USER QUESTION:
        {question}

        INSTRUCTIONS:
        1. List all available sections in the paper
        2. Be clear and organized
        3. You can briefly describe what each section covers if relevant

        OUTPUT FORMAT:
        Answer:
        <list of sections with brief descriptions>
        """
        
        elif query_type == 'specific_section':
            # First try to find matching section by name
            print(f"Step 1.1: Trying to find matching section by name...")
            matching_section = find_matching_section(question, paper_id)
            
            if matching_section:
                print(f"Step 1.2: Found matching section: {matching_section}")
                context = get_section_by_name(paper_id, matching_section)
            else:
                print(f"Step 1.2: No direct section match, using semantic search...")
                # Fall back to semantic search if no direct match
                context = get_paper_context(question, paper_id, top_k=15)
            
            if not context or context.startswith("No relevant") or context.startswith("Error"):
                return {
                    "answer": "Could not find the requested section in the paper. Try asking about: Introduction, Abstract, Results, Discussion, or Methodology.",
                    "sources": [paper_title],
                    "provider": None,
                    "status": "failed"
                }
            
            rag_prompt = f"""
        You are a research paper expert answering specific questions about paper sections.

        ---------------------
        PAPER TITLE:
        {paper_title}
        ---------------------

        SECTION CONTENT:
        {context}
        ---------------------

        USER QUESTION:
        {question}
        ---------------------

        INSTRUCTIONS:
        1. Answer using ONLY the provided section content
        2. Be specific and detailed
        3. Provide a comprehensive overview of the section
        4. Include key points, findings, or information from the section
        5. If the section is present, provide its full content summary
        6. Avoid saying "not covered" if the section content is provided above

        OUTPUT FORMAT:
        Answer:
        <your detailed answer about the section>
        """
        
        else:  # general
            # Standard retrieval for general questions
            context = get_paper_context(question, paper_id, top_k)
            if context.startswith("No relevant") or context.startswith("Error"):
                return {
                    "answer": "Could not find relevant sections in the paper. Try rephrasing your question.",
                    "sources": [],
                    "provider": None,
                    "status": "failed"
                }
            
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
        
        print(f"Context retrieved: {len(context)} chars")
        
        # Step 2: Generate answer using multi-provider LLM with fallback
        print(f"Step 2: Calling LLM generate_with_fallback...")
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
