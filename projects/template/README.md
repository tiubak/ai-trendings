# {PROJECT_NAME}

{ONE-LINE DESCRIPTION}

## What It Does

{BRIEF EXPLANATION OF THE PROJECT}

## How It Works

{TECHNICAL DETAILS}

## Usage

**CRITICAL: Python Backend Required**
```bash
# Install dependencies
pip install -r requirements.txt

# Run backend
python main.py

# Or with uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000

# Open frontend in browser
open http://localhost:8000
```

## Deployment Notes

⚠️ **CRITICAL: AI Trendings requires Python backend**

Every AI Trendings project MUST include:
- ✅ `main.py` - Functional Python backend (FastAPI recommended)
- ✅ `index.html` - Frontend that connects to backend API
- ✅ `requirements.txt` - Python dependencies
- ❌ NO frontend-only projects allowed

### Vercel Deployment

**Vercel Limitation:** Vercel does NOT support running Python servers directly as-is.

| Approach | When to Use | Notes |
|----------|--------------|-------|
| **Serverless Functions** | If deploying to Vercel | Complex setup, not recommended |
| **Alternative Host** | Recommended for Python backends | Render, Railway, Netlify (better support) |
| **Vercel + Backend** | Document limitation clearly | README explains Vercel issues + alternatives |

See [VERCEL_GUIDE.md](../../VERCEL_GUIDE.md) for detailed deployment instructions.

## Tech Stack

- **Backend:** Python (FastAPI) — optional, see deployment notes
- **Frontend:** HTML/JavaScript
- **API:** {API USED} (Free - see [FREE_APIS.md](../../FREE_APIS.md))

## API

Uses {API NAME} — {API DETAILS, LIMITS, ETC}

## Free API Resources

This project uses a free API. Browse more free APIs for future projects:
- [FREE_APIS.md](../../FREE_APIS.md) - Curated list of free APIs + Vercel deployment notes
- [free-apis.github.io](https://free-apis.github.io) - Community-maintained free API directory

---

Built as part of [AI Trendings](https://github.com/tiubak/ai-trendings) — Daily AI projects.
