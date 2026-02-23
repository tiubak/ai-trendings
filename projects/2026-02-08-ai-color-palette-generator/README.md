# AI Color Palette Generator

**Date:** 2026-02-08

Generate beautiful, harmonious color palettes using AI - from moods, keywords, or base colors.

## What It Does

The AI Color Palette Generator creates color schemes in three ways:

1. **From Mood** - Describe an emotion or atmosphere (calm, energetic, mysterious)
2. **From Keyword** - Enter any word (ocean, sunrise, forest) for inspiration
3. **Harmonious Colors** - Start with a base color and get a cohesive palette

All palettes include:
- Hex codes (copy-ready)
- RGB values
- Descriptive color names
- Usage tips
- Harmony explanations

## How to Use

### From Mood
1. Enter a mood: calm, energetic, joyful, mysterious, confident, etc.
2. Choose palette size (3-5 colors)
3. Click "Generate Palette"
4. Get colors that evoke that emotion

### From Keyword
1. Enter a keyword: ocean, forest, city, coffee, etc.
2. Choose a style: Modern, Vintage, Minimalist, Bold
3. Get a themed palette with best use cases

### Harmonious Colors
1. Enter a base color hex (e.g., #3498DB)
2. Get 4 harmonious colors (complementary, analogous, or triadic)
3. See scheme type and contrast info for accessibility

Features:
- **Click-to-copy** - Click any color swatch to copy its hex code
- **Visual display** - Large color swatches with information
- **Usage guidance** - Tips on how to apply each palette

## API Endpoints

### POST `/api/2026-02-08-ai-color-palette-generator`

#### Action: `from_mood`

Generates palette from mood.

**Request body:**
```json
{
  "action": "from_mood",
  "mood": "calm",
  "palette_size": 5
}
```

**Response:**
```json
{
  "palette": {
    "palette": [
      {
        "name": "Ocean Serenity",
        "hex": "#87CEEB",
        "rgb": "135,206,235",
        "description": "Peaceful sky blue, primary calming tone"
      },
      {
        "name": "Gentle Waves",
        "hex": "#98D8C8",
        "rgb": "152,216,200",
        "description": "Soothing teal accent"
      }
    ],
    "overall_mood": "calm",
    "usage_tip": "Use these colors to create a tranquility-focused design. Blues and soft greens promote relaxation."
  },
  "mood": "calm",
  "size": 5
}
```

#### Action: `from_keyword`

Generates palette from keyword.

**Request body:**
```json
{
  "action": "from_keyword",
  "keyword": "sunset",
  "style": "modern"
}
```

**Response:**
```json
{
  "palette_data": {
    "keyword": "sunset",
    "style": "modern",
    "palette": [
      {"name": "Sunset Orange", "hex": "#FF6B6B", "meaning": "Warmth and energy of setting sun"},
      {"name": "Golden Hour", "hex": "#FFD93D", "meaning": "Golden light"},
      {"name": "Purple Haze", "hex": "#C56CF0", "meaning": "Twilight transition"},
      {"name": "Dusk Blue", "hex": "#4ECDC4", "meaning": "Cool evening sky"}
    ],
    "total_vibe": "A vibrant, warm palette capturing sunset's beauty",
    "best_use_cases": ["Branding for summer products", "Travel websites", "Warm cozy themes"]
  },
  "keyword": "sunset",
  "style": "modern"
}
```

#### Action: `harmonious`

Generates harmonious colors from base.

**Request body:**
```json
{
  "action": "harmonious",
  "base_color": "#3498DB"
}
```

**Response:**
```json
{
  "harmony": {
    "base_color": "#3498DB",
    "scheme_type": "analogous",
    "palette": [
      {"name": "Base Blue", "hex": "#3498DB", "role": "base", "harmony_explanation": "Your primary color"},
      {"name": "Sky Light", "hex": "#5DADE2", "role": "complementary", "harmony_explanation": "Lighter adjacent hue"},
      {"name": "Ocean Deep", "hex": "#2E86C1", "role": "accent1", "harmony_explanation": "Deeper variation"}
    ],
    "contrast_ratio": "AA"
  },
  "base": "#3498DB"
}
```

## Color Theory

Our AI draws on color theory principles:

- **Mood-based**: Colors evoke specific emotions (blue=calm, red=energy)
- **Keyword inspiration**: Natural and conceptual word associations
- **Harmony schemes**:
  - **Analogous** - colors next to each other on color wheel (harmonious)
  - **Complementary** - colors opposite on wheel (high contrast)
  - **Triadic** - three evenly spaced colors (vibrant)
  - **Tetradic** - four colors forming rectangle (rich)

## Accessibility

The harmonious generator considers WCAG contrast ratios. When using palettes:
- Ensure text/background contrast meets AA/AAA standards
- Test with color blindness simulators
- Don't rely solely on color to convey information

## Use Cases

- **Web design** - generate site color schemes
- **Branding** - create brand palettes
- **UI/UX** - design interface colors
- **Interior design** - paint and decor inspiration
- **Art projects** - painting and digital art
- **Marketing** - presentation and slide decks

## Technology

- **Backend**: Python with Pollinations.AI for creative color generation
- **Frontend**: Interactive with click-to-copy hex codes
- **Visual**: Large swatches with hover effects, harmony info

## View the Live Project

Visit: https://ai-trendings.vercel.app
