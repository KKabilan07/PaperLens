from typing import List


def summarize_text(text: str, num_sentences: int = 5) -> str:
    """
    Generate extractive summary of text
    
    Args:
        text: Input text to summarize
        num_sentences: Number of sentences in summary
    
    Returns:
        Summary text
    """
    sentences = [s.strip() for s in text.split('.') if s.strip()]
    
    if len(sentences) <= num_sentences:
        return '. '.join(sentences) + '.'
    
    # Simple extractive summarization - take first and important sentences
    summary_sentences = []
    summary_sentences.append(sentences[0])  # First sentence
    
    for i in range(1, len(sentences)):
        if len(summary_sentences) < num_sentences:
            # Take roughly evenly spaced sentences
            if i % (len(sentences) // num_sentences) == 0:
                summary_sentences.append(sentences[i])
    
    return '. '.join(summary_sentences) + '.'


def extract_key_points(text: str, num_points: int = 5) -> List[str]:
    """
    Extract key points from text
    
    Args:
        text: Input text
        num_points: Number of key points to extract
    
    Returns:
        List of key point strings
    """
    sentences = [s.strip() for s in text.split('.') if s.strip()]
    
    # Simple heuristic: longer sentences often contain more information
    sentences_with_length = [(s, len(s.split())) for s in sentences]
    sentences_with_length.sort(key=lambda x: x[1], reverse=True)
    
    key_points = [s[0] for s in sentences_with_length[:num_points]]
    
    return key_points
