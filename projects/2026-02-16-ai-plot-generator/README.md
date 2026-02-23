# AI Plot Generator

**Date:** 2026-02-16

Generate complete plot outlines, add twists, and build three-act structures for your stories.

## What It Does

The AI Plot Generator offers three tools:

1. **Full Plot** - Generate a complete plot outline with acts, twists, climax, and resolution
2. **Add Twist** - Take an existing plot outline and add a meaningful twist
3. **Three-Act Structure** - Build classic three-act structure from a topic/genre

All plots include:
- Logline (elevator pitch)
- Act-by-act breakdowns
- Key plot twists
- Climax and resolution
- Genre conventions

Perfect for:
- Writers planning novels/screenplays
- Game designers creating story arcs
- Overcoming writer's block on plot problems
- Learning story structure fundamentals
- Exploring "what if" scenarios

## How to Use

### Full Plot Mode
1. Choose genre: fantasy, sci-fi, mystery, thriller, romance, horror, etc.
2. Choose story length: short, novella, or novel
3. Optionally specify protagonist type
4. Get complete plot with:
   - Title and logline
   - 3-5 acts with summaries
   - 2-3 major twists
   - Climax description
   - Resolution
   - Genre conventions used

### Add Twist Mode
1. Paste an existing plot outline (as JSON from Full Plot or your own)
2. Choose twist type: Unexpected, Shocking, Bittersweet, Redemption, Revenge
3. Get enhanced plot with twist integrated
4. See affected acts and reasoning

### Three-Act Structure Mode
1. Enter a story topic (betrayal, redemption, survival, etc.)
2. Choose genre
3. Get classic three-act breakdown:
   - Act I: Setup (ordinary world, inciting incident, key character)
   - Act II: Confrontation (rising action, midpoint, darkest moment)
   - Act III: Resolution (climax, denouement, theme fulfilled)
   - Central conflict and thematic statement

## API Endpoints

### POST `/api/2026-02-16-ai-plot-generator`

#### Action: `generate`

Generates full plot outline.

**Request body:**
```json
{
  "action": "generate",
  "genre": "fantasy",
  "length": "novel",
  "protagonist_type": "reluctant hero"
}
```

**Response:**
```json
{
  "plot": {
    "title": "The Last Spellweaver",
    "hook": "A reluctant magic-user must master forbidden spells to stop a world-ending catastrophe.",
    "structure": [
      {
        "act_number": 1,
        "title": "The Discovery",
        "summary": "Protagonist discovers magical ability and is drawn into conflict"
      },
      {
        "act_number": 2,
        "title": "The Training",
        "summary": "Learns to use powers while facing escalating threats"
      },
      {
        "act_number": 3,
        "title": "The Confrontation",
        "summary": "Final battle using all skills learned"
      }
    ],
    "key_twists": [
      "The mentor is secretly the villain",
      "The protagonist created the threat accidentally"
    ],
    "climax": "Hero uses forbidden magic to defeat villain but at great personal cost",
    "resolution": "Magic is restored but hero cannot use it anymore",
    "genre_conventions": ["Chosen one", "Magic school/training", "Final sacrifice"]
  },
  "genre": "fantasy",
  "length": "novel",
  "protagonist": "reluctant hero"
}
```

#### Action: `twist`

Adds twist to existing plot.

**Request body:**
```json
{
  "action": "twist",
  "plot_outline": { /* full plot object from generate */ },
  "twist_type": "shocking"
}
```

**Response:**
```json
{
  "twist": {
    "original_title": "The Last Spellweaver",
    "twist_added": "The villain is the protagonist's future self from another timeline",
    "affected_acts": [2, 3],
    "new_structure": [ /* modified act structure */ ],
    "twist_reasoning": "Creates deep personal stakes and explores nature vs nurture",
    "reader_reaction": "Mind-blowing revelation that recontextualizes everything"
  },
  "original": { /* original plot */ },
  "twist_type": "shocking"
}
```

#### Action: `structure`

Generates three-act structure.

**Request body:**
```json
{
  "action": "structure",
  "topic": "betrayal",
  "genre": "thriller"
}
```

**Response:**
```json
{
  "structure": {
    "logline": "A trusted friend's betrayal leads to catastrophic consequences in a high-stakes thriller.",
    "act_i_setup": {
      "ordinary_world": "Two friends run successful business together",
      "inciting_incident": "One discovers the other is embezzling",
      "key_character": "Protagonist: loyal but naïve entrepreneur"
    },
    "act_ii_confrontation": {
      "rising_action": "Confrontation leads to escalating threats and reveals",
      "midpoint": "Protagonist learns friend was blackmailed by crime syndicate",
      "darkest_moment": "Business destroyed, protagonist framed for crimes"
    },
    "act_iii_resolution": {
      "climax": "Face-off at docks where money laundering happens",
      "denouement": "Friend goes to prison, protagonist rebuilds with hard-won wisdom",
      "theme_fulfilled": "Betrayal from within cuts deepest but truth and integrity endure"
    },
    "central_conflict": "Friendship vs. integrity, loyalty vs. self-preservation",
    "thematic_statement": "Betrayal reveals true character in both betrayer and betrayed."
  },
  "topic": "betrayal",
  "genre": "thriller"
}
```

## Plot Structure Basics

**Classic Three-Act Structure:**
- **Act I (Setup)**: Establish normal world, introduce protagonist, inciting incident disrupts
- **Act II (Confrontation)**: Rising action, obstacles, midpoint reversal, darkest moment
- **Act III (Resolution)**: Climax, denouement, new equilibrium

**Key Elements:**
- **Logline**: One-sentence pitch that captures core conflict
- **Inciting Incident**: Event that launches the story
- **Midpoint**: Major turning point that raises stakes
- **Climax**: Highest tension confrontation
- **Resolution**: Loose ends tied up, new normal

## Use Cases

- **NaNoWriMo planning** - Outline before writing
- **Screenplay structure** - Hollywood three-act
- **Game narrative design** - Branching plot points
- **Short story planning** - Condensed structures
- **Plot hole diagnosis** - Identify missing middle
- **Genre exploration** - See conventions in action

## Technology

- **Backend**: Python with Pollinations.AI
- **Frontend**: Dark ocean theme, structured result displays, twist integration
- **Features**: Three modes, plot modification, act-by-act visualization

## View the Live Project

Visit: https://ai-trendings.vercel.app

Build compelling stories, one plot point at a time! 📖
