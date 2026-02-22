#!/usr/bin/env python3
"""
AI Story Illustrator - Generate Illustration Endpoint
POST /api/2026-02-22-ai-story-illustrator/illustrate

Generates an illustration for the story using Pollinations.AI image generation.

Built for AI Trendings — https://github.com/tiubak/ai-trendings
"""

import os
import json
import logging
import random
from http.server import BaseHTTPRequestHandler
from urllib.request import Request, urlopen
from urllib.parse import quote

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

POLLINATIONS_API_KEY = os.getenv("POLLINATIONS_API_KEY", "")

def create_image_prompt(story_text: str, art_style: str = "digital art") -> str:
    """Create a visual prompt from the story text"""
    
    # Extract key elements from story
    words = story_text.split()
    # Take first 20 words for context, avoiding common words
    important_words = [w for w in words[:20] if len(w) > 3][:15]
    context = " ".join(important_words)
    
    style_prompts = {
        "digital art": "digital art, vibrant colors, detailed, trending on artstation",
        "watercolor": "watercolor painting, soft brushstrokes, artistic, dreamy",
        "anime": "anime style, vibrant, detailed, studio ghibli inspired",
        "realistic": "photorealistic, 8k, detailed lighting, professional photography",
        "pixel art": "pixel art, retro gaming style, 16-bit colorful",
        "oil painting": "oil painting, classical art style, rich textures, museum quality"
    }
    
    style_instruction = style_prompts.get(art_style, "digital art, vibrant colors, detailed")
    
    # Create a visual prompt based on story context
    return f"Beautiful illustration of {context}, {style_instruction}, high quality"

def generate_image_url(prompt: str, seed: int = None) -> str:
    """Generate image URL using Pollinations.AI"""
    try:
        # Pollinations.AI image API format
        base_url = "https://image.pollinations.ai/prompt/"
        
        # Add seed for consistency
        if seed is None:
            seed = random.randint(1, 1000000)
        
        # Construct full URL
        encoded_prompt = quote(prompt)
        url = f"{base_url}{encoded_prompt}?seed={seed}&width=1024&height=768&nologo=true"
        
        # Add API key if available
        if POLLINATIONS_API_KEY:
            url += f"&key={POLLINATIONS_API_KEY}"
        
        logger.info(f"Generated image URL with seed {seed}")
        return url
        
    except Exception as e:
        logger.exception(f"Image URL generation error: {e}")
        # Return fallback image URL
        return f"https://image.pollinations.ai/prompt/beautiful%20landscape%20illustration?seed={seed or 42}&width=1024&height=768"

def extract_visual_description(story: str) -> str:
    """Extract visual elements from story for image generation"""
    # Simple heuristic: take sentences with visual keywords
    visual_keywords = ['saw', 'looked', 'watched', 'appeared', 'shone', 'stood', 'dark', 'bright', 
                      'color', 'sky', 'water', 'forest', 'castle', 'house', 'creature', 'light',
                      'moon', 'sun', 'stars', 'ocean', 'mountain', 'city', 'street']
    
    sentences = [s.strip() for s in story.split('.') if s.strip()]
    for sentence in sentences:
        if any(keyword in sentence.lower() for keyword in visual_keywords):
            # Clean up and return first visual sentence
            return sentence[:100]
    
    # Fallback: return first 100 characters
    return story[:100]

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(body) if body else {}
            
            story_text = data.get("story_text", "")
            art_style = data.get("art_style", "digital art")
            seed = data.get("seed")  # Optional seed for reproducibility
            
            if not story_text:
                raise ValueError("story_text is required")
            
            # Extract visual description and create image prompt
            visual_desc = extract_visual_description(story_text)
            image_prompt = create_image_prompt(visual_desc, art_style)
            
            # Generate image URL (Pollinations.AI generates on-demand)
            image_url = generate_image_url(image_prompt, seed)
            
            # Return image URL to client (client will store and display)
            response = {
                "image_url": image_url,
                "image_prompt": image_prompt,
                "art_style": art_style,
                "seed": seed or "random",
                "message": "Illustration generated!"
            }
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
            logger.info(f"Illustration generated: {art_style}")
            
        except Exception as e:
            logger.exception(f"Generate illustration error: {e}")
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
