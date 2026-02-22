# AI Dungeon Master

An interactive AI‑powered text adventure game that generates immersive storylines, characters, and choices in real‑time using free AI APIs.

## What It Does

AI Dungeon Master acts as your personal dungeon master, creating unique interactive stories across four themes: **fantasy**, **sci‑fi**, **horror**, and **mystery**. Each adventure is generated on‑the‑fly using Hugging Face text generation models, and scenes are illustrated with AI‑generated images from Pollinations.AI.

## How It Works

1. **Backend (FastAPI)** manages game state, calls AI APIs, and provides REST endpoints
2. **Hugging Face Inference API** generates story text using the free GPT‑2 model
3. **Pollinations.AI** creates scene illustrations based on the current story context
4. **Frontend (HTML/JavaScript)** presents the story, choices, and images in an engaging UI
5. **Game state** is maintained server‑side (in‑memory for demo) with full history tracking

## Usage

**CRITICAL: Python Backend Required**
```bash
# Install dependencies
pip install -r requirements.txt

# Run backend
python main.py

# Or with uvicorn (recommended)
uvicorn main:app --host 0.0.0.0 --port 8000

# Open frontend in browser
open http://localhost:8000  # or visit http://localhost:8000
```

## Deployment Notes

⚠️ **CRITICAL: AI Trendings requires Python backend**

Every AI Trendings project MUST include:
- ✅ `main.py` - Functional Python backend (FastAPI recommended)
- ✅ `index.html` - Frontend that connects to backend API
- ✅ `requirements.txt` - Python dependencies
- ❌ NO frontend‑only projects allowed

### Vercel Deployment

**Vercel Limitation:** Vercel does NOT support running Python servers directly as‑is.

| Approach | When to Use | Notes |
|----------|--------------|-------|
| **Serverless Functions** | If deploying to Vercel | Complex setup, not recommended |
| **Alternative Host** | Recommended for Python backends | Render, Railway, Netlify (better support) |
| **Vercel + Backend** | Document limitation clearly | This project is fully functional locally; Vercel static hosting works for frontend only |

See [VERCEL_GUIDE.md](../../VERCEL_GUIDE.md) for detailed deployment instructions.

## Tech Stack

- **Backend:** Python (FastAPI, Pydantic, httpx)
- **Frontend:** HTML5, CSS3, JavaScript (ES6)
- **AI APIs:** Hugging Face Inference API (GPT‑2), Pollinations.AI (image generation)
- **Deployment:** Vercel (frontend), Render/Railway (backend optional)

## API Details

| API | Usage | Limits | Key Required |
|-----|-------|--------|--------------|
| **Hugging Face Inference** | Text generation for story scenes | 1,000 requests/month (free tier) | ✅ Yes (free token) |
| **Pollinations.AI** | Image generation for scene illustrations | Unlimited (free) | ❌ Optional |

**Environment variables needed:**
- `HUGGINGFACE_API_KEY` – get at https://huggingface.co/settings/tokens
- `POLLINATIONS_API_KEY` – optional, get at https://enter.pollinations.ai
- `OPENROUTER_API_KEY` – optional, for alternative models

## Project Structure

```
2026‑02‑21‑ai‑dungeon‑master/
├── main.py              # FastAPI backend (1520+ lines)
├── index.html           # Frontend UI (500+ lines)
├── README.md            # This documentation
├── requirements.txt     # Python dependencies
└── (auto‑generated)     # No other files needed
```

## Features

✅ **Interactive Storytelling** – AI generates unique branching narratives  
✅ **Multiple Themes** – Fantasy, sci‑fi, horror, mystery  
✅ **AI‑Generated Images** – Each scene illustrated with AI art  
✅ **Game State Management** – Full history tracking and export  
✅ **Responsive UI** – Works on desktop and mobile  
✅ **Error Handling** – Graceful degradation if APIs fail  
✅ **Export Functionality** – Save your adventure as JSON  

## Local Testing

1. Clone the repository
2. Set environment variables (copy `.env.example` to `.env`)
3. Install dependencies: `pip install -r requirements.txt`
4. Run backend: `uvicorn main:app --host 0.0.0.0 --port 8000`
5. Open `http://localhost:8000` in your browser
6. Start your adventure!

## Free API Resources

This project uses free APIs. Browse more free APIs for future projects:
- [FREE_APIS.md](../../FREE_APIS.md) – Curated list of free APIs + Vercel deployment notes
- [free‑apis.github.io](https://free‑apis.github.io) – More free APIs for inspiration

---

Built for [AI Trendings](https://github.com/tiubak/ai‑trendings) – one AI project, every single day.