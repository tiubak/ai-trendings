# AI Story Starter

**Date:** 2026-02-15

Kickstart your writing with AI-generated story openings, writing prompts, and character introductions.

## What It Does

The AI Story Starter offers three tools for writers:

1. **Opening** - Generate gripping first paragraphs for stories in any genre
2. **Writing Prompt** - Get writing prompts or exercises to inspire you
3. **Character Intro** - Create compelling character introduction paragraphs

All outputs include:
- Genre and mood guidance
- Hook analysis
- Continue prompts/questions
- Key elements to develop

Perfect for:
- Overcoming writer's block
- NaNoWriMo preparation
- Writing practice exercises
- Character development exploration
- sparks of inspiration

## How to Use

### Opening Mode
1. Choose genre (fantasy, sci-fi, mystery, romance, etc.)
2. Pick mood (mysterious, tense, whimsical, hopeful, etc.)
3. Select protagonist type
4. Choose hook style (action, mystery, dialogue, question, statement)
5. Get a complete story opening (80-150 words)
6. See conflict seeds and continue prompts to guide your writing

### Writing Prompt Mode
- Option A: Enter a theme and/or genre mashup (e.g., "betrayal" + "sci-fi western")
- Option B: Enter your own writing prompt
- Get refined prompt + 3 story starter openings based on it
- Includes key elements and constraints

### Character Intro Mode
1. Enter character type (detective, witch, astronaut, etc.)
2. Choose archetype (hero, mentor, villain, etc.)
3. Describe their current situation
4. Get a "show don't tell" character intro paragraph
5. See casting suggestion and hook questions

## API Endpoints

### POST `/api/2026-02-15-ai-story-starter`

#### Action: `opening`

Generates a story opening.

**Request body:**
```json
{
  "action": "opening",
  "genre": "fantasy",
  "mood": "mysterious",
  "protagonist_type": "reluctant",
  "hook_type": "mystery"
}
```

**Response:**
```json
{
  "opening": {
    "opening": "The old bookshop hadn't been there yesterday. Aris stood before the dusty window, his reflection ghostly in the antique glass. Something inside called to him, a whisper of forgotten magic that made his inherited copper key grow warm in his pocket. He should have kept walking. But curiosity, their family's curse, had him pushing the door open.",
    "genre": "fantasy",
    "hook_used": "mystery",
    "protagonist_hint": "Reluctant hero named Aris with family legacy/cursed curiosity",
    "setting_established": "Modern city street with suddenly appearing magical shop",
    "conflict_seeds": ["Mystery of the suddenly appearing shop", "Family curse/expectation", "Magical calling vs ordinary life"],
    "continue_prompt": "What's so important about Aris's copper key? What's inside the shop that called to him? Why does it appear only when he's near?"
  },
  "genre": "fantasy",
  "mood": "mysterious"
}
```

#### Action: `prompt_writing`

Generates writing prompts or builds from input.

**Request body (custom prompt):**
```json
{
  "action": "prompt_writing",
  "writing_prompt": "A world where memories are currency"
}
```

**Response:**
```json
{
  "prompt_data": {
    "refined_prompt": "In a world where memories are currency, a poor person discovers they have a rare 'vintage' memory worth a fortune—but it's someone else's stolen past.",
    "story_starters": [
      "The memory broker offered me fifty thousand for the taste of strawberries. I'd give anything to forget that I remembered it at all.",
      "Every morning, I sold the previous day's memories to pay rent. I never looked at what I was selling until the day I found my own childhood in a stranger's collection.",
      "They said my childhood was worth a small fortune. They should have specified it wasn't mine to sell."
    ],
    "genre_blend": "sci-fi dystopia",
    "key_elements": ["Memory as money", "Identity vs ownership", "Class divide (memory rich vs poor)"],
    "word_limit": "1000-3000 words",
    "exercise_type": "worldbuilding"
  },
  "theme": "",
  "genre_mashup": "",
  "original_prompt": "A world where memories are currency"
}
```

#### Action: `character_intro`

Generates character introduction.

**Request body:**
```json
{
  "action": "character_intro",
  "character_type": "detective",
  "archetype": "antihero",
  "situation": "investigating a case they're not supposed to be on"
}
```

**Response:**
```json
{
  "character_intro": {
    "introduction": "Detective Mara Vance lit her fifth cigarette of the morning, although it was only nine. Her lieutenant had told her to stay out of theportcase, but the victim's daughter had called her from the hallway, whispered 'they're saying it was suicide, but she was scared.' Mara pocketed her badge photo, slipped past uniformed officers, and entered the crime scene not as an officer, but as a ghost investigating another ghost.",
    "character_name": "Mara Vance",
    "traits_revealed": ["Rebellious/rule-breaker", "Smoker (stress)", "Empathetic (took a personal call)", "Experienced (knows how to bypass protocols)", "Haunted by past cases"],
    "situation_context": "Illegally entering a murder crime scene, investigating despite orders",
    "narrator_pov": "third limited",
    "hook_question": "Why is Mara defying orders? What personal connection does she have to this case? What's on her badge photo that she needs to hide?",
    "casting_suggestion": "Similar vibe to Ellen Ripley from Alien: tough, weary, underneath it all cares deeply"
  },
  "character_type": "detective",
  "archetype": "antihero"
}
```

## Writing Tips from the AI

**Strong openings typically:**
- Create immediate intrigue or mystery
- Establish voice/tone quickly
- Introduce protagonist with hint of conflict
- Set scene with vivid sensory details
- Pose implicit questions in reader's mind

**Three common opening strategies:**
- **Action**: Drop character in middle of action
- **Mystery**: Present a puzzle or anomaly
- **Character**: Reveal compelling voice/attitude immediately

**Character introductions succeed when:**
- Show personality through action/dialogue (not just description)
- Hint at backstory or motivation
- Establish a unique voice or perspective
- Create curiosity about their journey

## Technology

- **Backend**: Python with Pollinations.AI
- **Frontend**: Writer-friendly blue gradient, clean typography, organized results
- **Features**: Three distinct modes, meta-analysis, continue prompts, casting suggestions

## View the Live Project

Visit: https://ai-trendings.vercel.app

Happy writing! 📝
