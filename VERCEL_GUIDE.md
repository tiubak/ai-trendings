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

## 🎯 Two Architectures for Projects

### 1. Frontend-Only (✅ PREFERRED for Vercel)

**What it is:**
- HTML + CSS + JavaScript only
- No Python/Node backend needed
- APIs called directly from browser

**When to use:**
- ✅ APIs work from browser (Pollinations.AI, free-apis.github.io)
- ✅ Simple processing (Canvas API, Web Speech API, etc.)
- ✅ No secrets needed in code
- ✅ Want project to work anywhere (Vercel, Netlify, GitHub Pages)

**Example:** AI Meme Generator
- Pollinations.AI called via `fetch()` from JavaScript
- Canvas API adds captions to images
- Downloads PNG files directly

**Pros:**
- ✅ Works perfectly on Vercel (just static files)
- ✅ No server costs
- ✅ Fast (no server round-trips)
- ✅ Simple deployment (just push to GitHub)
- ✅ Debuggable in browser console

**Cons:**
- ⚠️ API keys exposed in frontend code (use only for free/public APIs)
- ⚠️ Limited browser capabilities vs. Python

---

### 2. Python Backend (⚠️ Complex on Vercel)

**What it is:**
- FastAPI/Express server running Python/Node
- Requires Vercel Serverless Functions setup
- API endpoints served as `api/` routes

**When to use:**
- ⚠️ API needs secret keys (Hugging Face, OpenRouter)
- ⚠️ Complex processing (ML inference, large file handling)
- ⚠️ Server-side caching needed
- ⚠️ Database/storage requirements

**How it works on Vercel:**
```
1. Create `api/` directory in project
2. Each `.py` file becomes an API endpoint
3. Vercel compiles to serverless functions
4. Endpoints accessible at `/api/filename`
```

**Example Structure:**
```
projects/2026-02-22-project/
├── api/
│   ├── generate.py        → /api/generate
│   ├── health.py          → /api/health
│   └── requirements.txt
├── index.html              (frontend)
└── README.md
```

**Pros:**
- ✅ API keys secure (server-side)
- ✅ Full Python/Node capabilities
- ✅ Server-side processing

**Cons:**
- ❌ Complex setup (serverless functions)
- ❌ Slower (cold starts on each request)
- ❌ Costs money for high usage
- ❌ Harder to debug

---

## 🚀 Deployment Steps

### Option 1: Frontend-Only Project

1. Write HTML/CSS/JS code
2. Open `index.html` in browser to test
3. Git commit and push to GitHub
4. ✅ Vercel auto-deploys (30-60 seconds)
5. Done!

### Option 2: Python Backend Project

1. Create `api/` directory
2. Write Python FastAPI code
3. Create `requirements.txt` for serverless
4. Test with `vercel dev` locally
5. Git commit and push to GitHub
6. ✅ Vercel compiles and deploys
7. Test live endpoints at `https://ai-trendings.vercel.app/api/*`

---

## 🔐 Environment Variables

**Set on Vercel:** https://vercel.com/tiubak/ai-trendings/settings/environment-variables

| Variable | Purpose | When Needed |
|----------|-----------|--------------|
| `POLLINATIONS_API_KEY` | Pollinations.AI | Optional (free APIs work without it) |
| `HUGGINGFACE_API_KEY` | Hugging Face | Yes for backend projects |
| `OPENROUTER_API_KEY` | OpenRouter models | Yes for backend projects |

**Access in code:**
```python
import os
api_key = os.getenv("HUGGINGFACE_API_KEY")  # Backend only
```

```javascript
// Frontend-only: call APIs directly, no key needed
const response = await fetch('https://gen.pollinations.ai/prompt/...');
```

---

## 🐛 Common Issues & Solutions

### Issue: "NOT_FOUND" (CLE1) on Vercel

**Cause:** Project tries to call `/api/` endpoint that doesn't exist

**Solution:** Use frontend-only architecture or implement proper serverless functions

### Issue: API calls failing on Vercel

**Cause:** Calling API that requires key, but key not accessible

**Solution:** Use frontend APIs (Pollinations.AI) or set env vars properly

### Issue: CORS errors

**Cause:** Backend API blocking frontend requests

**Solution:** Add CORS middleware (FastAPI example in template)

### Issue: Build fails on Vercel

**Cause:** `requirements.txt` has incompatible packages or missing

**Solution:** Test locally with `vercel dev` before pushing

---

## 📋 Agent Decision Tree

The AI agent follows this process when creating projects:

1. **Does project need API key?**
   - YES → Backend consideration
   - NO → Frontend-first preferred

2. **Too complex for JavaScript?**
   - YES → Python backend (serverless)
   - NO → Frontend-only recommended

3. **Can be done frontend-only?**
   - YES → DO THIS (Vercel loves it)
   - NO → Backend only if needed

**Result:** Frontend-first is used 80% of the time

---

## ✅ Checklist Before Committing

- [ ] Project works locally (open index.html in browser)
- [ ] All features tested and working
- [ ] No console errors
- [ ] API calls successful
- [ ] Downloads/exports work
- [ ] README.md updated
- [ ] Calendar updated (`python scripts/generate_projects.py`)
- [ ] topics-used.txt updated
- [ ] Only frontend files (or properly structured backend)
