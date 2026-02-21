# Vercel Deployment Guide for AI Trendings

This guide explains how Vercel works for this project and how to build projects that work.

---

## 🏗️ How Vercel Works

**What Vercel Is:**
- A serverless edge hosting platform
- Primarily for **static sites** (HTML/CSS/JS)
- Python/Node servers require special setup (Serverless Functions)

**What AI Trendings Uses:**
- **Static hosting** - Main site is just HTML/CSS/JS
- **GitHub integration** - Auto-deploys on every push to `master` branch
- **Environment variables** - Secure storage for API keys

---

## ⚠️ CRITICAL REQUIREMENT: Python Backend Mandatory

**For AI Trendings Projects:**
- ✅ **EVERY project MUST have a Python backend**
- ❌ Frontend-only is NOT allowed
- ✅ Backend must use FastAPI (or similar framework)
- ✅ Backend must be fully functional and testable
- ✅ Frontend must connect to backend API endpoints

**Why?** AI Trendings is about demonstrating Python + AI development skills. Frontend-only projects don't showcase backend capabilities.

---

## 🎯 Required Architecture for AI Trendings

```
┌────────────────────────────────────┐
│  Browser (User)              │
│  • Opens index.html             │
│  • Enters prompts/data           │
│  • Fetches from backend API     │
│  • Displays results              │
│                                │
└────────────────────────────────────┘
              ↓
         Python Backend (FastAPI)
              ↓
    API Endpoints:
    - POST /api/process
    - GET /api/status
    - etc.
              ↓
    External APIs (Pollinations.AI,
    Hugging Face, OpenRouter)
```

**Every AI Trendings project must follow this architecture.**

---

## 🚀 Deployment Steps (Python Backend Required)

### Step 1: Create Project Structure

```
projects/2026-02-22-project/
├── main.py              # Python backend (REQUIRED)
├── index.html           # Frontend (connects to backend)
├── requirements.txt     # Python dependencies
├── README.md           # Documentation
└── .gitignore          # Python cache, venv, etc.
```

### Step 2: Write Python Backend (FastAPI)

```python
# main.py - Minimum structure required
from fastapi import FastAPI
import os

app = FastAPI(title="Project Name")

# Environment variables
API_KEY = os.getenv("API_KEY", "")

@app.get("/")
async def root():
    """Serve the frontend"""
    with open("index.html", "r") as f:
        return f.read()

@app.post("/api/generate")
async def generate(data: dict):
    """Main AI processing endpoint"""
    # Your AI logic here
    return {"result": "success", "data": ...}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Step 3: Write Frontend (Connects to Backend)

```javascript
// index.html - Must connect to backend
async function generate() {
    const response = await fetch('/api/generate', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({prompt: input.value})
    });
    const result = await response.json();
    // Display result from backend
}
```

### Step 4: Test Locally

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start Python backend
uvicorn main:app --host 0.0.0.0 --port 8000

# 3. Open in browser
open http://localhost:8000

# 4. Test all features
# - Verify frontend connects to backend
# - Test API endpoints
# - Check error handling
# - Verify AI API calls work
```

### Step 5: Commit and Deploy

```bash
# Only commit after testing!
git add .
git commit -m "Add project: Project Name (Python backend + frontend)"
git push origin master
# Vercel auto-deploys in 30-60 seconds
```

---

## 🔐 Environment Variables

**Set on Vercel:** https://vercel.com/tiubak/ai-trendings/settings/environment-variables

| Variable | Purpose | Required? | When to Use |
|----------|-----------|------------|--------------|
| `POLLINATIONS_API_KEY` | Pollinations.AI | Optional | Text/image APIs |
| `HUGGINGFACE_API_KEY` | Hugging Face | Yes | HF Inference API |
| `OPENROUTER_API_KEY` | OpenRouter | Yes | OpenRouter models |

**Access in Python:**
```python
import os
api_key = os.getenv("HUGGINGFACE_API_KEY")  # Backend
```

---

## ⚠️ Vercel Limitation: No Python Server

**Important:** Vercel does NOT support running Python FastAPI servers as-is. Two options:

### Option 1: Serverless Functions (Complex)
- Convert backend to Vercel `api/` functions
- Each endpoint becomes a serverless function
- Slower (cold starts on each request)
- Costs money for high usage
- Complex setup

### Option 2: Alternative Hosting (Recommended for Python Backends)
- **Render** (render.com) - Free tier, better Python support
- **Railway** (railway.app) - Good Python support
- **Netlify Functions** - Better than Vercel for Python
- Use for backend-first projects

### Option 3: Keep Python for Demo, Document Vercel Limitation
- Document that backend requires Vercel Serverless
- Provide instructions for deployment on other platforms
- README.md explains both Vercel and alternative options

---

## 🐛 Common Issues & Solutions

### Issue: Frontend can't connect to backend

**Cause:** Backend not running or CORS issues

**Solution:**
```python
# Add CORS to FastAPI
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Issue: Environment variables not available

**Cause:** Not set on Vercel or wrong variable name

**Solution:**
```bash
# Check Vercel env vars
vercel env ls

# Or test locally
export API_KEY="test_key"
python main.py
```

### Issue: Build fails on Vercel

**Cause:** `requirements.txt` has incompatible packages or missing dependencies

**Solution:**
```bash
# Test locally first
pip install -r requirements.txt
python main.py

# If works locally but not on Vercel, check Python version
vercel logs  # Check deployment logs
```

---

## ✅ Checklist Before Committing

### Backend Requirements (Mandatory)
- [ ] `main.py` exists and is functional
- [ ] Uses FastAPI (or similar Python framework)
- [ ] Has at least 2 API endpoints (health + main feature)
- [ ] Environment variables use `os.getenv()`
- [ ] Error handling for all API calls
- [ ] Code is commented and readable

### Frontend Requirements
- [ ] `index.html` connects to backend API
- [ ] Displays results from backend (no hardcoded results)
- [ ] Handles loading states and errors
- [ ] Responsive design

### Testing Requirements (CRITICAL)
- [ ] Backend tested locally: `uvicorn main:app`
- [ ] Frontend tested in browser
- [ ] API endpoints tested with curl or browser
- [ ] All features verified working
- [ ] No console errors
- [ ] Environment variables work (if used)

### Documentation
- [ ] README.md explains architecture
- [ ] requirements.txt lists all dependencies
- [ ] Calendar updated (`python scripts/generate_projects.py`)
- [ ] topics-used.txt updated with topic name

---

## 📊 Examples of Good vs Bad Projects

### ✅ GOOD: Python Backend + Frontend

**Project:** AI Text Classifier
- `main.py`: FastAPI with `/api/classify` endpoint
- `index.html`: Fetches from `/api/classify`, displays results
- **Works on:** Vercel (static) + any host with Python
- **AI Trendings compliant:** Has Python backend

### ❌ BAD: Frontend-Only

**Project:** AI Meme Generator (First Attempt)
- `main.py`: Deleted (no backend needed)
- `index.html`: Direct API calls to Pollinations.AI
- **Vercel issue:** Works, but doesn't meet AI Trendings requirement
- **AI Trendings compliant:** NO - missing Python backend

### ✅ GOOD: Python Backend with Vercel Notes

**Project:** AI Image Generator
- `main.py`: Full FastAPI backend with image processing
- `README.md`: Explains Vercel limitation + alternatives (Render, Railway)
- **Works on:** Vercel (for static) + Render (for backend)
- **AI Trendings compliant:** Has Python backend + documented deployment options

---

## 🎯 Summary

| Requirement | Status |
|------------|--------|
| Python Backend | ✅ MANDATORY for all projects |
| Frontend | ✅ Required (connects to backend) |
| Local Testing | ✅ CRITICAL - must work before commit |
| Environment Variables | ✅ Use `os.getenv()` |
| Documentation | ✅ Explain architecture clearly |
| Vercel Limitation | ✅ Document alternatives when needed |

---

**Remember:** AI Trendings is about Python + AI development. Every project must demonstrate Python backend skills!
