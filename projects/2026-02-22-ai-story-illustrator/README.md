# AI Story Illustrator

Transform your story ideas into beautifully illustrated narratives using AI.

## Features

- ✨ **Story Enhancement**: Expand your ideas into engaging, well-written stories
- 🎨 **AI Illustrations**: Generate custom artwork that matches your story
- 🎭 **Multiple Styles**: Choose from engaging, fantasy, sci-fi, mystery, humorous, or dramatic
- 🖼️ **Art Variations**: Digital art, watercolor, anime, realistic, pixel art, or oil painting
- 🔄 **Instant Regeneration**: Create new illustrations with one click

## How It Works

1. Enter your story idea (a sentence or two)
2. Choose a writing style (engaging, fantasy, sci-fi, etc.)
3. Click "Enhance Story" to expand your idea into a full narrative
4. The AI automatically generates an illustration
5. Change art styles or regenerate for different visuals

## Architecture

**Stateless Serverless Functions**
- Each endpoint runs independently with no shared state
- Client stores and passes state (story, styles, image URL) with each request
- API calls have fallback handling for reliability

**Endpoints**
- `POST /api/story (action: enhance)` - Enhances story text
- `POST /api/story (action: illustrate)` - Generates illustration URL

## Tech Stack

- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **Backend**: Python (Vercel Serverless Functions)
- **AI**: Pollinations.AI (text & image generation)
- **Deployment**: Vercel

## API Keys

Required environment variables on Vercel:
- `POLLINATIONS_API_KEY` - Get free at https://enter.pollinations.ai

## License

MIT
