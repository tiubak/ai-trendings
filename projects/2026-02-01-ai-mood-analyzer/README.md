# AI Mood Analyzer

**Date:** 2026-02-01

A compassionate AI tool that helps you understand your emotions and provides personalized support to improve your mood.

## What It Does

The AI Mood Analyzer takes your current emotional state and returns:

- **Mood Label**: A concise description of your emotional state
- **Intensity Rating**: How strong the feeling is (1-10 scale)
- **Possible Causes**: Three contextual factors that might be contributing
- **Coping Suggestions**: Three practical strategies to manage the mood
- **Uplifting Message**: A supportive, empathetic message tailored to your situation
- **Related Quote**: An inspirational quote relevant to your emotional state

After receiving your analysis, you can optionally request a **Personalized Mood Boost Plan** with:

- A 3-step actionable plan (immediate, short-term, and long-term)
- A quick win you can do in under 5 minutes
- Words of encouragement

## How to Use

1. Enter how you're feeling in the text area (e.g., "anxious about my presentation")
2. Optionally, add context about what's happening
3. Click "Analyze My Mood"
4. Review your personalized analysis
5. Optionally, click "Get Personalized Mood Boost Plan" for actionable steps

## API Endpoints

### POST `/api/2026-02-01-ai-mood-analyzer`

The API accepts an `action` parameter:

#### Action: `analyze`

Analyzes the provided mood information.

**Request body:**
```json
{
  "action": "analyze",
  "feeling": "anxious about work deadline",
  "context": "I have a big project due tomorrow"
}
```

**Response:**
```json
{
  "analysis": {
    "mood_label": "Anxious",
    "intensity": 7,
    "possible_causes": ["Upcoming deadline", "Perfectionist tendencies", "Lack of sleep"],
    "coping_suggestions": ["Practice 5-4-3-2-1 grounding technique", "Break task into smaller steps", "Take a 10-minute walk"],
    "uplifting_message": "Your anxiety shows you care deeply about your work...",
    "related_quote": "This too shall pass."
  },
  "feeling": "anxious about work deadline",
  "context": "I have a big project due tomorrow"
}
```

#### Action: `boost`

Generates a personalized mood boost plan based on a previous analysis.

**Request body:**
```json
{
  "action": "boost",
  "analysis": { /* the analysis object from analyze response */ },
  "preferred_activity": "reading"  // optional
}
```

**Response:**
```json
{
  "boost_plan": {
    "mood_goal": "Calm and focused",
    "step_1_immediate": {
      "action": "Do 10 deep breaths",
      "reason": "Activates parasympathetic nervous system"
    },
    "step_2_short_term": {
      "action": "Work in 25-minute Pomodoro intervals",
      "reason": "Builds momentum and reduces overwhelm"
    },
    "step_3_long_term": {
      "action": "Practice daily mindfulness meditation",
      "reason": "Builds resilience to stress"
    },
    "quick_win": "Listen to your favorite uplifting song",
    "encouragement": "You've overcome challenges before and you'll overcome this one too..."
  },
  "original_analysis": { /* original analysis object */ }
}
```

## Technology

- **Backend**: Python with Pollinations.AI API
- **Frontend**: Vanilla HTML/CSS/JavaScript with glassmorphism design
- **AI Model**: Text generation via Pollinations.AI
- **Architecture**: Vercel serverless functions

## Disclaimer

This tool is for informational and supportive purposes only. It is not a substitute for professional mental health care. If you are experiencing severe emotional distress, please consult a licensed mental health professional or contact a crisis helpline.

## View the Live Project

Visit: https://ai-trendings.vercel.app
