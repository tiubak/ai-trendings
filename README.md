# 🤖 AI Trendings

**One AI project, every single day. Fully automated by Atlas.**

🔗 **Live Site:** [https://ai-trendings.vercel.app](https://ai-trendings.vercel.app)

## What This Is

A living portfolio showcasing daily AI/ML projects — interactive web apps powered by free AI APIs. Each project is built from scratch, committed automatically, and deployed to Vercel.

**Goal:** Demonstrate creativity, technical skill, and consistent delivery through 30+ unique AI applications.

## Tech Stack

| Layer | Technology |
|-------|------------|
| **AI/ML** | Pollinations.AI (free text/image generation) |
| **Backend** | Python serverless functions on Vercel |
| **Frontend** | Vanilla HTML/CSS/JS (no frameworks) |
| **Deployment** | Vercel (auto-deploys from GitHub) |
| **Automation** | OpenClaw cron job running daily at 2 AM ET |

## Project Structure

```
ai-trendings/
├── api/                        # Python serverless functions
│   ├── 2026-02-20-*.py        # One file per project (FLAT structure!)
│   ├── 2026-02-21-*.py
│   ├── pyproject.toml         # Build config
│   └── requirements.txt       # Dependencies
├── projects/                   # Daily project frontends
│   ├── 2026-02-20-ai-cosmic-whisperer/
│   │   ├── index.html         # Frontend UI
│   │   └── README.md          # Project docs
│   ├── 2026-02-21-ai-dungeon-master/
│   └── ...
├── projects.json               # Project registry
├── index.html                  # Main calendar landing page
└── README.md                   # This file
```

## How It Works

Each project follows this architecture:

```
api/2026-02-XX-project-name.py  →  /api/2026-02-XX-project-name
projects/2026-02-XX-project-name/index.html → frontend
```

**Key Design Decisions:**
- **Single API file per project** — all endpoints via `action` parameter
- **Flat API structure** — Vercel Python requires `api/*.py` directly (no nested dirs!)
- **curl subprocess** — Pollinations.AI blocks Python urllib (Cloudflare 403)
- **Stateless handlers** — each request is independent

## Featured Projects

| Date | Project | Description |
|------|---------|-------------|
| Feb 20 | [AI Cosmic Whisperer](projects/2026-02-20-ai-cosmic-whisperer/) | Mystical wisdom generator with space-themed UI |
| Feb 21 | [AI Dungeon Master](projects/2026-02-21-ai-dungeon-master/) | Interactive text adventure game |
| Feb 22 | [AI Story Illustrator](projects/2026-02-22-ai-story-illustrator/) | Transform stories into illustrated narratives |
| Feb 23 | [AI Character Generator](projects/2026-02-23-ai-character-generator/) | Create detailed character profiles |

*...and counting!*

## API Policy

**Free APIs only:**
- **Pollinations.AI** — Text and image generation (free, generous limits)
- **Hugging Face Inference** — ML models (free tier)
- **Local models** — Faster-Whisper, etc.

No paid services. No credit cards required.

## Automation

Powered by a nightly cron job (2:00 AM ET) that:

1. Reads [`skills/ai-trending-generator.md`](../skills/ai-trending-generator.md) for instructions
2. Picks a creative project idea
3. Generates Python backend + HTML frontend
4. Updates `projects.json` registry
5. Commits and pushes to GitHub
6. Vercel auto-deploys the changes

The agent uses the `stepfun/step-3.5-flash` model via OpenRouter (free tier).

## Development

```bash
# Clone the repo
git clone https://github.com/tiubak/ai-trendings.git

# No build step needed — just open index.html
# Or deploy to Vercel for full functionality

# Environment variables (for Vercel)
POLLINATIONS_API_KEY=your_key_here  # Optional but recommended
```

## License

MIT — use anything here for your own projects!

---

Built by [@tiubak](https://github.com/tiubak) • Automated by [Atlas](https://openclaw.ai) 🌍
