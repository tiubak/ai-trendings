# AI Character Persona Generator

Generate rich, detailed character profiles for stories, games, and roleplaying using AI.

## 🎭 Features

- **Instant Character Creation**: Input a name, role, and setting to get a complete character profile
- **Detailed Profiles**: Includes backstory, personality, strengths, weaknesses, motivation, relationships, and signature quotes
- **Multiple Archetypes**: Hero, Villain, Mentor, Rogue, Warrior, Scholar, and more
- **Character History**: Keep track of all generated characters and reload them anytime
- **Fallback Mode**: Works even if AI API is unavailable with handcrafted templates

## 🚀 How It Works

1. Enter your character's name, role, setting, theme, and desired traits
2. Click "Generate Persona" to create a unique character
3. Explore the detailed profile with backstory, personality, relationships, and more
4. Generate multiple characters and browse your character history

## 🏗️ Architecture

**Stateless Serverless Functions:**
- Each request is independent - no shared in-memory state
- Client stores character history in JavaScript array
- Server processes requests and returns complete persona data
- Fallback templates ensure functionality even if AI API fails

**API Endpoint:**
- `POST /api/2026-02-23-ai-character-generator/start`
- Request: `{ name, role, setting, theme, traits }`
- Response: `{ success: true, persona: { ... } }`

**Frontend:**
- Stores all generated characters in client-side array
- No backend database needed
- State persists during the session (could be extended with localStorage)

## 🛠️ Tech Stack

- **Frontend**: Vanilla HTML/CSS/JavaScript
- **Backend**: Vercel Serverless Functions (Python)
- **AI API**: Pollinations.AI (text generation)
- **Hosting**: Vercel

## 📦 Environment Variables

Required on Vercel:
- `POLLINATIONS_API_KEY`: Your Pollinations.AI API key (free at https://enter.pollinations.ai)

## 🎨 Character Fields

Each generated persona includes:

- **Name**: Character's name
- **Role**: Archetype (hero, villain, mentor, etc.)
- **Backstory**: 3-4 sentences about origin and past
- **Personality**: Temperament and behavior description
- **Strengths**: 3 key abilities or traits
- **Weaknesses**: 3 vulnerabilities or flaws
- **Motivation**: What drives this character
- **Relationships**: Important ally and rival descriptions
- **Signature Quote**: A memorable line the character would say

## 🌐 Live Demo

https://ai-trendings.vercel.app/projects/2026-02-23-ai-character-generator/

## 📝 Example Usage

**Input:**
```
Name: Aric Thorne
Role: Hero
Setting: Fantasy World
Theme: Epic Adventure
Traits: brave, honorable
```

**Output:**
```json
{
  "name": "Aric Thorne",
  "role": "Hero",
  "backstory": "Aric Thorne emerged from humble beginnings in Fantasy World, destined to protect the innocent and fight for justice against overwhelming odds.",
  "personality": "Brave, selfless, and driven by an unshakeable moral compass. Often struggles with the weight of responsibility.",
  "strengths": ["Unwavering courage", "Natural leadership", "Magnetic charisma"],
  "weaknesses": ["Self-sacrificing to a fault", "Trusts too easily", "Haunted by past failures"],
  "motivation": "To protect those who cannot protect themselves and restore balance to the world.",
  "relationships": {
    "ally": "A wise mentor who guides them through difficult choices.",
    "rival": "A dark reflection of themselves who tests their convictions."
  },
  "signature_quote": "Hope is not given. It is forged in the fires of sacrifice."
}
```

## 🔒 Security

- All character generation happens server-side
- API keys are stored as environment variables
- CORS headers allow only necessary domains
- Input validation on all fields

## 📄 License

MIT License - Feel free to use and modify for your projects!
