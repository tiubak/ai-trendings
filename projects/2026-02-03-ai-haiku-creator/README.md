# AI Haiku Creator

**Date:** 2026-02-03

Generate beautiful Japanese-inspired haiku poetry with AI, customize them, or create from seasonal themes.

## What It Does

The AI Haiku Creator offers three ways to generate poetry:

1. **Create** - Generate a haiku with custom theme, mood, and style (traditional 5-7-5 or modern free-form)
2. **Customize** - Take an existing haiku and modify it according to your requests
3. **Generate from Theme** - Create haiku based on specific nature elements (season, time of day, natural element)

Each haiku includes:
- The poem itself (preserving line breaks)
- Syllable structure (5-7-5 or free-form)
- Theme and mood indicators
- Explanation of the imagery and feeling

## How to Use

### Option 1: Create Your Own
- Enter a theme or topic (optional)
- Choose a mood (optional)
- Select traditional or modern style
- Click "Generate Haiku"

### Option 2: Generate by Nature Theme
- Click "Generate by Nature Theme"
- The AI will randomly select a season, time of day, and natural element
- Get a nature-inspired haiku with full sensory details

### Option 3: Customize
- After generating a haiku, click "Customize This Haiku"
- Describe how you want to modify it (e.g., "make it more hopeful", "change to winter imagery")
- Get a refined version with change notes

## API Endpoints

### POST `/api/2026-02-03-ai-haiku-creator`

#### Action: `create`

Generates a new haiku.

**Request body:**
```json
{
  "action": "create",
  "theme": "sunset",
  "mood": "peaceful",
  "style": "traditional"
}
```

**Response:**
```json
{
  "haiku": {
    "haiku": "Golden sun dips low\nHorizon blazes with fire\nDay surrenders",
    "syllables": "5-7-5",
    "theme": "sunset",
    "mood": "peaceful",
    "explanation": "This haiku captures the tranquil beauty of a sunset..."
  },
  "theme": "sunset",
  "mood": "peaceful",
  "style": "traditional"
}
```

#### Action: `customize`

Modifies an existing haiku.

**Request body:**
```json
{
  "action": "customize",
  "original_haiku": "Golden sun dips low\nHorizon blazes with fire\nDay surrenders",
  "modification": "Change to a more melancholic mood with autumn imagery"
}
```

**Response:**
```json
{
  "customized": {
    "haiku": "Crimson leaves descend\nCold wind whispers through bare trees\nSummer's ghost fades",
    "modifications_made": ["Changed imagery from sunset to autumn", "Shifted mood to melancholic", "Replaced warm colors with cold"],
    "why_it_fits": "The modified haiku captures autumn's sense of loss and transition..."
  },
  "original": "...",
  "modification_request": "..."
}
```

#### Action: `generate_from_theme`

Creates haiku from natural themes.

**Request body:**
```json
{
  "action": "generate_from_theme",
  "season": "spring",
  "time_of_day": "dawn",
  "element": "cherry blossoms"
}
```

**Response:**
```json
{
  "haiku": {
    "haiku": "First light touches pink\nPetals drift on morning breeze\nSpring awakes softly",
    "imagery": "Dawn light illuminating pink cherry blossoms drifting on a gentle wind",
    "sensory_details": ["Pink petals in vision", "Cool morning air", "Soft rustling sound"],
    "seasonal_kigo": "cherry blossoms (spring)",
    "emotional_essence": "Delicate renewal and gentle awakening"
  },
  "season": "spring",
  "time": "dawn",
  "element": "cherry blossoms"
}
```

## About Haiku

A traditional haiku follows the 5-7-5 syllable pattern across three lines, often incorporating:
- A **kigo** (seasonal reference)
- A **kireji** (cutting word) that creates a pause
- Nature imagery that evokes an emotional response

Our AI can create both traditional and modern haiku. Traditional haiku aim to capture a moment in nature and include seasonal references. Modern haiku may be more free-form while still evoking the haiku spirit.

## Technology

- **Backend**: Python with Pollinations.AI text generation
- **Frontend**: Bright, nature-inspired gradient theme
- **Features**: Multiple generation modes, customization, thematic exploration

## View the Live Project

Visit: https://ai-trendings.vercel.app
