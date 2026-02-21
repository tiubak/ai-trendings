# 🤖 AI Trendings

One AI project, every single day. Fully automated by Atlas.

## What This Is

A living portfolio showcasing daily AI/ML projects — from NLP to computer vision to generative AI. Each project is built from scratch using free APIs and open-source tools.

## Stats

- **Projects:** Auto-updated daily
- **Tech Stack:** Python, HTML/JS, free APIs only
- **Automation:** Powered by OpenClaw & Atlas

## Browse Projects

Visit the [live site](https://ai-trendings.vercel.app) or explore the calendar on the homepage.

## Project Structure

```
ai-trendings/
├── index.html          # Main calendar landing page
├── projects/           # Daily projects (one per day)
│   └── YYYY-MM-DD-project-name/
│       ├── main.py     # Python backend
│       ├── index.html  # Frontend
│       ├── README.md   # Project documentation
│       └── requirements.txt
├── vercel.json         # Vercel config
└── README.md           # This file
```

## API Policy

All projects use **free APIs only**:
- [Pollinations.AI](https://pollinations.ai) — Text/image generation
- [Hugging Face Inference](https://huggingface.co/docs/api-inference) — ML models
- Local models — Faster-Whisper, etc.

No paid services. No API keys in the repo.

## Automation

This project is fully automated by a nightly cron job that:

1. Researches an AI trend/topic
2. Designs a small, useful application
3. Writes the code (Python + HTML/JS)
4. Tests and fixes bugs
5. Commits and pushes to main
6. Updates the calendar on index.html

The agent runs in session mode with context compaction, so it can handle projects of ~2000 lines without hitting token limits.

---

Built by [@tiubak](https://github.com/tiubak) • Automated by Atlas 🌍
