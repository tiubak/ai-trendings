# 🤖 AI Trendings

**One AI project, every single day. Fully automated by Atlas.**

🔗 **Live:** [https://ai-trendings.vercel.app](https://ai-trendings.vercel.app)  
📦 **Repo:** [https://github.com/tiubak/ai-trendings](https://github.com/tiubak/ai-trendings)

---

## What This Is

A living portfolio showcasing **daily AI/ML projects** — interactive web apps powered by free AI APIs. Each project is built from scratch, committed automatically, and deployed to Vercel.

**Goal:** Demonstrate creativity, technical skill, and consistent delivery through unique AI applications.

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| **AI/ML** | OpenRouter (text), Pollinations.AI (images), HuggingFace (TTS, embeddings) |
| **Backend** | Python serverless functions on Vercel |
| **Frontend** | Vanilla HTML/CSS/JS (no frameworks) |
| **Deployment** | Vercel (auto-deploys from GitHub) |
| **Automation** | OpenClaw cron job running daily at 2:00 AM ET |

---

## Project Types

We maintain a **balance** between educational and fun projects:

### 🧠 Deep AI Topics (2-3 days/week)
Educational projects **ABOUT AI**:
- AI concept explainers (transformers, attention, embeddings)
- AI model comparators (GPT vs Claude vs Gemini)
- Neural network visualizers
- AI ethics simulators, safety explorers
- Training cost calculators, token counters

### 🎮 Fun AI Applications (2-3 days/week)
Entertaining projects **USING AI**:
- AI Dream Interpreter, AI Fortune Teller
- AI Story Generator, AI Poetry Creator
- AI Meme Generator, AI Joke Teller
- AI Game Master, AI Adventure Guide

### 🛠️ Practical AI Tools (1-2 days/week)
Useful everyday applications:
- AI Email Drafter, AI Summarizer
- AI Code Explainer, AI Translator

---

## Architecture

### Single Serverless Function Design

Vercel's Hobby plan limits to **12 serverless functions**. We use **ONE** with dynamic routing.

```
api/
├── index.py           ← SINGLE function (routes by date)
├── lib/
│   ├── base.py        ← Common: OpenRouter, Pollinations, HuggingFace
│   └── projects/
│       ├── __init__.py
│       ├── day_2026_02_01.py  ← Each project's logic
│       └── day_2026_02_02.py
├── pyproject.toml
└── requirements.txt

projects/
├── 2026-02-01-ai-context-window/
│   ├── index.html     ← Frontend
│   └── README.md
└── projects.json      ← Project registry (for calendar)

index.html              ← Main calendar landing page
```

### How It Works

```
Frontend sends POST to /api/index with { date: "2026-02-01", action: "start", ... }
                                    ↓
                           api/index.py routes by date
                                    ↓
                  lib/projects/day_2026_02_01.py handles action
                                    ↓
                            Returns JSON response
```

---

## API Policy

**Free APIs only:**

| API | Use Case | Auth |
|-----|----------|------|
| **OpenRouter** | Text generation (primary) | `OPENROUTER_API_KEY` |
| **Pollinations.AI** | Image generation | `POLLINATIONS_API_KEY` |
| **HuggingFace** | TTS, embeddings, audio | `HUGGINGFACE_API_KEY` |

**No paid services. No credit cards required.**

---

## Featured Projects

| Date | Project | Type |
|------|---------|------|
| Feb 1 | [AI Context Window Explorer](projects/2026-02-01-ai-context-window-explorer/) | 🧠 Education |
| Feb 2 | *Coming soon...* | 🎮 Fun |

*Projects generated daily at 2:00 AM ET.*

---

## Security

**API keys NEVER exposed to frontend:**

```python
# ❌ WRONG - Exposes API key!
return {"image_url": "https://...?key=SECRET"}

# ✅ CORRECT - API key stays on backend
image_base64 = fetch_image(prompt)  # Auth handled in backend
return {"image_base64": image_base64}  # Frontend: data:image/png;base64,...
```

---

## Automation

Powered by a nightly cron job that:

1. Reads `skills/ai-trending-generator.md` for instructions
2. Picks a project idea (balanced by type)
3. Creates Python backend + HTML frontend
4. Updates `projects.json` registry
5. Commits and pushes to GitHub
6. Vercel auto-deploys

**Agent Model:** `openrouter/stepfun/step-3.5-flash:free`

---

## Development

```bash
# Clone the repo
git clone https://github.com/tiubak/ai-trendings.git

# Install dependencies (for local testing)
cd ai-trendings/api
pip install -r requirements.txt

# Environment variables (set in Vercel)
OPENROUTER_API_KEY=your_key
POLLINATIONS_API_KEY=your_key
HUGGINGFACE_API_KEY=your_key

# Local development
python -m http.server 8000  # Serve frontends
# Or deploy to Vercel for full functionality
```

---

## Project Guidelines

See [`skills/ai-trending-generator.md`](../skills/ai-trending-generator.md) for complete instructions on:
- Project structure and naming
- Security requirements
- Balance guidelines
- Mandatory checklist

---

## Stats

- **Projects:** Daily since Feb 2026
- **API Cost:** $0 (all free tiers)
- **Deployment:** Automated via Vercel
- **Uptime:** 99.9% (Vercel SLA)

---

## License

MIT — use anything here for your own projects!

---

Built by [@tiubak](https://github.com/tiubak) • Automated by [Atlas](https://openclaw.ai) 🌍
