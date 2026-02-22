# AI Dungeon Master

An AI-powered interactive text adventure game.

## Architecture

This project uses **Vercel Serverless Python Functions** with project-specific API endpoints:

```
ai-trendings/
├── api/
│   └── dungeon-master/           ← Project-specific API
│       ├── start.py              ← POST /api/dungeon-master/start
│       └── choice.py             ← POST /api/dungeon-master/choice
└── projects/
    └── 2026-02-21-ai-dungeon-master/
        └── index.html             ← Frontend (calls /api/dungeon-master/*)
```

## How It Works

1. Frontend calls `/api/dungeon-master/start` to create a new game
2. Backend generates story using Pollinations.AI
3. Player makes choices → `/api/dungeon-master/choice`
4. AI generates next scene based on choice

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/dungeon-master/start` | POST | Start new game |
| `/api/dungeon-master/choice` | POST | Make a choice |

## Environment Variables

Set on Vercel:
- `POLLINATIONS_API_KEY` - Required for text generation

---

Built for [AI Trendings](https://github.com/tiubak/ai-trendings)
