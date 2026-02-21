#!/usr/bin/env python3
"""
AI Story Illustrator
Transform your short stories into illustrated visual narratives using AI

Built for AI Trendings — https://github.com/tiubak/ai-trendings
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
import urllib.parse
import urllib.request
import json
import re
import asyncio
import aiohttp
from dataclasses import dataclass
from enum import Enum
import logging
import time
from concurrent.futures import ThreadPoolExecutor
import hashlib

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================================================
# CONFIGURATION & CONSTANTS
# ============================================================================

class Config:
    """Application configuration constants"""
    
    # API endpoints
    POLLINATIONS_TEXT_API = "https://text.pollinations.ai/"
    POLLINATIONS_IMAGE_API = "https://image.pollinations.ai/prompt/"
    
    # Rate limiting
    MAX_CONCURRENT_REQUESTS = 5
    REQUEST_TIMEOUT = 60  # seconds
    RETRY_ATTEMPTS = 3
    RETRY_DELAY = 2  # seconds
    
    # Story processing
    MIN_STORY_LENGTH = 50
    MAX_STORY_LENGTH = 2000
    MIN_SCENES = 3
    MAX_SCENES = 6
    
    # Image generation
    IMAGE_WIDTH = 512
    IMAGE_HEIGHT = 512
    IMAGE_SEED_MIN = 1
    IMAGE_SEED_MAX = 999999
    
    # Art styles for illustration
    ART_STYLES = {
        "watercolor": "beautiful watercolor painting style, soft colors, artistic",
        "comic": "comic book style, bold outlines, vibrant colors, graphic novel art",
        "anime": "anime art style, manga illustration, detailed, expressive",
        "realistic": "photorealistic digital art, detailed, cinematic lighting",
        "fantasy": "fantasy art style, magical atmosphere, ethereal, dreamlike",
        "minimalist": "minimalist illustration, clean lines, simple shapes, modern",
        "vintage": "vintage book illustration style, classic art, nostalgic feeling",
        "sketch": "pencil sketch style, hand-drawn look, artistic lines"
    }
    
    # Story genres for context
    GENRES = [
        "fantasy", "science fiction", "romance", "mystery", "adventure",
        "horror", "thriller", "comedy", "drama", "children's story"
    ]


# ============================================================================
# DATA MODELS
# ============================================================================

class ArtStyle(str, Enum):
    """Available art styles for illustration"""
    WATERCOLOR = "watercolor"
    COMIC = "comic"
    ANIME = "anime"
    REALISTIC = "realistic"
    FANTASY = "fantasy"
    MINIMALIST = "minimalist"
    VINTAGE = "vintage"
    SKETCH = "sketch"


class StoryGenre(str, Enum):
    """Story genre options"""
    FANTASY = "fantasy"
    SCIFI = "science fiction"
    ROMANCE = "romance"
    MYSTERY = "mystery"
    ADVENTURE = "adventure"
    HORROR = "horror"
    THRILLER = "thriller"
    COMEDY = "comedy"
    DRAMA = "drama"
    CHILDRENS = "children's story"


@dataclass
class Scene:
    """Represents a single scene from the story"""
    number: int
    original_text: str
    description: str
    image_prompt: str
    image_url: Optional[str] = None
    error: Optional[str] = None


@dataclass
class IllustratedStory:
    """Complete illustrated story with all scenes"""
    title: str
    genre: str
    art_style: str
    scenes: List[Scene]
    processing_time: float
    total_scenes: int
    successful_images: int


class StoryRequest(BaseModel):
    """Request model for story submission"""
    story: str = Field(..., min_length=Config.MIN_STORY_LENGTH, max_length=Config.MAX_STORY_LENGTH)
    art_style: ArtStyle = Field(default=ArtStyle.WATERCOLOR)
    genre: Optional[StoryGenre] = Field(default=None)
    title: Optional[str] = Field(default=None, max_length=100)
    
    @validator('story')
    def validate_story(cls, v):
        """Ensure story has meaningful content"""
        # Remove extra whitespace
        v = ' '.join(v.split())
        # Check for minimum word count
        words = v.split()
        if len(words) < 10:
            raise ValueError(f'Story must have at least 10 words (found {len(words)})')
        return v


class SceneExtractionRequest(BaseModel):
    """Request for extracting scenes from story"""
    story: str
    num_scenes: int = Field(default=4, ge=Config.MIN_SCENES, le=Config.MAX_SCENES)


class ImagePromptRequest(BaseModel):
    """Request for generating image prompt"""
    scene_description: str
    art_style: ArtStyle
    genre: Optional[StoryGenre] = None


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    service: str
    version: str
    features: List[str]


# ============================================================================
# API CLIENTS
# ============================================================================

class PollinationsClient:
    """
    Client for interacting with Pollinations.AI APIs
    Handles both text generation and image generation
    """
    
    def __init__(self, timeout: int = Config.REQUEST_TIMEOUT):
        self.timeout = timeout
        self.session = None
        self._executor = ThreadPoolExecutor(max_workers=Config.MAX_CONCURRENT_REQUESTS)
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session"""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=self.timeout)
            )
        return self.session
    
    async def close(self):
        """Close the aiohttp session"""
        if self.session and not self.session.closed:
            await self.session.close()
    
    async def generate_text(
        self, 
        prompt: str, 
        max_retries: int = Config.RETRY_ATTEMPTS
    ) -> str:
        """
        Generate text using Pollinations.AI text API
        
        Args:
            prompt: The input prompt for text generation
            max_retries: Number of retry attempts on failure
            
        Returns:
            Generated text response
            
        Raises:
            Exception: If all retries fail
        """
        session = await self._get_session()
        last_error = None
        
        for attempt in range(max_retries):
            try:
                logger.info(f"Text generation attempt {attempt + 1}/{max_retries}")
                
                # Prepare the request
                data = {
                    "messages": [
                        {"role": "user", "content": prompt}
                    ],
                    "model": "openai",
                    "seed": int(time.time())  # Add randomness
                }
                
                async with session.post(
                    Config.POLLINATIONS_TEXT_API,
                    json=data,
                    headers={"Content-Type": "application/json"}
                ) as response:
                    if response.status == 200:
                        result = await response.text()
                        logger.info(f"Text generation successful: {len(result)} chars")
                        return result.strip()
                    else:
                        error_text = await response.text()
                        last_error = f"API returned {response.status}: {error_text[:200]}"
                        logger.warning(f"Attempt {attempt + 1} failed: {last_error}")
                        
            except asyncio.TimeoutError:
                last_error = "Request timed out"
                logger.warning(f"Attempt {attempt + 1} timed out")
            except aiohttp.ClientError as e:
                last_error = f"Client error: {str(e)}"
                logger.warning(f"Attempt {attempt + 1} client error: {e}")
            except Exception as e:
                last_error = f"Unexpected error: {str(e)}"
                logger.error(f"Attempt {attempt + 1} unexpected error: {e}")
            
            if attempt < max_retries - 1:
                await asyncio.sleep(Config.RETRY_DELAY * (attempt + 1))
        
        raise Exception(f"Text generation failed after {max_retries} attempts: {last_error}")
    
    def generate_image_url(
        self, 
        prompt: str, 
        width: int = Config.IMAGE_WIDTH,
        height: int = Config.IMAGE_HEIGHT,
        seed: Optional[int] = None
    ) -> str:
        """
        Generate an image URL using Pollinations.AI image API
        
        The URL directly returns an image when accessed, no API call needed.
        This is synchronous because it just constructs a URL.
        
        Args:
            prompt: Image generation prompt
            width: Image width in pixels
            height: Image height in pixels
            seed: Random seed for reproducibility
            
        Returns:
            URL string that will generate the image
        """
        # Use time-based seed if not provided
        if seed is None:
            seed = int(time.time() * 1000) % Config.IMAGE_SEED_MAX
        
        # Enhance prompt for better results
        enhanced_prompt = f"{prompt}, high quality, detailed, {width}x{height}"
        
        # URL encode the prompt
        encoded_prompt = urllib.parse.quote(enhanced_prompt)
        
        # Construct the full URL with parameters
        url = f"{Config.POLLINATIONS_IMAGE_API}{encoded_prompt}"
        url += f"?width={width}&height={height}&seed={seed}&nologo=true"
        
        logger.info(f"Generated image URL for prompt: {prompt[:50]}...")
        return url
    
    async def generate_image_url_async(
        self,
        prompt: str,
        width: int = Config.IMAGE_WIDTH,
        height: int = Config.IMAGE_HEIGHT,
        seed: Optional[int] = None
    ) -> str:
        """Async wrapper for generate_image_url"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            self._executor,
            self.generate_image_url,
            prompt,
            width,
            height,
            seed
        )


# ============================================================================
# STORY PROCESSOR
# ============================================================================

class StoryProcessor:
    """
    Processes stories to extract scenes and generate illustrations
    
    This class handles:
    1. Story analysis and scene extraction
    2. Image prompt generation for each scene
    3. Coordinating parallel image generation
    """
    
    def __init__(self, client: PollinationsClient):
        self.client = client
    
    def extract_title(self, story: str, provided_title: Optional[str] = None) -> str:
        """
        Extract or generate a title for the story
        
        Args:
            story: The full story text
            provided_title: User-provided title (optional)
            
        Returns:
            Story title
        """
        if provided_title:
            return provided_title.strip()
        
        # Try to extract title from first line if it looks like a title
        lines = story.strip().split('\n')
        first_line = lines[0].strip()
        
        # Heuristics for detecting a title
        if len(first_line) < 60 and len(first_line) > 3:
            # Check if it doesn't end with typical sentence punctuation
            if not first_line.endswith(('.', ',', '!', '?')):
                # Check if it's not just continuing the story
                if len(lines) > 1 and lines[1].strip():
                    return first_line
        
        # Generate a title from first few words
        words = story.split()[:6]
        title = ' '.join(words)
        if len(title) > 40:
            title = title[:37] + "..."
        return title
    
    async def extract_scenes_with_ai(
        self, 
        story: str, 
        num_scenes: int = 4
    ) -> List[Dict[str, str]]:
        """
        Use AI to intelligently extract key scenes from the story
        
        Args:
            story: The full story text
            num_scenes: Number of scenes to extract
            
        Returns:
            List of scene dictionaries with 'text' and 'description' keys
        """
        prompt = f"""You are a story analyst. Extract exactly {num_scenes} key visual scenes from this story that would make great illustrations.

For each scene, provide:
1. A brief excerpt from the original story (1-2 sentences)
2. A visual description suitable for an artist to illustrate

Story:
{story}

Respond in this exact JSON format:
{{
    "scenes": [
        {{
            "excerpt": "Original text from story",
            "description": "Visual description for illustration"
        }}
    ]
}}

Extract scenes that show key moments, emotional peaks, or important visual elements. Space them evenly through the story."""

        try:
            response = await self.client.generate_text(prompt)
            
            # Parse JSON response
            # Handle potential markdown code blocks
            json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', response, re.DOTALL)
            if json_match:
                response = json_match.group(1)
            
            # Find JSON object
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                json_str = response[json_start:json_end]
                data = json.loads(json_str)
                return data.get('scenes', [])
            
        except json.JSONDecodeError as e:
            logger.warning(f"Failed to parse AI response as JSON: {e}")
        except Exception as e:
            logger.warning(f"AI scene extraction failed: {e}")
        
        # Fall back to rule-based extraction
        return self._extract_scenes_rule_based(story, num_scenes)
    
    def _extract_scenes_rule_based(
        self, 
        story: str, 
        num_scenes: int
    ) -> List[Dict[str, str]]:
        """
        Fallback: Extract scenes using rule-based approach
        
        Splits story into segments and creates descriptions
        """
        # Split story into sentences
        sentences = re.split(r'(?<=[.!?])\s+', story)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if len(sentences) < num_scenes:
            # If story is too short, duplicate or extend
            while len(sentences) < num_scenes:
                sentences.append(sentences[-1] if sentences else "A mysterious scene unfolds.")
        
        # Calculate segment size
        segment_size = max(1, len(sentences) // num_scenes)
        
        scenes = []
        for i in range(num_scenes):
            start_idx = i * segment_size
            end_idx = start_idx + segment_size if i < num_scenes - 1 else len(sentences)
            
            segment_sentences = sentences[start_idx:end_idx]
            excerpt = ' '.join(segment_sentences[:2])  # Take first 2 sentences as excerpt
            
            # Generate simple description
            description = self._generate_simple_description(excerpt)
            
            scenes.append({
                'excerpt': excerpt,
                'description': description
            })
        
        return scenes
    
    def _generate_simple_description(self, text: str) -> str:
        """
        Generate a simple visual description from text
        
        Uses keyword extraction and pattern matching
        """
        # Common visual elements to look for
        visual_keywords = {
            'characters': ['man', 'woman', 'boy', 'girl', 'child', 'person', 'hero', 
                          'king', 'queen', 'wizard', 'witch', 'dragon', 'knight',
                          'princess', 'prince', 'friend', 'enemy', 'creature'],
            'locations': ['forest', 'castle', 'mountain', 'river', 'sea', 'ocean',
                         'village', 'city', 'house', 'garden', 'cave', 'desert',
                         'island', 'kingdom', 'tower', 'bridge'],
            'actions': ['walking', 'running', 'fighting', 'dancing', 'singing',
                       'flying', 'swimming', 'climbing', 'talking', 'looking',
                       'smiling', 'crying', 'laughing'],
            'moods': ['dark', 'bright', 'mysterious', 'happy', 'sad', 'exciting',
                     'peaceful', 'dangerous', 'magical', 'beautiful'],
            'time': ['night', 'day', 'morning', 'evening', 'sunset', 'sunrise',
                    'midnight', 'dawn', 'dusk']
        }
        
        text_lower = text.lower()
        found_elements = {}
        
        for category, keywords in visual_keywords.items():
            found = [kw for kw in keywords if kw in text_lower]
            if found:
                found_elements[category] = found
        
        # Build description
        parts = []
        
        if 'characters' in found_elements:
            parts.append(f"Featuring {', '.join(found_elements['characters'][:2])}")
        
        if 'locations' in found_elements:
            parts.append(f"in a {found_elements['locations'][0]}")
        
        if 'moods' in found_elements:
            parts.append(f"with a {found_elements['moods'][0]} atmosphere")
        
        if 'time' in found_elements:
            parts.append(f"during {found_elements['time'][0]}")
        
        if 'actions' in found_elements:
            parts.append(f", {found_elements['actions'][0]}")
        
        if parts:
            description = ' '.join(parts)
        else:
            # Generic description based on text
            words = text.split()[:8]
            description = f"A scene showing {' '.join(words)}..."
        
        return description.capitalize()
    
    def create_image_prompt(
        self,
        scene_description: str,
        art_style: ArtStyle,
        genre: Optional[StoryGenre] = None
    ) -> str:
        """
        Create an optimized image generation prompt
        
        Combines scene description with art style and genre context
        to create prompts that produce consistent, high-quality images
        
        Args:
            scene_description: Visual description of the scene
            art_style: Selected art style
            genre: Optional story genre for context
            
        Returns:
            Optimized prompt string
        """
        # Get art style description
        style_desc = Config.ART_STYLES.get(art_style.value, "beautiful illustration")
        
        # Build prompt components
        components = [
            scene_description,
            style_desc
        ]
        
        # Add genre context if available
        if genre:
            genre_context = f"{genre.value} theme"
            components.append(genre_context)
        
        # Add quality enhancers
        quality_enhancers = [
            "highly detailed",
            "professional illustration",
            "vibrant colors" if art_style in [ArtStyle.COMIC, ArtStyle.ANIME] else "soft colors",
            "perfect composition"
        ]
        
        # Combine all components
        main_prompt = ', '.join(components)
        quality_prompt = ', '.join(quality_enhancers[:2])  # Limit to avoid prompt being too long
        
        # Construct final prompt (Pollinations handles longer prompts well)
        final_prompt = f"{main_prompt}, {quality_prompt}"
        
        # Clean up the prompt
        final_prompt = re.sub(r'\s+', ' ', final_prompt)  # Remove extra spaces
        final_prompt = final_prompt.strip()
        
        return final_prompt
    
    async def process_story(
        self,
        story: str,
        art_style: ArtStyle,
        genre: Optional[StoryGenre] = None,
        title: Optional[str] = None,
        num_scenes: int = 4
    ) -> IllustratedStory:
        """
        Process a complete story into an illustrated narrative
        
        This is the main orchestration method that:
        1. Extracts the title
        2. Analyzes and extracts key scenes
        3. Generates image prompts
        4. Creates image URLs for each scene
        
        Args:
            story: The story text
            art_style: Selected art style for illustrations
            genre: Optional story genre
            title: Optional story title
            num_scenes: Number of scenes to create
            
        Returns:
            IllustratedStory object with all scenes and images
        """
        start_time = time.time()
        
        # Extract title
        story_title = self.extract_title(story, title)
        logger.info(f"Processing story: '{story_title}'")
        
        # Extract scenes using AI
        logger.info("Extracting scenes from story...")
        raw_scenes = await self.extract_scenes_with_ai(story, num_scenes)
        
        if not raw_scenes:
            raise ValueError("Failed to extract any scenes from the story")
        
        # Process each scene
        scenes = []
        successful_images = 0
        
        for i, raw_scene in enumerate(raw_scenes[:num_scenes]):
            scene_number = i + 1
            excerpt = raw_scene.get('excerpt', '')
            description = raw_scene.get('description', '')
            
            # If no description, create one from excerpt
            if not description:
                description = self._generate_simple_description(excerpt)
            
            # Create image prompt
            image_prompt = self.create_image_prompt(description, art_style, genre)
            
            # Generate image URL
            # Use different seed for each scene to get variety
            seed = int(time.time() * 1000) + i
            try:
                image_url = self.client.generate_image_url(
                    image_prompt,
                    seed=seed
                )
                successful_images += 1
                error = None
            except Exception as e:
                logger.error(f"Failed to generate image for scene {scene_number}: {e}")
                image_url = None
                error = str(e)
            
            scene = Scene(
                number=scene_number,
                original_text=excerpt,
                description=description,
                image_prompt=image_prompt,
                image_url=image_url,
                error=error
            )
            scenes.append(scene)
            
            # Small delay to prevent rate limiting
            await asyncio.sleep(0.1)
        
        processing_time = time.time() - start_time
        
        # Create the final illustrated story
        illustrated = IllustratedStory(
            title=story_title,
            genre=genre.value if genre else "general",
            art_style=art_style.value,
            scenes=scenes,
            processing_time=processing_time,
            total_scenes=len(scenes),
            successful_images=successful_images
        )
        
        logger.info(f"Story processed in {processing_time:.2f}s with {successful_images}/{len(scenes)} images")
        
        return illustrated


# ============================================================================
# STORY TEMPLATES & EXAMPLES
# ============================================================================

class StoryTemplates:
    """Pre-built story templates for quick demos"""
    
    TEMPLATES = {
        "fantasy": {
            "title": "The Dragon's Last Flight",
            "story": """In the kingdom of Eldoria, an ancient dragon named Pyrrhus lived atop the highest mountain. 
For centuries, the villagers feared him, telling tales of his fiery breath. But young Maya, 
an adventurous girl with curious eyes, dared to climb the mountain one starlit night.

She found the dragon not menacing, but melancholic. His scales, once brilliant gold, 
had faded to dull bronze. "Why are you sad?" Maya asked bravely.

"I am the last of my kind," Pyrrhus replied, his voice like distant thunder. 
"I have no one to share the skies with."

Maya smiled warmly. "Then let me fly with you." And for the first time in a thousand years, 
the dragon soared through the clouds with a friend by his side, painting the night sky 
with streams of golden fire."""
        },
        "adventure": {
            "title": "The Lost Temple",
            "story": """Captain Elena stood at the edge of the jungle, map in hand. The Lost Temple of Zora 
awaited somewhere beyond the vines and ancient trees. Her crew had deserted her, 
fearful of the legends, but she pressed forward alone.

Three days she trekked through the dense forest. Monkeys chattered warnings from above, 
and strange flowers glowed in the twilight. On the fourth dawn, she found it—stone pillars 
wrapped in ivy, a doorway shaped like a serpent's mouth.

Inside, golden light reflected off walls covered in precious gems. But the real treasure 
wasn't gold or jewels. It was the ancient library, preserved for millennia, containing 
wisdom of a civilization long forgotten. Elena smiled, knowing she had found something 
worth more than all the gold in the world."""
        },
        "mystery": {
            "title": "The Midnight Visitor",
            "story": """The old mansion at Willow Lane had been empty for forty years. So when lights 
appeared in the windows one stormy night, the whole town whispered about ghosts.

Detective Sarah Chen didn't believe in ghosts. She believed in facts. Armed with her 
flashlight and determination, she entered through the creaky front door.

Footsteps echoed from upstairs. Someone—or something—was here. Sarah followed the sound 
to the library, where she found an elderly woman reading by candlelight.

"You're the new owner," Sarah realized. "Miriam Blackwood's granddaughter."

The woman smiled. "I came to find what grandmother left behind. A letter, hidden in 
these books, explaining why she vanished all those years ago."

Together, they uncovered the truth: Miriam hadn't disappeared. She had simply chosen 
a new life, and her secret was safe in the mansion all along."""
        }
    }
    
    @classmethod
    def get_template(cls, name: str) -> Optional[Dict[str, str]]:
        """Get a story template by name"""
        return cls.TEMPLATES.get(name.lower())
    
    @classmethod
    def list_templates(cls) -> List[str]:
        """List available template names"""
        return list(cls.TEMPLATES.keys())


# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

# Initialize FastAPI app
app = FastAPI(
    title="AI Story Illustrator",
    description="Transform your short stories into illustrated visual narratives using AI",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize clients
pollinations_client = PollinationsClient()
story_processor = StoryProcessor(pollinations_client)


# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Initialize resources on startup"""
    logger.info("AI Story Illustrator starting up...")
    logger.info(f"Pollinations Text API: {Config.POLLINATIONS_TEXT_API}")
    logger.info(f"Pollinations Image API: {Config.POLLINATIONS_IMAGE_API}")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup resources on shutdown"""
    logger.info("AI Story Illustrator shutting down...")
    await pollinations_client.close()


@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the frontend application"""
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read(), status_code=200)
    except FileNotFoundError:
        return HTMLResponse(
            content="<html><body><h1>Frontend not found</h1></body></html>",
            status_code=404
        )


@app.get("/api/health", response_model=HealthResponse)
async def health():
    """
    Health check endpoint
    
    Returns service status and available features
    """
    return HealthResponse(
        status="ok",
        service="AI Story Illustrator",
        version="1.0.0",
        features=[
            "Story illustration",
            "Multiple art styles",
            "AI scene extraction",
            "Example templates"
        ]
    )


@app.get("/api/styles")
async def get_art_styles():
    """
    Get available art styles
    
    Returns a dictionary of style names and their descriptions
    """
    return {
        "styles": [
            {
                "id": style.value,
                "name": style.value.replace("_", " ").title(),
                "description": Config.ART_STYLES[style.value]
            }
            for style in ArtStyle
        ]
    }


@app.get("/api/genres")
async def get_genres():
    """
    Get available story genres
    
    Returns a list of supported genres
    """
    return {
        "genres": [
            {
                "id": genre.value,
                "name": genre.value.title()
            }
            for genre in StoryGenre
        ]
    }


@app.get("/api/templates")
async def get_templates():
    """
    Get story templates for quick demos
    
    Returns available template names and previews
    """
    templates = []
    for name, data in StoryTemplates.TEMPLATES.items():
        templates.append({
            "id": name,
            "title": data["title"],
            "preview": data["story"][:100] + "..."
        })
    
    return {"templates": templates}


@app.get("/api/templates/{template_id}")
async def get_template(template_id: str):
    """
    Get a specific story template
    
    Args:
        template_id: The template identifier
        
    Returns:
        Template data with title and full story
    """
    template = StoryTemplates.get_template(template_id)
    if not template:
        raise HTTPException(
            status_code=404,
            detail=f"Template '{template_id}' not found"
        )
    
    return template


@app.post("/api/illustrate")
async def illustrate_story(request: StoryRequest):
    """
    Main endpoint: Transform a story into an illustrated narrative
    
    This endpoint:
    1. Validates the story input
    2. Extracts key scenes using AI
    3. Generates image prompts for each scene
    4. Returns the illustrated story with image URLs
    
    Args:
        request: StoryRequest with story text and options
        
    Returns:
        IllustratedStory with scenes and image URLs
    """
    try:
        # Determine number of scenes based on story length
        word_count = len(request.story.split())
        if word_count < 100:
            num_scenes = 3
        elif word_count < 200:
            num_scenes = 4
        else:
            num_scenes = min(5, Config.MAX_SCENES)
        
        # Process the story
        illustrated = await story_processor.process_story(
            story=request.story,
            art_style=request.art_style,
            genre=request.genre,
            title=request.title,
            num_scenes=num_scenes
        )
        
        # Convert to dict for JSON response
        return {
            "success": True,
            "data": {
                "title": illustrated.title,
                "genre": illustrated.genre,
                "art_style": illustrated.art_style,
                "processing_time": round(illustrated.processing_time, 2),
                "total_scenes": illustrated.total_scenes,
                "successful_images": illustrated.successful_images,
                "scenes": [
                    {
                        "number": scene.number,
                        "original_text": scene.original_text,
                        "description": scene.description,
                        "image_prompt": scene.image_prompt,
                        "image_url": scene.image_url,
                        "error": scene.error
                    }
                    for scene in illustrated.scenes
                ]
            }
        }
        
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error processing story: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process story: {str(e)}"
        )


@app.post("/api/extract-scenes")
async def extract_scenes(request: SceneExtractionRequest):
    """
    Extract scenes from a story without generating images
    
    Useful for previewing how the story will be divided
    
    Args:
        request: SceneExtractionRequest with story and num_scenes
        
    Returns:
        List of extracted scenes with descriptions
    """
    try:
        scenes = await story_processor.extract_scenes_with_ai(
            request.story,
            request.num_scenes
        )
        
        return {
            "success": True,
            "scenes": scenes
        }
        
    except Exception as e:
        logger.error(f"Error extracting scenes: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to extract scenes: {str(e)}"
        )


@app.post("/api/generate-prompt")
async def generate_prompt(request: ImagePromptRequest):
    """
    Generate an image prompt from a scene description
    
    Args:
        request: ImagePromptRequest with description and style
        
    Returns:
        Optimized image prompt and preview URL
    """
    try:
        prompt = story_processor.create_image_prompt(
            request.scene_description,
            request.art_style,
            request.genre
        )
        
        url = pollinations_client.generate_image_url(prompt)
        
        return {
            "success": True,
            "prompt": prompt,
            "preview_url": url
        }
        
    except Exception as e:
        logger.error(f"Error generating prompt: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate prompt: {str(e)}"
        )


@app.get("/api/demo")
async def get_demo():
    """
    Get a quick demo with a pre-loaded story
    
    Returns a random template story ready for illustration
    """
    import random
    
    template_names = StoryTemplates.list_templates()
    random_template = random.choice(template_names)
    template = StoryTemplates.get_template(random_template)
    
    return {
        "demo": {
            "template_id": random_template,
            "title": template["title"],
            "story": template["story"],
            "suggested_style": random.choice(list(ArtStyle)).value
        }
    }


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Custom HTTP exception handler"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.detail,
            "status_code": exc.status_code
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """General exception handler for unexpected errors"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "An unexpected error occurred",
            "detail": str(exc) if app.debug else "Internal server error"
        }
    )


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    # Run the server
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
