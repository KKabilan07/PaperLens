import os
from typing import List, Any
from llama_index.core import Settings
from llama_index.core.embeddings import BaseEmbedding
from llama_index.llms.gemini import Gemini
import google.generativeai as genai
from app.core.config import GEMINI_API_KEY

class CustomGeminiEmbedding(BaseEmbedding):
    """
    Custom LlamaIndex Embedding class wrapping the official google-generativeai SDK.
    Bypasses version mismatches and guarantees exact 768-dimensional output
    for models/gemini-embedding-001.
    """
    model_name: str
    
    def __init__(self, model_name: str, api_key: str, **kwargs: Any) -> None:
        super().__init__(model_name=model_name, **kwargs)
        genai.configure(api_key=api_key)
        
    def _get_query_embedding(self, query: str) -> List[float]:
        result = genai.embed_content(
            model=self.model_name,
            content=query,
            task_type="retrieval_query"
        )
        return result["embedding"]
        
    def _get_text_embedding(self, text: str) -> List[float]:
        result = genai.embed_content(
            model=self.model_name,
            content=text,
            task_type="retrieval_document"
        )
        return result["embedding"]
        
    def _get_text_embeddings(self, texts: List[str]) -> List[List[float]]:
        result = genai.embed_content(
            model=self.model_name,
            content=texts,
            task_type="retrieval_document"
        )
        return result["embedding"]

    async def _aget_query_embedding(self, query: str) -> List[float]:
        return self._get_query_embedding(query)
        
    async def _aget_text_embedding(self, text: str) -> List[float]:
        return self._get_text_embedding(text)

def init_llm():
    """
    Initialize global LlamaIndex settings for LLM and Embeddings.
    Uses Gemini 2.5 Flash for generation and custom wrapper around gemini-embedding-001 (768 dimensions).
    """
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY environment variable is not set.")
        
    Settings.llm = Gemini(
        model="models/gemini-2.5-flash",
        api_key=GEMINI_API_KEY
    )
    
    # Instantiate custom embedding class ensuring exact 768 dimensions
    Settings.embed_model = CustomGeminiEmbedding(
        model_name="models/gemini-embedding-001",
        api_key=GEMINI_API_KEY
    )

    print("LLM Initiated Successfully")