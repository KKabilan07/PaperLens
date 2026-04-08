"""
Embeddings service for generating vector representations of text
Uses sentence-transformers for local embedding generation (free, no API calls)
"""

from typing import List
import numpy as np

try:
    from sentence_transformers import SentenceTransformer
    EMBEDDINGS_AVAILABLE = True
except ImportError:
    EMBEDDINGS_AVAILABLE = False

# Model: 384-dimensional embeddings, good balance of speed and quality
MODEL_NAME = "all-MiniLM-L6-v2"
model_instance = None


def _get_model():
    """Lazy load the embedding model"""
    global model_instance
    if model_instance is None:
        if not EMBEDDINGS_AVAILABLE:
            raise ImportError(
                "sentence-transformers not installed. "
                "Install with: pip install sentence-transformers"
            )
        model_instance = SentenceTransformer(MODEL_NAME)
    return model_instance


def embed_text(text: str) -> List[float]:
    """
    Generate embedding for a single text
    
    Args:
        text: Text to embed
    
    Returns:
        List of floats (384 dimensions)
    """
    try:
        model = _get_model()
        embedding = model.encode(text, convert_to_tensor=False)
        return embedding.tolist()
    except Exception as e:
        raise Exception(f"Error generating embedding: {str(e)}")


def embed_texts(texts: List[str]) -> List[List[float]]:
    """
    Generate embeddings for multiple texts (batch processing - faster)
    
    Args:
        texts: List of texts to embed
    
    Returns:
        List of embedding lists
    """
    try:
        model = _get_model()
        embeddings = model.encode(texts, convert_to_tensor=False)
        return embeddings.tolist()
    except Exception as e:
        raise Exception(f"Error generating embeddings: {str(e)}")


def get_embedding_dimension() -> int:
    """Get the dimension of embeddings (384 for all-MiniLM-L6-v2)"""
    return 384
