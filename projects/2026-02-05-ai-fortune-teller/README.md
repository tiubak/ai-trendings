# AI Fortune Teller

**Date:** 2026-02-05

Peer into the mystical orb and receive AI-generated fortunes, horoscopes, and destiny readings.

## What It Does

The AI Fortune Teller offers three divination methods:

1. **Quick Fortune** - Personalized message with lucky numbers, colors, elements, and guidance
2. **Daily Horoscope** - Complete zodiac horoscope with love, career, health, and more
3. **Destiny Reading** - Life path analysis based on birth date with soul purpose and challenges

All readings are AI-generated and include mystical, inspirational content with actionable guidance.

## How to Use

### Quick Fortune
1. Enter your name (required)
2. Optionally ask a specific question
3. Choose a focus area (General, Love, Career, Health, Spiritual)
4. Click "Reveal My Fortune"
5. Receive your personalized fortune with:
   - Main fortune message
   - Lucky number and color
   - Lucky element
   - Omen rating
   - Planetary influence
   - Personal guidance

### Daily Horoscope
1. Click on your zodiac sign from the grid
2. Click "Reveal My Fortune"
3. Get your daily reading with:
   - Overview
   - Love advice
   - Career/finance guidance
   - Health & wellness tips
   - Lucky time of day
   - Compatibility with another sign
   - Caution for the day

### Destiny Reading
1. Enter your birth month (1-12) and year
2. Optionally ask a life question
3. Click "Reveal My Fortune"
4. Receive a comprehensive destiny analysis:
   - Life path number
   - Chinese zodiac animal
   - Element (fire, earth, air, water)
   - Core trait
   - Soul purpose
   - Life challenge
   - Natural gift
   - Decade theme
   - Personalized advice

## API Endpoints

### POST `/api/2026-02-05-ai-fortune-teller`

#### Action: `tell_fortune`

Quick personalized fortune.

**Request body:**
```json
{
  "action": "tell_fortune",
  "user_name": "Morgan",
  "question": "Will I find love this year?",
  "focus_area": "love"
}
```

**Response:**
```json
{
  "fortune": {
    "fortune": "The stars whisper of a connection forming under a silver moon...",
    "lucky_number": 23,
    "lucky_color": "deep crimson",
    "lucky_element": "fire",
    "omen": "favorable",
    "guidance": "Be open to unexpected encounters - romance finds you when you're not looking.",
    "planetary_influence": "Venus in harmonious trine to your natal chart"
  },
  "name": "Morgan",
  "question": "Will I find love this year?",
  "focus": "love"
}
```

#### Action: `daily_horoscope`

Full daily horoscope.

**Request body:**
```json
{
  "action": "daily_horoscope",
  "zodiac_sign": "Libra"
}
```

**Response:**
```json
{
  "horoscope": {
    "sign": "Libra",
    "date": "February 5, 2026",
    "overview": "Cosmic energies amplify your natural diplomacy...",
    "love": "Communication flows smoothly with your partner...",
    "career": "A collaborative project brings recognition...",
    "health": "Balance is key - remember to rest...",
    "lucky_time": "early evening",
    "compatibility": " Gemini",
    "caution": "Avoid overcommitting to social events"
  },
  "sign": "Libra"
}
```

#### Action: `destiny_reading`

Life path reading based on birth date.

**Request body:**
```json
{
  "action": "destiny_reading",
  "birth_month": 7,
  "birth_year": 1990,
  "life_question": "What is my purpose?"
}
```

**Response:**
```json
{
  "reading": {
    "life_path_number": 7,
    "zodiac_animal": "Horse",
    "element": "fire",
    "core_trait": "Seeker of truth",
    "soul_purpose": "To explore knowledge and share wisdom with others.",
    "challenge": "Learning to trust intuition over logic",
    "gift": "Deep analytical insight",
    "decade_theme": "Spiritual awakening and teaching",
    "advice": "Your quest for understanding is your greatest strength."
  },
  "birth_month": 7,
  "birth_year": 1990,
  "question": "What is my purpose?"
}
```

## About Fortune Telling

These AI-generated readings are for entertainment and inspiration. They combine elements from various mystical traditions (Western astrology, Chinese zodiac, numerology) with creative AI interpretation.

**Remember**: You have free will. Use these readings as prompts for self-reflection, not as deterministic predictions. Your choices shape your destiny.

## Mystical Elements Explained

- **Life Path Number**: Numerological calculation from birth date (single digit or master numbers 11, 22, 33)
- **Zodiac Animal**: Chinese zodiac based on birth year (12-year cycle)
- **Element**: Associated with both Western and Chinese elemental systems
- **Omen**: General fortune indication (favorable/neutral/challenging)

## Technology

- **Backend**: Python with Pollinations.AI, custom mystical prompt engineering
- **Frontend**: Dark mystical theme with glowing crystal ball effect
- **Modes**: Three distinct reading types with appropriate visual styling

## View the Live Project

Visit: https://ai-trendings.vercel.app
