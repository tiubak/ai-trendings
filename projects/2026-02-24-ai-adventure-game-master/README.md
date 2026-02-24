# AI Adventure Game Master

An interactive AI-powered storytelling experience where you embark on a personalized adventure! Choose your genre, create your character, and make decisions that shape your journey through dynamically generated worlds.

## 🎮 How It Works

1. **Choose Your Genre:** Fantasy, Sci-Fi, Mystery, Horror, Adventure, Steampunk, or Cyberpunk
2. **Create Your Character:** Be as creative as you like (default: adventurer)
3. **Begin Your Journey:** AI generates an opening scene with three choices
4. **Make Your Choice:** Every decision shapes the story's direction
5. **Continue Exploring:** The story adapts to your choices, creating a unique adventure
6. **Visualize the Scene:** Generate an image of the current scene to bring the story to life

## ✨ Features

- **Dynamic Storytelling:** AI generates unique narrative content based on your choices
- **Multiple Genres:** Explore different worlds and storytelling styles
- **Character Customization:** Play as any character you imagine
- **Interactive Choices:** Your decisions matter and shape the story
- **Scene Visualization:** Generate images to visualize key moments
- **Endless Adventures:** Every playthrough creates a new story

## 🛠️ Technical Details

- **API:** Single Vercel serverless function with dynamic routing
- **AI Text Generation:** OpenRouter with free model (openrouter/free)
- **Image Generation:** Pollinations.AI with Flux model
- **No Database:** Story state managed entirely in frontend session
- **Responsive Design:** Works on desktop and mobile

## 🎯 Example Adventures

### Fantasy
- "You are a brave knight in a medieval kingdom..."
- Choices might include: "Enter the dark forest", "Visit the wizard", "Search the ancient ruins"

### Sci-Fi
- "Your starship has crashed on an unknown planet..."
- Choices: "Repair the communicator", "Explore the alien structure", "Search for supplies"

### Mystery
- "You've received an anonymous letter pointing to a hidden truth..."
- Choices: "Investigate the address", "Research the sender", "Contact an old friend"

## 🚀 Potential Expansions

- Story persistence (save/load adventures)
- More complex branching narratives
- Character stats and inventory system
- Multiplayer cooperative or competitive modes
- Voice narration with TTS
- Export stories as PDFs or images
- Share adventure stories with friends

## 📂 Project Structure

```
api/
├── index.py           # Single serverless function router
└── pyproject.toml     # Dependencies

lib/
├── base.py            # Common API functions
└── projects/
    ├── __init__.py    # Project registry
    └── day_2026_02_24.py  # Adventure handler

projects/
└── 2026-02-24-ai-adventure-game-master/
    ├── index.html     # Frontend
    └── README.md      # This file
```

## 🤖 AI Prompt Strategy

The project uses carefully crafted prompts to ensure:

- **Consistent tone** matching the selected genre
- **Clear scene descriptions** with sensory details
- **Three distinct choices** that meaningfully branch the story
- **Continuity** from previous scenes and user choices
- **Appropriate pacing** with neither too much nor too little detail

## 📝 Learning Outcomes

This project demonstrates:

- Dynamic content generation with LLMs
- State management in a serverless environment
- Interactive storytelling patterns
- Image generation integration
- Clean frontend-backend API design
- CORS and error handling
- Responsive web design

---

**Created:** February 24, 2026  
**Category:** Fun - Interactive AI Applications  
**Part of:** [AI Trendings](https://ai-trendings.vercel.app) daily showcase
