#!/usr/bin/env python3
"""
AI Dungeon Master - Interactive Text Adventure Game
An AI-powered dungeon master that generates immersive storylines, characters, and choices in real-time.

Built for AI Trendings — https://github.com/tiubak/ai-trendings

REFACTORED: Now uses Pollinations.AI for BOTH text and images (no API keys needed)
"""

import os
import logging
import uuid
import json
import asyncio
from typing import Optional, Dict, List, Any
from fastapi import FastAPI, Request, HTTPException, BackgroundTasks
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import httpx

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Environment variables (set on Vercel)
POLLINATIONS_API_KEY = os.getenv("POLLINATIONS_API_KEY", "")
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY", "")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")

# Pollinations.AI settings (NO API KEY REQUIRED!)
POLLINATIONS_API_URL = "https://gen.pollinations.ai"
POLLINATIONS_TEXT_API_URL = "https://text.pollinations.ai"

# Game state storage (in-memory, for demo purposes)
games: Dict[str, Dict[str, Any]] = {}

# Pydantic models for request/response validation
class GameStartRequest(BaseModel):
    theme: str = Field(default="fantasy", description="Game theme: fantasy, sci-fi, horror, mystery")
    player_name: Optional[str] = Field(default="Adventurer", description="Player's character name")

class ChoiceRequest(BaseModel):
    choice_index: int = Field(ge=0, le=2, description="Index of selected choice (0-2)")

class ImageGenRequest(BaseModel):
    prompt: Optional[str] = Field(default=None, description="Optional custom prompt for image generation")

# FastAPI app
app = FastAPI(
    title="AI Dungeon Master",
    description="An AI-powered interactive text adventure game that generates stories and images in real-time",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Helper functions
async def generate_text_pollinations(prompt: str, max_length: int = 300) -> str:
    """Generate text using Pollinations.AI text API (NO API KEY NEEDED!)"""
    try:
        # Build URL for Pollinations.AI text API
        prompt_encoded = prompt.replace(" ", "%20")
        url = f"{POLLINATIONS_TEXT_API_URL}/{prompt_encoded}"
        
        # Add API key if available (optional for Pollinations.AI)
        headers = {}
        if POLLINATIONS_API_KEY:
            headers["Authorization"] = f"Bearer {POLLINATIONS_API_KEY}"
        
        logger.info(f"Generating text with Pollinations.AI: {prompt[:50]}...")
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers, timeout=30.0, follow_redirects=True)
            
            if response.status_code == 200:
                # Pollinations.AI returns plain text
                generated_text = response.text.strip()
                logger.info("Text generated successfully via Pollinations.AI")
                return generated_text
            else:
                error_text = response.text
                logger.error(f"Pollinations.AI text API error {response.status_code}: {error_text}")
                raise HTTPException(
                    status_code=502,
                    detail=f"The oracle whispers riddles... (Text generation failed)"
                )
    
    except Exception as e:
        logger.exception(f"Text generation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Mysterious fog obscures path... (Error: {str(e)})")

async def generate_image_pollinations(prompt: str, width: int = 512, height: int = 512) -> str:
    """Generate image using Pollinations.AI image API (NO API KEY NEEDED!)"""
    try:
        # Build URL with parameters
        prompt_encoded = prompt.replace(" ", "%20")
        url = f"{POLLINATIONS_API_URL}/prompt/{prompt_encoded}"
        params = {
            "width": width,
            "height": height,
            "model": "flux",  # Using Flux model
            "nologo": "true",  # Optional: don't add watermark
        }
        
        # Add API key if available
        headers = {}
        if POLLINATIONS_API_KEY:
            params["key"] = POLLINATIONS_API_KEY
        
        logger.info(f"Generating image with Pollinations.AI: {prompt[:50]}...")
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params, headers=headers, timeout=30.0, follow_redirects=True)
            
            if response.status_code == 200:
                # Pollinations.AI returns the image directly
                # We return the URL (Vercel/clients will fetch it)
                image_url = str(response.url)
                logger.info(f"Image generated: {image_url[:60]}...")
                return image_url
            else:
                error_text = response.text
                logger.error(f"Pollinations.AI image API error {response.status_code}: {error_text}")
                raise HTTPException(
                    status_code=502,
                    detail=f"The ancient magic fails... (Image generation failed)"
                )
    
    except Exception as e:
        logger.exception(f"Image generation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Darkness consumes all... (Error: {str(e)})")

def parse_scene_and_choices(text: str) -> tuple[str, List[str]]:
    """Parse generated text into scene description and choices"""
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    # Look for markers like "Choices:" or numbered choices
    scene_lines = []
    choices = []
    in_choices = False
    
    for line in lines:
        lower_line = line.lower()
        if lower_line.startswith(("choices:", "options:", "choose:")):
            in_choices = True
            continue
        
        if in_choices:
            # Extract numbered choices (1., 2., etc.)
            if line and line[0].isdigit() and (". " in line or ")" in line):
                choice_text = line.split(". ", 1)[-1] if ". " in line else line.split(") ", 1)[-1]
                choices.append(choice_text)
            elif line and line.startswith("- "):
                choices.append(line[2:])
            elif line:
                # If we're in choices section but no marker, treat as choice
                choices.append(line)
        else:
            scene_lines.append(line)
    
    scene = "\n".join(scene_lines)
    
    # If no choices parsed, create some default ones
    if not choices:
        choices = [
            "Explore the dark corridor ahead",
            "Investigate the strange artifact",
            "Rest and regain your strength"
        ]
    
    # Ensure we have exactly 3 choices
    while len(choices) < 3:
        choices.append(f"Option {len(choices)+1}: Continue journey")
    
    return scene[:500], choices[:3]

def create_initial_prompt(theme: str, player_name: str) -> str:
    """Create prompt for initial scene generation"""
    themes = {
        "fantasy": "a high fantasy dungeon with magical creatures and ancient ruins",
        "sci-fi": "a futuristic spaceship or alien planet with advanced technology",
        "horror": "a haunted mansion or cursed forest with supernatural elements",
        "mystery": "a mysterious crime scene or enigmatic puzzle to solve"
    }
    
    setting = themes.get(theme, themes["fantasy"])
    
    return f"""You are an expert dungeon master running a text adventure game. The player '{player_name}' is starting a new adventure in {setting}.

Generate an opening scene with vivid description (2-3 paragraphs). Then provide exactly 3 choices for the player.

Format:
[Scene description here]

Choices:
1. [First choice]
2. [Second choice]
3. [Third choice]

Scene:"""

# API Endpoints
@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve frontend"""
    with open("index.html", "r") as f:
        return f.read()

@app.get("/api/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "ok",
        "service": "AI Dungeon Master",
        "env_vars": {
            "pollinations": bool(POLLINATIONS_API_KEY),
            "huggingface": bool(HUGGINGFACE_API_KEY),
            "openrouter": bool(OPENROUTER_API_KEY)
        },
        "apis_available": {
            "text_generation": "Pollinations.AI (no key needed)",
            "image_generation": "Pollinations.AI (no key needed)"
        }
    }

@app.post("/api/game/start")
async def start_game(request: GameStartRequest, background_tasks: BackgroundTasks):
    """Start a new game"""
    game_id = str(uuid.uuid4())
    
    # Generate initial scene
    prompt = create_initial_prompt(request.theme, request.player_name)
    
    try:
        generated_text = await generate_text_pollinations(prompt)
        scene, choices = parse_scene_and_choices(generated_text)
        
        # Create game state
        game_state = {
            "game_id": game_id,
            "theme": request.theme,
            "player_name": request.player_name,
            "current_scene": scene,
            "choices": choices,
            "history": [{"scene": scene, "choices": choices, "selected_choice": None}],
            "image_url": None,
            "created_at": asyncio.get_event_loop().time(),
            "last_updated": asyncio.get_event_loop().time()
        }
        
        games[game_id] = game_state
        
        # Generate image in background
        async def generate_initial_image():
            image_prompt = f"{scene[:100]}, {request.theme} adventure, digital art, dramatic lighting"
            image_url = await generate_image_pollinations(image_prompt)
            if image_url:
                games[game_id]["image_url"] = image_url
        
        background_tasks.add_task(generate_initial_image)
        
        return {
            "game_id": game_id,
            "scene": scene,
            "choices": choices,
            "theme": request.theme,
            "player_name": request.player_name,
            "message": "Game started! Your adventure begins..."
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Failed to start game: {e}")
        raise HTTPException(status_code=500, detail=f"An ancient force awakens... (Error: {str(e)})")

@app.get("/api/game/{game_id}")
async def get_game_state(game_id: str):
    """Get current game state"""
    if game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")
    
    game = games[game_id]
    return {
        "game_id": game_id,
        "scene": game["current_scene"],
        "choices": game["choices"],
        "theme": game["theme"],
        "player_name": game["player_name"],
        "image_url": game["image_url"],
        "history_count": len(game["history"])
    }

@app.post("/api/game/{game_id}/choice")
async def make_choice(game_id: str, choice: ChoiceRequest, background_tasks: BackgroundTasks):
    """Make a choice and advance the story"""
    if game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")
    
    game = games[game_id]
    
    if choice.choice_index >= len(game["choices"]):
        raise HTTPException(status_code=400, detail="Invalid choice index")
    
    selected_choice = game["choices"][choice.choice_index]
    
    # Update history
    game["history"][-1]["selected_choice"] = selected_choice
    
    # Generate next scene based on choice
    prompt = f"""As a dungeon master, continue to story based on this context:

Previous scene: {game['current_scene']}
Player's choice: {selected_choice}

Generate a next scene (2-3 paragraphs) showing the consequences of this choice. Then provide exactly 3 new choices for the player.

Format:
[Scene description here]

Choices:
1. [First choice]
2. [Second choice]
3. [Third choice]

Scene:"""
    
    try:
        generated_text = await generate_text_pollinations(prompt)
        new_scene, new_choices = parse_scene_and_choices(generated_text)
        
        # Update game state
        game["current_scene"] = new_scene
        game["choices"] = new_choices
        game["history"].append({
            "scene": new_scene,
            "choices": new_choices,
            "selected_choice": None
        })
        game["last_updated"] = asyncio.get_event_loop().time()
        
        # Generate new image in background
        async def generate_next_image():
            image_prompt = f"{new_scene[:100]}, {game['theme']} adventure, digital art, dramatic lighting"
            image_url = await generate_image_pollinations(image_prompt)
            if image_url:
                game["image_url"] = image_url
        
        background_tasks.add_task(generate_next_image)
        
        return {
            "game_id": game_id,
            "scene": new_scene,
            "choices": new_choices,
            "selected_choice": selected_choice,
            "message": "The story continues..."
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Failed to make choice: {e}")
        raise HTTPException(status_code=500, detail=f"The dungeon master's power wanes... (Error: {str(e)})")

@app.post("/api/game/{game_id}/image")
async def generate_scene_image(game_id: str, request: ImageGenRequest = None):
    """Generate or regenerate image for current scene"""
    if game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")
    
    game = games[game_id]
    
    prompt = request.prompt if request.prompt else f"{game['current_scene'][:100]}, {game['theme']} adventure, digital art, dramatic lighting"
    image_url = await generate_image_pollinations(prompt)
    
    if image_url:
        game["image_url"] = image_url
        return {"image_url": image_url, "message": "Image generated successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to generate image")

@app.get("/api/game/{game_id}/history")
async def get_game_history(game_id: str):
    """Get full game history"""
    if game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")
    
    return {
        "game_id": game_id,
        "history": games[game_id]["history"]
    }

@app.delete("/api/game/{game_id}")
async def end_game(game_id: str):
    """End and remove a game"""
    if game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")
    
    del games[game_id]
    return {"message": "Game ended successfully"}

@app.get("/api/game/{game_id}/export")
async def export_game(game_id: str):
    """Export game as JSON story"""
    if game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")
    
    game = games[game_id]
    export_data = {
        "title": f"{game['theme'].title()} Adventure - {game['player_name']}'s Journey",
        "player": game["player_name"],
        "theme": game["theme"],
        "chapters": []
    }
    
    for i, entry in enumerate(game["history"]):
        chapter = {
            "chapter": i + 1,
            "scene": entry["scene"],
            "choices": entry["choices"],
            "selected_choice": entry["selected_choice"]
        }
        export_data["chapters"].append(chapter)
    
    return export_data

# Cleanup old games (runs periodically)
async def cleanup_old_games():
    """Remove games older than 24 hours"""
    current_time = asyncio.get_event_loop().time()
    expired_games = []
    
    for game_id, game in games.items():
        if current_time - game["last_updated"] > 86400:  # 24 hours
            expired_games.append(game_id)
    
    for game_id in expired_games:
        del games[game_id]
    
    if expired_games:
        logger.info(f"Cleaned up {len(expired_games)} expired games")

@app.on_event("startup")
async def startup_event():
    """Initialize on startup"""
    logger.info("Starting AI Dungeon Master...")
    logger.info("Environment variables configured:")
    logger.info(f"  - POLLINATIONS_API_KEY: {bool(POLLINATIONS_API_KEY)}")
    logger.info(f"  - HUGGINGFACE_API_KEY: {bool(HUGGINGFACE_API_KEY)}")
    logger.info(f"  - OPENROUTER_API_KEY: {bool(OPENROUTER_API_KEY)}")
    
    logger.info("✓ REFACTORED: Now using Pollinations.AI for BOTH text and images (no API keys needed)")
    logger.info("  Text API: Pollinations.AI text.pollinations.ai (no key)")
    logger.info("  Image API: Pollinations.AI gen.pollinations.ai (no key)")
    
    # Schedule periodic cleanup
    asyncio.create_task(periodic_cleanup())

async def periodic_cleanup():
    """Run cleanup every hour"""
    while True:
        await asyncio.sleep(3600)
        await cleanup_old_games()

if __name__ == "__main__":
    import uvicorn
    import sys
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
