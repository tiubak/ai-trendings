# AI Meme Generator

Generate hilarious memes using AI-generated images and witty captions — all for free!

## What It Does

This project combines free AI APIs to create custom memes in seconds. You can:
1. Generate images from text prompts using Pollinations.AI's free image generation
2. Generate witty captions using Pollinations.AI's text generation
3. Combine images with top and bottom text to create classic meme formats
4. Download your creations to share with friends

## How It Works

The backend is built with Python/FastAPI and leverages two key free APIs:
- **Pollinations.AI Image Generation**: Generates images from text prompts using models like Flux
- **Pollinations.AI Text Generation**: Generates funny captions and text responses

When you submit a request, the system:
1. Checks if the image prompt exists in cache (for speed)
2. If not cached, fetches a fresh image from Pollinations.AI
3. Adds your top and bottom text with proper meme formatting (white text with black outline)
4. Returns the completed meme image

The frontend provides an intuitive interface with example prompts, random idea generation, and one-click downloads.

## Usage

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
python main.py

# Visit http://localhost:8000 in your browser
```

Or simply open the `index.html` file in your browser when the server is running.

## Tech Stack

- **Backend:** Python 3.10+, FastAPI, Uvicorn
- **Frontend:** HTML5, CSS3, JavaScript (Vanilla)
- **Image Processing:** Pillow (PIL)
- **APIs:** Pollinations.AI (Image & Text Generation)

## API Details

Uses Pollinations.AI's completely free APIs:
- **Image Generation:** `https://image.pollinations.ai/prompt/{prompt}`
- **Text Generation:** `https://text.pollinations.ai/prompt/{prompt}`
- **No API keys required** — truly free tier for everyone
- **Models:** Flux (default), OpenAI, and others available

## Features

- 🚀 **Free & No Signup**: Uses entirely free APIs with no authentication
- 🎨 **AI-Generated Images**: Create images from any text prompt
- 📝 **AI-Generated Captions**: Get witty captions based on your ideas
- 🖼️ **Meme Formatting**: Classic top/bottom text with proper styling
- 💾 **One-Click Download**: Save your memes as PNG files
- 🎲 **Random Ideas**: Get inspiration with preset meme concepts
- ⚡ **Smart Caching**: Reduces API calls and speeds up generation

## Project Structure

```
ai-meme-generator/
├── main.py              # FastAPI backend with all endpoints
├── index.html           # Frontend interface
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── cache/              # Local image/caption cache
│   ├── images/         # Cached generated images
│   └── captions/       # Cached generated text
└── main.py.backup      # Original template backup
```

## Development

To modify or extend this project:
1. Edit `main.py` to add new API endpoints
2. Update `index.html` for frontend changes
3. The cache system prevents excessive API calls during testing
4. All error handling is built-in for robustness

## Limitations

- Image generation may take 5-10 seconds depending on load
- Free APIs have rate limits (Pollinations.AI has generous free tier)
- Text generation may occasionally produce unexpected results
- Requires internet connection for API calls

## Credits

Built as part of [AI Trendings](https://github.com/tiubak/ai-trendings) — Daily AI projects.

Special thanks to:
- [Pollinations.AI](https://pollinations-ai.com/) for providing free image and text generation APIs
- FastAPI and Pillow communities for excellent libraries

---

**Enjoy creating memes! Share your creations with #AIMemeGenerator 🎭**