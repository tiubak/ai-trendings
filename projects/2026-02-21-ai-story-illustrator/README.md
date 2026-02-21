# AI Story Illustrator

Transform your short stories into beautiful illustrated narratives using AI. This project extracts key scenes from your story and generates unique artwork for each one.

## What It Does

1. **Analyzes your story** - Uses AI to identify the most visually compelling moments
2. **Extracts scenes** - Intelligently divides the narrative into 3-6 key scenes
3. **Generates descriptions** - Creates detailed visual descriptions for each scene
4. **Creates artwork** - Produces unique illustrations using AI image generation

## How It Works

```
Story Input → Scene Extraction → Prompt Generation → Image Creation → Display
     ↓              ↓                   ↓                  ↓
  50-2000 chars   AI analysis      Style + Genre    Pollinations.AI
                  (3-6 scenes)     enhancement      (free API)
```

### Technical Flow

1. **Backend (Python/FastAPI)**
   - Receives story text via `/api/illustrate` endpoint
   - Calls Pollinations.AI text API to extract scenes with context
   - Falls back to rule-based extraction if AI fails
   - Enhances prompts with art style and genre context
   - Generates image URLs via Pollinations.AI image API

2. **Frontend (HTML/JS)**
   - Modern responsive UI with gradient styling
   - Real-time loading feedback with animated messages
   - Scene-by-scene display with staggered animations
   - Template stories for quick demos

## Usage

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
python main.py

# Open http://localhost:8000 in your browser
```

### Vercel Deployment

This project is ready for Vercel deployment. The `main.py` serves both the API and frontend.

## Features

- **8 Art Styles**: Watercolor, Comic, Anime, Realistic, Fantasy, Minimalist, Vintage, Sketch
- **10 Genres**: Fantasy, Sci-Fi, Adventure, Romance, Mystery, and more
- **Smart Scene Detection**: AI-powered extraction of key visual moments
- **Sample Stories**: Pre-built templates for quick demos
- **Responsive Design**: Works on desktop and mobile

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Serve frontend |
| `/api/health` | GET | Health check |
| `/api/styles` | GET | List art styles |
| `/api/genres` | GET | List genres |
| `/api/templates` | GET | List sample stories |
| `/api/templates/{id}` | GET | Get specific template |
| `/api/illustrate` | POST | Process a story |
| `/api/extract-scenes` | POST | Extract scenes only |
| `/api/generate-prompt` | POST | Generate image prompt |
| `/api/demo` | GET | Get random demo story |

## Tech Stack

- **Backend**: Python 3.11+, FastAPI, aiohttp
- **Frontend**: Vanilla HTML/CSS/JavaScript
- **API**: [Pollinations.AI](https://pollinations.ai) (free, no API key required)
  - Text API: Scene extraction and analysis
  - Image API: Illustration generation

## API Policy

This project uses **100% free APIs**:
- No API keys required
- No rate limits (within reason)
- No authentication needed

Pollinations.AI provides:
- Text generation via `text.pollinations.ai`
- Image generation via `image.pollinations.ai/prompt/{prompt}`

## Example

**Input:**
> In the kingdom of Eldoria, an ancient dragon named Pyrrhus lived atop the highest mountain...

**Output:**
- 4 illustrated scenes
- Each scene shows a key moment
- Consistent art style throughout
- ~10-20 seconds processing time

## Limitations

- Story length: 50-2000 characters
- Maximum 6 scenes per story
- Image generation depends on Pollinations.AI availability
- First-time image loads may take a few seconds

---

Built as part of [AI Trendings](https://github.com/tiubak/ai-trendings) — Daily AI projects.
