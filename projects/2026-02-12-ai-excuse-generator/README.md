# AI Excuse Generator

**Date:** 2026-02-12

Generate plausible (and funny) excuses for canceling plans, missing events, or getting out of commitments.

## What It Does

The AI Excuse Generator provides three types of excuses:

1. **General** - Tailored to situation, audience, and credibility level
2. **Professional** - Work-appropriate, socially acceptable excuses
3. **Funny** - Absurd, humorous excuses for texting friends

All excuses include:
- Credibility/professionalism ratings
- Risk assessment
- Delivery tips
- Backup stories/variations
- Warnings about overuse

## How to Use

### General Mode
- Describe your situation (e.g., "cancel dinner", "miss birthday party")
- Choose audience: Casual, Formal, or Romantic
- Select credibility: Reasonable, Highly Plausible, or Borderline
- Get a tailored excuse with timing advice and backup details

### Professional Mode
- Optionally specify profession (tailors to workplace norms)
- Optionally specify reason needed (leaving early, missing deadline, etc.)
- Get work-safe excuse with delivery tips and alternative phrasings

### Funny Mode
- Choose absurdity level: Mild, Moderate, or Extreme
- Get ridiculous excuses meant for friends only
- Includes suggested emojis and follow-up lines

## ⚠️ Ethical Note

Excuses can harm trust when overused or used for serious matters. This tool is intended for:
- Light social situations (rescheduling casual plans)
- Breaking tension with humor
- Creative writing scenarios

**Not for**:
- Workplace discipline avoidance
- Breaking serious commitments
- Deception in relationships
- Legal/medical excuses

Honesty remains the best policy for important matters.

## API Endpoints

### POST `/api/2026-02-12-ai-excuse-generator`

#### Action: `generate`

General excuse generator.

**Request body:**
```json
{
  "action": "generate",
  "situation": "canceling dinner last minute",
  "audience": "casual",
  "credibility": "reasonable"
}
```

**Response:**
```json
{
  "excuse": {
    "excuse": "I'm not feeling well and need to rest.",
    "credibility_level": 6,
    "social_risk": "low",
    "when_to_use": "Canceling any casual social plans",
    "backup_story": "Started feeling dizzy after work.",
    "warning": "Weak excuse if used repeatedly. People will notice pattern."
  },
  "situation": "canceling dinner last minute",
  "audience": "casual"
}
```

#### Action: `socially_acceptable`

Professional/work-appropriate excuses.

**Request body:**
```json
{
  "action": "socially_acceptable",
  "profession": "software developer",
  "reason_needed": "leaving early"
}
```

**Response:**
```json
{
  "excuse": {
    "excuse": "I have a personal appointment that cannot be rescheduled.",
    "professionalism_score": 9,
    "appropriate_for_work": true,
    "delivery_tip": "Be vague but confident. Don't over-apologize or over-explain.",
    "alternative_phrasings": ["I need to step out for a personal matter", "I have a necessary commitment"],
    "why_it_works": "Unspecific but professional; people respect boundaries and privacy."
  },
  "profession": "software developer",
  "reason": "leaving early"
}
```

#### Action: `funny`

Humorous absurd excuses.

**Request body:**
```json
{
  "action": "funny",
  "absurdity_level": "moderate"
}
```

**Response:**
```json
{
  "excuse": {
    "excuse": "My cat has declared a national holiday and I'm required to observe it.",
    "laugh_factor": 8,
    "absurdity_score": 9,
    "best_for": "Close friends who know you well enough to get the joke",
    "straight_man_alternative": "Yes, he's very serious about his holidays.",
    "emoji_suggestions": ["🐱", "🎉", "😅"]
  },
  "absurdity_level": "moderate"
}
```

## Excuse Psychology

**Why excuses exist:**
- Save face and maintain social relationships
- Avoid revealing uncomfortable truths
- Manage others' expectations
- Provide face-saving exits from commitments

**Good excuses:**
- Are plausible (could actually happen)
- Are specific enough to be believable, vague enough to avoid scrutiny
- Match the audience's expectations
- Include backup details if pressed
- Are used sparingly

**Bad excuses:**
- Are obviously false
- Are too complicated (hard to remember)
- Contradict known facts
- Overused (people catch patterns)
- Cast blame on others unnecessarily

## Technology

- **Backend**: Python with Pollinations.AI
- **Frontend**: Dark theme with red accents, emphasis on risk/credibility bars
- **Features**: Three modes, scoring systems, professional filtering

## View the Live Project

Visit: https://ai-trendings.vercel.app
