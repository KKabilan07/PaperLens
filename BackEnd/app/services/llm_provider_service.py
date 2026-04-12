"""
Multi-provider LLM service with automatic fallback
Tries providers in order: Gemini → Claude → Groq
Handles rate limits and errors gracefully
"""

import os
from typing import Optional, Dict
import anthropic
import google.generativeai as genai

# Initialize providers
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

PROVIDERS = {
    "gemini": {
        "key": os.getenv("GEMINI_API_KEY"),
        "available": bool(os.getenv("GEMINI_API_KEY"))
    },
    "claude": {
        "key": os.getenv("CLAUDE_API_KEY"),
        "available": bool(os.getenv("CLAUDE_API_KEY"))
    },
    "groq": {
        "key": os.getenv("GROQ_API_KEY"),
        "available": bool(os.getenv("GROQ_API_KEY"))
    }
}

# Try to import optional providers
try:
    import groq
    HAS_GROQ = True
except ImportError:
    HAS_GROQ = False


def _call_gemini(prompt: str) -> Optional[str]:
    """Call Gemini with fallback model discovery"""
    try:
        print(f"[Gemini] Starting...")
        # Discover available model
        models = genai.list_models()
        model_name = None
        
        for model in models:
            if 'generateContent' in model.supported_generation_methods:
                model_name = model.name.replace('models/', '')
                print(f"[Gemini] Found model: {model_name}")
                break
        
        if not model_name:
            print(f"[Gemini] No suitable model found")
            return None
        
        model = genai.GenerativeModel(model_name)
        print(f"[Gemini] Generating content...")
        response = model.generate_content(prompt)
        print(f"[Gemini] Success!")
        return response.text
    
    except Exception as e:
        print(f"[Gemini] Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


def _call_claude(prompt: str) -> Optional[str]:
    """Call Claude API"""
    try:
        api_key = os.getenv("CLAUDE_API_KEY")
        if not api_key:
            return None
        
        client = anthropic.Anthropic(api_key=api_key)
        
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",  # Latest Claude model
            max_tokens=2048,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        return message.content[0].text
    
    except anthropic.RateLimitError as e:
        print(f"Claude rate limited: {str(e)}")
        return None
    except Exception as e:
        print(f"Claude error: {str(e)}")
        return None


def _call_groq(prompt: str) -> Optional[str]:
    """Call Groq API"""
    try:
        if not HAS_GROQ:
            return None
        
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            return None
        
        client = groq.Groq(api_key=api_key)
        
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant analyzing research papers. Provide clear, accurate, and concise answers."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="mixtral-8x7b-32768",  # Groq's fast model
            temperature=0.7,
            max_tokens=2048,
        )
        
        return chat_completion.choices[0].message.content
    
    except Exception as e:
        print(f"Groq error: {str(e)}")
        return None


def generate_with_fallback(
    prompt: str,
    provider_order: list = None
) -> Dict[str, any]:
    """
    Generate content using multiple providers with fallback
    
    Args:
        prompt: Text prompt to send to LLM
        provider_order: Order to try providers (default: ["gemini", "claude", "groq"])
    
    Returns:
        Dict with:
        - success: bool
        - answer: str (generated text or error message)
        - provider_used: str (which provider succeeded)
        - timestamp: datetime
    """
    from datetime import datetime
    
    if provider_order is None:
        provider_order = ["gemini", "claude", "groq"]
    
    print(f"\n=== LLM Provider Fallback ===")
    print(f"Providers available: {[p for p in provider_order if PROVIDERS[p]['available']]}")
    
    # Try each provider in order
    for provider_name in provider_order:
        if not PROVIDERS[provider_name]["available"]:
            print(f"⊘ {provider_name}: API key not configured")
            continue
        
        print(f"\n→ Trying {provider_name}...")
        
        if provider_name == "gemini":
            answer = _call_gemini(prompt)
        elif provider_name == "claude":
            print(f"[Claude] Starting...")
            answer = _call_claude(prompt)
        elif provider_name == "groq":
            print(f"[Groq] Starting...")
            answer = _call_groq(prompt)
        else:
            answer = None
        
        if answer:
            result = {
                "success": True,
                "answer": answer,
                "provider_used": provider_name,
                "timestamp": datetime.now().isoformat()
            }
            print(f"✓ {provider_name} succeeded! Answer length: {len(answer)} chars")
            return result
        else:
            print(f"✗ {provider_name} returned None")
    
    # All providers failed
    print(f"\n✗ All LLM providers failed")
    return {
        "success": False,
        "answer": "Error: All LLM providers failed. Please check API keys and rate limits.",
        "provider_used": None,
        "timestamp": datetime.now().isoformat()
    }


def get_available_providers() -> Dict:
    """Get information about available providers"""
    return {
        "gemini": PROVIDERS["gemini"]["available"],
        "claude": PROVIDERS["claude"]["available"],
        "groq": PROVIDERS["groq"]["available"] and HAS_GROQ,
        "total_available": sum([
            PROVIDERS["gemini"]["available"],
            PROVIDERS["claude"]["available"],
            PROVIDERS["groq"]["available"] and HAS_GROQ
        ])
    }


def test_providers() -> Dict:
    """Test all configured providers"""
    test_prompt = "Say 'Hello' in one word."
    results = {}
    
    for provider_name in ["gemini", "claude", "groq"]:
        if not PROVIDERS[provider_name]["available"]:
            results[provider_name] = {"status": "not_configured"}
            continue
        
        try:
            if provider_name == "gemini":
                answer = _call_gemini(test_prompt)
            elif provider_name == "claude":
                answer = _call_claude(test_prompt)
            elif provider_name == "groq":
                answer = _call_groq(test_prompt)
            else:
                answer = None
            
            results[provider_name] = {
                "status": "success" if answer else "failed",
                "response": answer[:50] if answer else None
            }
        except Exception as e:
            results[provider_name] = {
                "status": "error",
                "error": str(e)
            }
    
    return results
