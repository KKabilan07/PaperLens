import os
from typing import Optional
from app.services.llm_provider_service import generate_with_fallback


def generate_explanation(question: str, context: str, paper_title: str) -> str:
    """
    Generate AI response to a question about a paper using multi-provider LLM
    
    Args:
        question: User's question
        context: Relevant sections from the paper
        paper_title: Title of the paper
    
    Returns:
        AI-generated explanation
    """
    try:
        prompt = f"""You are an expert academic assistant. Based on the following context from the paper "{paper_title}", 
        please answer this question clearly and concisely:

        Question: {question}

        Context from the paper:
        {context}

        Provide a detailed and accurate response based on the paper content."""

        result = generate_with_fallback(prompt)
        return result.get("answer", "Error generating explanation")
    
    except Exception as e:
        return f"Error generating explanation: {str(e)}"


def generate_summary(text: str, paper_title: str) -> str:
    """
    Generate a comprehensive summary of the paper using multi-provider LLM
    
    Args:
        text: Full text of the paper
        paper_title: Title of the paper
    
    Returns:
        AI-generated summary of the paper
    """
    try:
        # Limit text to avoid token limits
        text_truncated = text[:8000]
        
        prompt = f"""Please provide a comprehensive but concise summary of the following academic paper titled "{paper_title}".
        
        The summary should include:
        1. Main objectives and research question
        2. Key methodology
        3. Major findings
        4. Conclusions and implications
        
        Paper text:
        {text_truncated}
        
        Provide a well-structured summary."""

        result = generate_with_fallback(prompt)
        return result.get("answer", "Error generating summary")
    
    except Exception as e:
        return f"Error generating summary: {str(e)}"


def compare_papers(paper1_text: str, paper2_text: str, paper1_title: str, paper2_title: str) -> dict:
    """
    Compare two papers using multi-provider LLM
    
    Args:
        paper1_text: Text of first paper
        paper2_text: Text of second paper
        paper1_title: Title of first paper
        paper2_title: Title of second paper
    
    Returns:
        Comparison result with similarities, differences, and common topics
    """
    try:
        # Truncate texts to avoid token limits
        text1_truncated = paper1_text[:5000]
        text2_truncated = paper2_text[:5000]
        
        prompt = f"""Compare these two academic papers and provide a detailed analysis.

        Paper 1: {paper1_title}
        {text1_truncated}

        Paper 2: {paper2_title}
        {text2_truncated}

        Please analyze and provide:
        1. Key similarities in research focus, methodology, or findings
        2. Key differences in approach, conclusions, or scope
        3. Common topics or themes discussed in both papers
        4. How these papers complement or contradict each other

        Format your response as a structured analysis."""

        result = generate_with_fallback(prompt)
        
        return {
            "paper1": paper1_title,
            "paper2": paper2_title,
            "analysis": result.get("answer", "Error comparing papers"),
            "status": "success" if result.get("success") else "error",
            "provider": result.get("provider_used")
        }
    
    except Exception as e:
        return {
            "paper1": paper1_title,
            "paper2": paper2_title,
            "analysis": f"Error comparing papers: {str(e)}",
            "status": "error",
            "provider": None
        }
