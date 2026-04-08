# 🔄 Multi-Provider LLM Fallback System

## Overview

PaperLens now automatically rotates between **Gemini**, **Claude**, and **Groq** when API rate limits are hit.

```
User Query
    ↓
Try Gemini (60/min)
    ↓ If rate-limited, try Claude
Claude (100K tokens/month)
    ↓ If rate-limited, try Groq
Groq (90/min, fastest)
    ↓
Return Answer
```

---

## 📋 Setup Instructions

### Step 1: Get API Keys (5 minutes total)

All keys are **FREE**. Get them from:

#### **Gemini** (Currently using)
- URL: https://ai.google.dev/tutorials/setup
- Create project → Enable API → Generate key
- Free: 60 requests/min

#### **Claude** ⭐ RECOMMENDED
- URL: https://console.anthropic.com
- Sign up → API tab → Generate key
- Free: 100K tokens/month (~10K calls)
- **Best quality & largest free tier**

#### **Groq** ⚡ FASTEST
- URL: https://console.groq.com
- Sign up → Keys tab → Generate key
- Free: 90 requests/min
- **Fastest response (~50ms)**

### Step 2: Configure Keys

Copy `.env.example` to `.env` and add all keys:

```env
GEMINI_API_KEY=your_gemini_key
CLAUDE_API_KEY=your_claude_key
GROQ_API_KEY=your_groq_key
```

### Step 3: Install New Dependencies

```bash
pip install -r requirements.txt
```

New packages:
- `anthropic==0.7.1` - Claude API
- `groq==0.4.1` - Groq API

---

## 🧠 How It Works

### Provider Priority (Default Order)

1. **Gemini** (primary)
2. **Claude** (fallback)
3. **Groq** (last resort)

Each provider is tried in order until one succeeds.

### Rate Limit Handling

```python
# Automatic, no code needed:
# If Gemini returns 429 (rate limited):
#   → Try Claude
# If Claude returns 429:
#   → Try Groq
# If all fail:
#   → Return error message
```

### Response Tracking

Every response includes which provider was used:

```json
{
  "success": true,
  "answer": "...",
  "provider_used": "claude",  // Shows which provider worked
  "timestamp": "2026-04-08T..."
}
```

---

## 💰 Cost Breakdown

| Provider | Cost | Limit | Best For |
|----------|------|-------|----------|
| **Gemini** | FREE | 60/min | Quick queries |
| **Claude** | FREE | 100K tokens/month | Complex analysis, best quality |
| **Groq** | FREE | 90/min | Speed-critical apps |
| **Combined** | FREE | ~∞ | Unlimited for personal use |

**Total monthly cost with all 3:** $0 🎉

---

## 🧪 Testing Providers

### Test All Configured Providers

```python
from app.services.llm_provider_service import test_providers

results = test_providers()
print(results)
```

Output:
```
{
  "gemini": {"status": "success", "response": "Hello"},
  "claude": {"status": "success", "response": "Hello"},
  "groq": {"status": "success", "response": "Hi there"}
}
```

### Check Available Providers

```python
from app.services.llm_provider_service import get_available_providers

available = get_available_providers()
print(f"Providers available: {available['total_available']}")
# Output: Providers available: 3
```

---

## 📊 Provider Comparison

### Speed
```
Groq ⚡ ~50ms (fastest - LPU based)
  ↓
Claude & Gemini ~200-500ms
```

### Quality
```
Claude 🌟 (best for nuanced analysis)
  ↓
Gemini & Groq (good, slightly faster)
```

### Free Tier Capacity
```
Claude 💰 100K tokens/month (≈ 10K calls)
  ↓
Gemini & Groq 🚀 60-90 requests/min (≈ 36K-50K per month)
```

---

## 🔧 Advanced Configuration

### Custom Provider Order

```python
from app.services.llm_provider_service import generate_with_fallback

# Try Groq first, then Claude, then Gemini
result = generate_with_fallback(
    prompt="Your question here",
    provider_order=["groq", "claude", "gemini"]
)
```

### Error Handling

```python
result = generate_with_fallback(prompt)

if result["success"]:
    print(f"Answer: {result['answer']}")
    print(f"Provider: {result['provider_used']}")
else:
    print("All providers failed")
```

---

## 🐛 Troubleshooting

### Issue: "All providers failed"

**Causes & Solutions:**
1. **No API keys configured**
   - Solution: Add keys to `.env`

2. **API keys invalid**
   - Solution: Verify keys on provider dashboards

3. **Provider account disabled**
   - Solution: Check provider account status

4. **Internet connectivity**
   - Solution: Check network connection

### Test Individual Provider

```python
from app.services.llm_provider_service import _call_claude

result = _call_claude("Hello")
if result:
    print("Claude working!")
else:
    print("Claude failed")
```

---

## 📈 Monitoring & Metrics

### Track Which Providers Are Used

Update your database/logging to track:

```python
{
    "question": "What is wind power?",
    "provider_used": "claude",
    "response_time_ms": 245,
    "timestamp": "2026-04-08T12:34:56Z"
}
```

### Rate Limit Prevention

Monitor usage to stay within free tier:
- Gemini: Max 60 req/min
- Claude: Max 100K tokens/month
- Groq: Max 90 req/min

---

## 🚀 Best Practices

### 1. Configure All 3 Keys (Recommended)
```env
# Gives maximum uptime & resilience
GEMINI_API_KEY=key1
CLAUDE_API_KEY=key2
GROQ_API_KEY=key3
```

### 2. Use Meaningful Prompts
- Shorter prompts = fewer tokens = stay in free tier longer

### 3. Cache Results
- Store responses in Redis/DB to avoid repeated calls

### 4. Monitor Provider Status
- Track which providers fail most often
- Rotate provider order if needed

---

## 📞 Need Help?

1. **Test providers**: `python -c "from app.services.llm_provider_service import test_providers; print(test_providers())"`
2. **Check env vars**: Ensure `.env` has all keys
3. **Verify API keys**: Test keys on provider dashboards

---

## 🎯 Next Steps

1. ✅ Get API keys (5 min)
2. ✅ Update `.env` file
3. ✅ Run `pip install -r requirements.txt`
4. ✅ Restart backend server
5. ✅ Test upload & chat (should work with any provider)

Done! Your system is now resistant to rate limits. 🛡️
