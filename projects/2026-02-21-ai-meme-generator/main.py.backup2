#!/usr/bin/env python3
"""
AI Meme Generator
Generate hilarious memes using AI-generated images and witty captions — all for free!

Built for AI Trendings — https://github.com/tiubak/ai-trendings
"""

import asyncio
import hashlib
import io
import json
import os
import time
from pathlib import Path
from typing import Optional, Dict, Any

import aiohttp
import uvicorn
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from PIL import Image, ImageDraw, ImageFont

# Configuration
POLLINATIONS_IMAGE_URL = "https://image.pollinations.ai/prompt/{prompt}"
POLLINATIONS_TEXT_URL = "https://text.pollinations.ai/prompt/{prompt}"
DEFAULT_IMAGE_SIZE = (512, 512)
DEFAULT_MODEL = "flux"
CACHE_DIR = Path("./cache")
CACHE_DIR.mkdir(exist_ok=True)
MAX_CACHE_SIZE = 100  # Max number of cached images

# In-memory cache for quick lookup
image_cache: Dict[str, bytes] = {}
caption_cache: Dict[str, str] = {}

# Initialize FastAPI app
app = FastAPI(
    title="AI Meme Generator",
    description="Generate hilarious memes using AI-generated images and witty captions — all for free!",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Helper functions
def get_hash_key(prompt: str, **kwargs) -> str:
    """Generate a consistent hash key for caching."""
    data = prompt + json.dumps(kwargs, sort_keys=True)
    return hashlib.md5(data.encode()).hexdigest()

async def fetch_pollinations_image(prompt: str, width: int = 512, height: int = 512, model: str = DEFAULT_MODEL) -> bytes:
    """Fetch an image from Pollinations.AI."""
    url = POLLINATIONS_IMAGE_URL.format(prompt=prompt)
    params = {
        "width": width,
        "height": height,
        "model": model,
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params, timeout=30) as response:
            if response.status != 200:
                raise HTTPException(status_code=502, detail="Failed to generate image")
            return await response.read()

async def fetch_pollinations_text(prompt: str) -> str:
    """Fetch generated text from Pollinations.AI."""
    url = POLLINATIONS_TEXT_URL.format(prompt=prompt)
    async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=30) as response:
            if response.status != 200:
                raise HTTPException(status_code=502, detail="Failed to generate text")
            return await response.text()

def add_caption_to_image(image_bytes: bytes, top_text: str = "", bottom_text: str = "") -> bytes:
    """Add captions to an image and return the resulting image bytes."""
    image = Image.open(io.BytesIO(image_bytes))
    # Resize if too large
    if image.size[0] > 1024 or image.size[1] > 1024:
        image.thumbnail((1024, 1024), Image.Resampling.LANCZOS)
    
    draw = ImageDraw.Draw(image)
    # Try to load a font, fallback to default
    try:
        font_size = max(20, image.size[1] // 15)
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
    except:
        font = ImageFont.load_default()
    
    # Function to draw outlined text
    def draw_outlined_text(draw_obj, text, position, font, fill="white", outline="black", outline_width=2):
        x, y = position
        # Draw outline
        for dx in range(-outline_width, outline_width+1):
            for dy in range(-outline_width, outline_width+1):
                draw_obj.text((x+dx, y+dy), text, font=font, fill=outline)
        # Draw main text
        draw_obj.text(position, text, font=font, fill=fill)
    
    if top_text:
        # Position top text centered near the top
        bbox = draw.textbbox((0, 0), top_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (image.size[0] - text_width) // 2
        y = 10
        draw_outlined_text(draw, top_text, (x, y), font)
    
    if bottom_text:
        bbox = draw.textbbox((0, 0), bottom_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (image.size[0] - text_width) // 2
        y = image.size[1] - text_height - 10
        draw_outlined_text(draw, bottom_text, (x, y), font)
    
    # Save to bytes
    output = io.BytesIO()
    image.save(output, format="PNG")
    return output.getvalue()

def save_to_cache(key: str, data: bytes, cache_type: str = "image"):
    """Save data to cache directory and manage cache size."""
    if cache_type == "image":
        cache_subdir = CACHE_DIR / "images"
    else:
        cache_subdir = CACHE_DIR / "captions"
    cache_subdir.mkdir(exist_ok=True)
    
    cache_file = cache_subdir / f"{key}.{'png' if cache_type == 'image' else 'txt'}"
    with open(cache_file, "wb" if cache_type == "image" else "w") as f:
        f.write(data)
    
    # Limit cache size by removing oldest files
    files = list(cache_subdir.iterdir())
    if len(files) > MAX_CACHE_SIZE:
        files.sort(key=lambda x: x.stat().st_mtime)
        for old_file in files[:-MAX_CACHE_SIZE]:
            old_file.unlink()

def load_from_cache(key: str, cache_type: str = "image") -> Optional[bytes]:
    """Load data from cache if exists."""
    if cache_type == "image":
        cache_subdir = CACHE_DIR / "images"
        cache_file = cache_subdir / f"{key}.png"
    else:
        cache_subdir = CACHE_DIR / "captions"
        cache_file = cache_subdir / f"{key}.txt"
    
    if not cache_file.exists():
        return None
    
    with open(cache_file, "rb" if cache_type == "image" else "r") as f:
        data = f.read()
    return data

# API Endpoints
@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the frontend."""
    with open("index.html", "r") as f:
        return f.read()

@app.get("/api/health")
async def health():
    """Health check endpoint."""
    return {"status": "ok", "service": "AI Meme Generator"}

@app.get("/api/generate-image")
async def generate_image(
    prompt: str = Query(..., description="Prompt for image generation"),
    width: int = Query(512, ge=64, le=1024),
    height: int = Query(512, ge=64, le=1024),
    model: str = Query(DEFAULT_MODEL, description="Model to use (flux, openai, etc.)")
):
    """Generate an image based on the prompt."""
    cache_key = get_hash_key(prompt, width=width, height=height, model=model)
    cached = load_from_cache(cache_key, "image")
    if cached:
        return StreamingResponse(io.BytesIO(cached), media_type="image/png")
    
    try:
        image_bytes = await fetch_pollinations_image(prompt, width, height, model)
        save_to_cache(cache_key, image_bytes, "image")
        return StreamingResponse(io.BytesIO(image_bytes), media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/generate-caption")
async def generate_caption(
    prompt: str = Query(..., description="Prompt for caption generation"),
    max_length: int = Query(100, ge=10, le=500)
):
    """Generate a witty caption based on the prompt."""
    cache_key = get_hash_key(prompt, max_length=max_length)
    cached = load_from_cache(cache_key, "caption")
    if cached:
        return JSONResponse({"caption": cached.decode()})
    
    try:
        # Truncate prompt if too long
        if len(prompt) > 200:
            prompt = prompt[:197] + "..."
        caption = await fetch_pollinations_text(prompt)
        # Limit length
        if len(caption) > max_length:
            caption = caption[:max_length-3] + "..."
        save_to_cache(cache_key, caption.encode(), "caption")
        return JSONResponse({"caption": caption})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/create-meme")
async def create_meme(request: Request):
    """Create a meme by combining an image with captions."""
    data = await request.json()
    prompt = data.get("prompt", "")
    top_text = data.get("top_text", "")
    bottom_text = data.get("bottom_text", "")
    width = data.get("width", 512)
    height = data.get("height", 512)
    
    if not prompt and not (top_text or bottom_text):
        raise HTTPException(status_code=400, detail="At least prompt or captions required")
    
    # Generate image if prompt provided
    if prompt:
        cache_key = get_hash_key(prompt, width=width, height=height)
        cached = load_from_cache(cache_key, "image")
        if cached:
            image_bytes = cached
        else:
            try:
                image_bytes = await fetch_pollinations_image(prompt, width, height)
                save_to_cache(cache_key, image_bytes, "image")
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Image generation failed: {e}")
    else:
        # Use a default blank image? For now, generate a generic placeholder
        # Create a simple colored background
        image = Image.new("RGB", (width, height), color=(73, 109, 137))
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        image_bytes = buffer.getvalue()
    
    # Add captions
    try:
        meme_bytes = add_caption_to_image(image_bytes, top_text, bottom_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Caption addition failed: {e}")
    
    return StreamingResponse(io.BytesIO(meme_bytes), media_type="image/png")

@app.get("/api/stats")
async def stats():
    """Get statistics about cache usage."""
    image_cache_files = list((CACHE_DIR / "images").glob("*.png")) if (CACHE_DIR / "images").exists() else []
    caption_cache_files = list((CACHE_DIR / "captions").glob("*.txt")) if (CACHE_DIR / "captions").exists() else []
    return JSONResponse({
        "image_cache_count": len(image_cache_files),
        "caption_cache_count": len(caption_cache_files),
        "total_cache_size_mb": sum(f.stat().st_size for f in image_cache_files + caption_cache_files) / (1024 * 1024)
    })

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)