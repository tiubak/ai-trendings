# AI Name Generator

**Date:** 2026-02-09

Generate perfect names for babies, fictional characters, or businesses using AI.

## What It Does

The AI Name Generator provides three specialized modes:

1. **Baby Names** - Find baby names with meaning, origin, and vibe
2. **Character Names** - Create names for story/game characters with backstory hooks
3. **Business Names** - Generate brandable business names with tagline suggestions

## How to Use

### Baby Name Mode
- Select gender preference (Any, Boy, Girl)
- Optionally specify origin (Irish, Spanish, Greek, etc.)
- Optionally specify meaning preference (strong, peaceful, etc.)
- Optionally add sibling name for compatibility
- Get 5 suggestions with:
  - Name meaning
  - Origin
  - Vibe/feeling (classic, modern, nature-inspired)
  - Sibling compatibility if requested

### Character Name Mode
- Enter archetype: hero, villain, mentor, rogue, etc.
- Choose genre: Fantasy, Sci-fi, Historical, Contemporary
- Select gender
- Get 5 character names with:
  - Full name (with surname/title)
  - Cultural inspiration
  - Story hook (backstory suggestion)
  - Archetype matching explanation

### Business Name Mode
- Enter industry: tech, cafe, fitness, consulting, etc.
- Choose style: Modern, Classic, Playful, Sophisticated
- Optionally add keywords to incorporate
- Get 5 business names with:
  - Memorability score
  - Domain availability hint
  - Tagline suggestion
  - Reasoning behind the name

## API Endpoints

### POST `/api/2026-02-09-ai-name-generator`

#### Action: `baby_name`

Generates baby names.

**Request body:**
```json
{
  "action": "baby_name",
  "gender": "girl",
  "origin": "Greek",
  "meaning_pref": "wise",
  "sibling_name": "Elias"
}
```

**Response:**
```json
{
  "names": [
    {
      "name": "Sophia",
      "gender": "girl",
      "origin": "Greek",
      "meaning": "Wisdom",
      "vibe": "timeless"
    },
    {
      "name": "Athena",
      "gender": "girl",
      "origin": "Greek",
      "meaning": "Goddess of wisdom",
      "vibe": "mythological"
    }
  ],
  "type": "baby",
  "gender": "girl",
  "origin": "Greek"
}
```

#### Action: `character_name`

Generates character names.

**Request body:**
```json
{
  "action": "character_name",
  "archetype": "villain",
  "genre": "fantasy",
  "gender": "male"
}
```

**Response:**
```json
{
  "names": [
    {
      "name": "Malakar",
      "full_name": "Malakar the Voidreaver",
      "archetype_match": "Dark sorcerer villain",
      "cultural_inspiration": "Dark fantasy",
      "story_hook": "Once a promising student of light magic, corrupted by an ancient artifact"
    }
  ],
  "type": "character",
  "archetype": "villain",
  "genre": "fantasy"
}
```

#### Action: `business_name`

Generates business names.

**Request body:**
```json
{
  "action": "business_name",
  "industry": "fitness",
  "style": "modern",
  "keywords": ["strong", "energy", "transform"]
}
```

**Response:**
```json
{
  "names": [
    {
      "name": "TransformStrong",
      "tagline_suggestion": "Transform your strength",
      "memorability_score": 9,
      "domain_available": true,
      "reasoning": "Combines transformation with strength, .com likely available"
    }
  ],
  "type": "business",
  "industry": "fitness",
  "style": "modern"
}
```

## Naming Principles

Our AI considers:

**For Baby Names:**
- Meaning and etymology
- Sibling name harmony
- Cultural appropriateness
- Pronunciation ease
- Popularity trends

**For Character Names:**
- Genre appropriateness
- Cultural inspiration consistency
- Memorability
- Sound and rhythm
- Archetype alignment

**For Business Names:**
- Brandability and memorability
- Domain availability likelihood
- Industry relevance
- Marketing potential
- Scalability

## Use Cases

- **Expectant parents** - Find the perfect baby name
- **Writers** - Generate character names with built-in story hooks
- **Entrepreneurs** - Brainstorm business/startup names
- **Game designers** - Create NPC names
- **Marketers** - Product naming ideation

## Technology

- **Backend**: Python with Pollinations.AI for creative name generation
- **Frontend**: Tabbed interface with card-based result display
- **Features**: Three distinct modes with detailed metadata

## View the Live Project

Visit: https://ai-trendings.vercel.app
