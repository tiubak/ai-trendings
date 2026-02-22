# Free APIs for AI Trendings Projects

This file catalogs free APIs the agent can use for daily projects. All APIs listed here:
- ✅ Free (no payment required)
- ✅ No API key (or free signup only)
- ✅ Legal to use in public projects

## Environment Variables (Set on Vercel)

| Variable | Purpose | Required? | Where to Get |
|----------|-----------|------------|--------------|
| `POLLINATIONS_API_KEY` | Pollinations.AI | **YES - REQUIRED** | https://enter.pollinations.ai |
| `HUGGINGFACE_API_KEY` | Hugging Face Inference | Yes for HF API | https://huggingface.co/settings/tokens |
| `OPENROUTER_API_KEY` | OpenRouter models | Yes for OpenRouter | https://openrouter.ai/keys |

**Note:** These are set on Vercel → Project Settings → Environment Variables.

**Local Development:** Copy `.env.example` to `.env` and fill in values.

## AI/ML APIs

### Text Generation
- **Pollinations.AI Text** - https://pollinations.ai  
  - Text generation, prompts, creative writing
  - **API key now REQUIRED** (changed 2026-02-21)
  - Free tier: Unlimited with valid key
  - Get key at: https://enter.pollinations.ai

- **Hugging Face Inference** - https://huggingface.co/docs/api-inference
  - Thousands of free models (text, image, audio)
  - Free tier: 1,000 requests/month
  - Requires: Free account (API key)

### Image Generation
- **Pollinations.AI Images** - https://pollinations.ai
  - Flux model, DALL-E alternatives
  - **API key now REQUIRED** (changed 2026-02-21)
  - Free tier: Unlimited with valid key
  - Get key at: https://enter.pollinations.ai
- **Pollinations.AI Images** - https://pollinations.ai
  - Flux model, DALL-E alternatives
  - No API key required
  - Free unlimited generation

- **Hugging Face** - https://huggingface.co/docs/api-inference
  - Stable Diffusion, Midjourney alternatives
  - Free tier available
  - Requires: Free account

### Speech/Audio
- **Faster-Whisper** (Local) - https://github.com/SYSTRAN/faster-whisper
  - Speech-to-text transcription
  - Runs locally, no API needed
  - Installed on this system

### Computer Vision
- **Hugging Face Vision Models** - https://huggingface.co
  - Object detection, segmentation, classification
  - Free tier available
  - Requires: Free account

### NLP/Text Processing
- **Hugging Face NLP Models** - https://huggingface.co
  - Sentiment analysis, summarization, translation
  - Free tier available
  - Requires: Free account

## General Free APIs (https://free-apis.github.io)

Browse for inspiration:
- **Weather APIs** - OpenWeather, WeatherAPI
- **Currency APIs** - Exchange rates
- **Random APIs** - Jokes, quotes, facts
- **Data APIs** - JSON datasets, mock APIs
- **Social APIs** - Twitter, Reddit (public endpoints)
- **Game APIs** - Trivia, word games
- **Dev Tools APIs** - Hash generators, validators

## Project Ideas by Category

### NLP (Natural Language Processing)
- Sentiment analyzer
- Text summarizer
- Language translator
- Keyword extractor
- Named entity recognizer
- Document classifier

### Computer Vision
- Object detector
- Face detector
- Color palette extractor
- Image style transfer
- Sketch generator
- Photo enhancer

### Generative AI
- Story generator
- Poem writer
- Caption generator
- Code explainer
- Prompt optimizer
- Chatbot trainer

### Data Tools
- CSV visualizer
- JSON formatter
- Data cleaner
- Statistics calculator
- Chart generator

### Games/Interactive
- AI-powered quiz
- Guess the AI
- Word puzzle solver
- Strategy game AI
- Trivia generator

### Utilities
- Image compressor
- PDF converter
- QR code generator
- Markdown editor
- Regex tester

## Vercel Deployment Notes

⚠️ **Vercel Limitation:** Vercel does NOT support running FastAPI/Python servers directly. For AI Trendings projects:

**Recommended Approach: Frontend-First**
- Call APIs directly from JavaScript (no backend needed)
- Use client-side libraries (Canvas API, Web Speech API, etc.)
- Works on any static host (Vercel, Netlify, GitHub Pages)
- Faster and cheaper (no serverless function execution)

**When to Use Backend:**
- Only if:
  1. API requires secret keys that shouldn't be exposed
  2. Complex processing that can't be done in browser
  3. Need to cache results server-side

If backend is required on Vercel:
- Use Vercel Serverless Functions (api/ directory)
- Or use Render/Railway/Netlify Functions (better Python support)

**Example:** AI Meme Generator (2026-02-21) was refactored to frontend-only:
- Pollinations.AI called directly from browser
- Canvas API adds captions client-side
- No Python backend needed

## Notes for Agent

1. **Always check topics-used.txt** before choosing a new topic
2. **Rotate categories** - don't do NLP 3 days in a row
3. **Prefer APIs with no keys** - easier deployment
4. **Keep it demoable** - the project should work in < 5 minutes
5. **Document the API** - link, limits, usage in README
