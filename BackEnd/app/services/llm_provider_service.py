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
    """Call Gemini with fallback model discovery and retry logic"""
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
        error_str = str(e)
        # Handle rate limits gracefully
        if "high demand" in error_str.lower() or "503" in error_str:
            print(f"[Gemini] Error: Service temporarily unavailable - {error_str}")
        else:
            print(f"[Gemini] Error: {error_str}")
        import traceback
        traceback.print_exc()
        return None


def _call_claude(prompt: str) -> Optional[str]:
    """Call Claude API"""
    try:
        api_key = os.getenv("CLAUDE_API_KEY")
        if not api_key:
            print("[Claude] No API key found")
            return None
        
        print("[Claude] Starting...")
        client = anthropic.Anthropic(api_key=api_key)
        print("[Claude] Client created successfully")
        
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",  # Latest Claude model
            max_tokens=2048,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        print("[Claude] Success!")
        return message.content[0].text
    
    except anthropic.RateLimitError as e:
        print(f"[Claude] Rate limited: {str(e)}")
        return None
    except AttributeError as e:
        print(f"[Claude] API Error (outdated library?): {str(e)}")
        print("[Claude] Please update: pip install --upgrade anthropic")
        return None
    except Exception as e:
        print(f"[Claude] Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


def _call_groq(prompt: str) -> Optional[str]:
    """Call Groq API with fallback models"""
    try:
        if not HAS_GROQ:
            return None
        
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            print("[Groq] No API key found")
            return None
        
        print("[Groq] Starting...")
        client = groq.Groq(api_key=api_key)
        
        # Try multiple models in case one is decommissioned
        models_to_try = [
            "llama-3.2-90b-text-preview",  # Primary (newer)
            "mixtral-8x7b-32768",           # Fallback
            "llama2-70b-4096",              # Second fallback
        ]
        
        for model_name in models_to_try:
            try:
                print(f"[Groq] Trying model: {model_name}")
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
                    model=model_name,
                    temperature=0.7,
                    max_tokens=2048,
                )
                
                print(f"[Groq] Success with {model_name}!")
                return chat_completion.choices[0].message.content
            except Exception as model_error:
                if "decommissioned" in str(model_error).lower():
                    print(f"[Groq] Model {model_name} decommissioned, trying next...")
                    continue
                else:
                    raise model_error
        
        print("[Groq] All models failed")
        return None
    
    except Exception as e:
        print(f"[Groq] Error: {str(e)}")
        import traceback
        traceback.print_exc()
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
            answer = _call_claude(prompt)
        elif provider_name == "groq":
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
    error_message = """❌ Error: All LLM providers failed. 

**What to do:**

1. **Gemini API** (Free tier: 20 req/day)
   - ⏳ Wait for quota to reset (usually next day)
   - 💳 Or upgrade to paid plan: https://ai.google.dev/gemini-api/

2. **Claude API** (Requires credits)
   - 💳 Add credits: https://console.anthropic.com/account/billing/overview
   - Minimum $5 to start

3. **Groq API** (FREE & FAST - Recommended!)
   - ✅ Get free API key: https://console.groq.com
   - Add to .env: GROQ_API_KEY=your_key_here
   - Free tier is very generous

**Quick Fix:** Get a Groq API key (it's free!) and add to your .env file.
Then restart the server and try again."""
    
    return {
        "success": False,
        "answer": error_message,
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
