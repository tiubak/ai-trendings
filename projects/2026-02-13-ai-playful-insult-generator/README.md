# AI Playful Insult Generator

**Date:** 2026-02-13

Generate playful, friendly insults for bantering with friends and lighthearted roasting.

## What It Does

The AI Playful Insult Generator creates humorously insulting content in three modes:

1. **Insult** - Choose target (personality, appearance, skills, habits, intelligence) and intensity
2. **Tease a Friend** - Specify a friend's quirk for personalized teasing
3. **Roast Me** - Self-deprecating humor (you insult yourself)

All insults include:
- Safety assessment (appropriate for relationship)
- Suggested emojis to soften delivery
- Humor style classification
- Follow-up positive reinforcement (where applicable)
- Comeback opportunities

## ⚠️ Important: Use Responsibly

**Playful insults are ONLY appropriate when:**
- You know the person well enough that they'll understand the humor
- You have a foundation of mutual respect and affection
- You match the tone to your relationship
- You include obvious humor signals (emojis, exaggerated delivery, positive follow-up)
- You can read the room and know when to stop

**Never use with:**
- Strangers or acquaintances
- People who are sensitive about the topic
- Power-imbalanced relationships (boss/employee, teacher/student)
- In professional settings
- Online where tone is lost

When in doubt, don't. Kindness is always in style.

## How to Use

### Insult Mode
1. Choose what to target (personality, appearance, etc.)
2. Select intensity: Light, Moderate, or Bold
3. Pick relationship context (friends, besties, siblings, coworkers)
4. Get a playful insult with safety check and delivery tips

### Tease a Friend Mode
1. Enter your friend's specific quirk or habit
2. Generate a personalized tease
3. See suggested comeback and positive follow-up

### Roast Me Mode
1. Enter a trait you want to humorously critique about yourself
2. Choose style (Light, Moderate, Brutal)
3. Get a self-deprecating joke
4. Perfect for breaking the ice or showing you don't take yourself too seriously

## API Endpoints

### POST `/api/2026-02-13-ai-playful-insult-generator`

#### Action: `generate`

Generates a playful insult.

**Request body:**
```json
{
  "action": "generate",
  "target_type": "personality",
  "intensity": "moderate",
  "relationship": "bff"
}
```

**Response:**
```json
{
  "insult": {
    "insult": "You have the organizational skills of a tornado in a glitter factory.",
    "intensity": "moderate",
    "target": "personality",
    "relationship": "bff",
    "humor_style": "exaggeration",
    "safe_for_relationship": true,
    "smiley_suggestion": "😜"
  },
  "target_type": "personality",
  "intensity": "moderate"
}
```

#### Action: `between_friends`

Generates a friendly tease about a specific quirk.

**Request body:**
```json
{
  "action": "between_friends",
  "friend_quirk": "always 10 minutes late"
}
```

**Response:**
```json
{
  "tease": {
    "tease": "Your sense of time is so unique, it's like you live in a different timezone.",
    "quirk_targeted": "punctuality",
    "comeback_opportunity": "Says I'm just fashionably late to everything",
    "affection_level": 9,
    "relationship_strength": "besties",
    "follow_up_positive": "But seriously, I love that you're always true to yourself."
  },
  "quirk": "always 10 minutes late"
}
```

#### Action: `roast_me`

Generates self-deprecating humor.

**Request body:**
```json
{
  "action": "roast_me",
  "personality_trait": "procrastination",
  "style": "light"
}
```

**Response:**
```json
{
  "roast": {
    "roast": "I procrastinate so well, I could probably get a PhD in 'I'll do it tomorrow'.",
    "style": "light",
    "trait_targeted": "procrastination",
    "confidence_required": 6,
    "audience_reaction": "Everyone laughs because they relate",
    "self_love_balance": "Saying it with a smile shows you're secure about it"
  },
  "style": "light",
  "trait": "procrastination"
}
```

## The "Playful" Distinction

**Playful insults** differ from mean-spirited ones in:
- **Intent**: Making people laugh together, not making them feel bad
- **Target**: Often universal quirks or traits the person knows they have
- **Delivery**: Exaggerated, surrounded by positive signals (emojis, smiles)
- **Relationship**: Only used where trust exists
- **Follow-up**: Usually followed by affection or compliment ("...but you're still awesome")

**Signals a joke is not serious:**
- Obviously impossible exaggeration ("You're dumber than a box of hammers" - said to someone smart)
- Self-targeting ("I'm so lazy I'd buy a remote控制的bed if I could")
- Including emojis that contradict words (😄👻)
- Follow-up "just kidding" or "but seriously, you're great"
- Said with a big smile to close friends

## Technology

- **Backend**: Python with Pollinations.AI
- **Frontend**: Bold, carnival-style design with rotating cards
- **Features**: Multiple modes, safety indicators, comeback suggestions

## View the Live Project

Visit: https://ai-trendings.vercel.app
