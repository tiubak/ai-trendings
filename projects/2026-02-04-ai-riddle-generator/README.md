# AI Riddle Generator

**Date:** 2026-02-04

Challenge your mind with AI-generated riddles! Create, solve, and customize brain-teasing puzzles across various categories and difficulties.

## What It Does

The AI Riddle Generator provides three modes:

1. **Random Riddle** - Generate a riddle by selecting difficulty (easy, medium, hard) and category (nature, animals, objects, food, places, abstract concepts)
2. **Custom Topic** - Create a riddle about any topic you choose
3. **Solve** - Enter your answer and get instant feedback with hints

Features:
- Progressive hints for stuck solvers
- Answer checking with semantic understanding
- Difficulty and category organization
- Preview of answer before revealing

## How to Use

### Random Riddle Mode
1. Select difficulty level
2. Choose a category
3. Click "Generate Riddle"
4. Read the riddle carefully
5. Type your answer and click "Check Answer"
6. Use hints if you're stuck

### Custom Topic Mode
1. Switch to "Custom Topic" mode
2. Enter any topic (e.g., "coffee", "quantum physics", "friendship")
3. Generate the riddle
4. Challenge yourself or friends to solve it

## API Endpoints

### POST `/api/2026-02-04-ai-riddle-generator`

#### Action: `generate`

Generates a random riddle.

**Request body:**
```json
{
  "action": "generate",
  "difficulty": "medium",
  "category": "animals"
}
```

**Response:**
```json
{
  "riddle": {
    "riddle": "What has roots as nobody sees,\nIs taller than trees,\nUp, up it goes,\nAnd yet never grows?",
    "answer": "mountain",
    "hints": ["It's a natural landform", "It is immovable and ancient"],
    "difficulty": "medium",
    "category": "nature"
  },
  "difficulty": "medium",
  "category": "nature"
}
```

#### Action: `solve`

Checks if the user's answer is correct.

**Request body:**
```json
{
  "action": "solve",
  "user_answer": "mountain",
  "riddle": "I have roots as nobody sees...",
  "correct_answer": "mountain"
}
```

**Response:**
```json
{
  "evaluation": {
    "is_correct": true,
    "feedback": "The answer is correct!",
    "if_wrong": "",
    "alternative_phrasings": ["peak", "summit", "hill"]
  },
  "user_answer": "mountain"
}
```

#### Action: `create_custom`

Generates a riddle on a custom topic with specified creativity level.

**Request body:**
```json
{
  "action": "create_custom",
  "topic": "the internet",
  "creativity_level": "high"
}
```

**Response:**
```json
{
  "riddle": {
    "riddle": "I connect all the world without moving,\nI carry voices, pictures, and lore,\nYou cannot see me, yet I'm always there,\nWhat am I?",
    "answer": "the internet",
    "difficulty_estimate": "medium",
    "topic_subcategory": "technology",
    "hint": "Think about global connectivity and information"
  },
  "topic": "the internet",
  "creativity": "high"
}
```

## Riddle Best Practices

Our AI generates riddles that follow classic principles:
- **Descriptive imagery**: Uses vivid language to describe the answer
- **Metaphorical thinking**: Often uses metaphor rather than literal description
- **Logical consistency**: The clues should point clearly to one answer
- **Appropriate difficulty**: Easier riddles use common objects; harder ones use more abstract concepts

## Tips for Solving Riddles

1. **Look for keywords** - Identify the main nouns and verbs
2. **Think metaphorically** - Riddles rarely describe things literally
3. **Consider all possibilities** - Don't jump to the first answer that comes to mind
4. **Use hints strategically** - Each hint reveals more context
5. **Break it down** - Analyze each line separately, then together

## Technology

- **Backend**: Python with Pollinations.AI for creative riddle generation
- **Frontend**: Purple/gold theme evoking treasure and mystery
- **Features**: Three-generation modes, hint system, answer validation

## View the Live Project

Visit: https://ai-trendings.vercel.app
