"""AI Fundamentals Explorer - February 10, 2026

A comprehensive interactive guide to understanding Artificial Intelligence.
Learn about AI concepts, how AI models work, key terminology, and real-world applications.
"""

from ..base import call_openrouter, generate_image_url, extract_json
import json


def handle(action: str, data: dict) -> dict:
    """Handle project actions.

    Args:
        action: 'start', 'overview', 'types', 'how_it_works', 'concepts',
                'applications', 'ethics', 'quiz', 'visualize', 'glossary'
        data: Request data from frontend

    Returns:
        dict: Response to send to frontend
    """

    if action == 'start':
        """Initialize project with welcome message and learning path."""
        prompt = """Welcome to AI Fundamentals Explorer! Your journey to understanding AI starts here.

In this interactive learning experience, you'll discover:
- What AI really is (and isn't)
- Different types of AI systems
- How AI models learn and think
- Key concepts every AI user should know
- Real-world applications transforming industries
- Important ethical considerations
- Test your knowledge with interactive quizzes

Whether you're a developer, business user, or just curious about AI,
this guide will give you practical, actionable knowledge.

Let's begin with a clear, jargon-free introduction to AI!

Write an engaging, welcoming introduction (~200 words) that:
- Explains why understanding AI matters today
- Sets expectations for what learners will discover
- Encourages curiosity and exploration
- Uses approachable language for beginners"""

        introduction = call_openrouter(prompt)

        # Generate a welcome visual
        image_prompt = "Friendly robot and human collaborating on digital tablet, modern flat design, blue gradient background, geometric shapes floating, representing AI education and partnership. Clean, professional, approachable style."
        welcome_image = generate_image_url(image_prompt)

        # Learning modules overview
        modules = [
            {"id": "overview", "title": "What is AI?", "duration": "5 min", "icon": "🤖"},
            {"id": "types", "title": "Types of AI", "duration": "8 min", "icon": "📊"},
            {"id": "how_it_works", "title": "How AI Works", "duration": "10 min", "icon": "⚙️"},
            {"id": "concepts", "title": "Key Concepts", "duration": "12 min", "icon": "💡"},
            {"id": "applications", "title": "Real-World AI", "duration": "10 min", "icon": "🌍"},
            {"id": "ethics", "title": "Ethics & Safety", "duration": "10 min", "icon": "⚖️"},
            {"id": "quiz", "title": "Test Your Knowledge", "duration": "15 min", "icon": "🎯"},
            {"id": "glossary", "title": "AI Glossary", "duration": "reference", "icon": "📚"}
        ]

        return {
            "introduction": introduction,
            "welcome_image": welcome_image,
            "modules": modules,
            "total_duration": "~70 minutes of learning",
            "difficulty": "Beginner-friendly"
        }

    elif action == 'overview':
        """Explain what AI is in simple terms."""
        prompt = """Provide a clear, beginner-friendly explanation of Artificial Intelligence (AI).

Cover these points (~300 words):
1. Simple definition: AI as machines that can perceive, reason, learn, and act
2. Key distinction: Narrow AI (specialized) vs General AI (human-like, doesn't exist yet)
3. Common AI capabilities we see today: image recognition, language understanding, recommendation systems
4. What AI is NOT: sentient beings, magic, infallible
5. Brief history: from Turing test to today's AI boom
6. Why AI matters now: computational power, data availability, algorithmic advances
7. How AI impacts daily life (without being obvious)

Use analogies and everyday examples. Avoid jargon. Make it accessible to someone with no technical background."""

        overview = call_openrouter(prompt)

        # Generate visual for AI concept
        image_prompt = "Simple infographic showing AI ecosystem: inputs (data, images, text) -> AI brain/processing -> outputs (answers, predictions, images). Clean vector illustration with arrows and icons."
        image_url = generate_image_url(image_prompt)

        return {
            "overview": overview,
            "visualization": image_url,
            "key_takeaway": "AI is a tool that recognizes patterns and makes predictions based on data - it doesn't 'think' like humans do."
        }

    elif action == 'types':
        """Explain different types of AI systems."""
        prompt = """Explain the different categories and types of AI systems.

Structure the explanation (~350 words):

1. By Capability:
   - Narrow/Weak AI: What it is, examples (chess bots, recommendation systems, voice assistants)
   - General/Strong AI: Definition, current status (hypothetical, doesn't exist yet)
   - Superintelligence: Theoretical concept, debates about risks

2. By Approach (AI Techniques):
   - Machine Learning: Learning from data without explicit programming
   - Deep Learning: Neural networks with many layers
   - Natural Language Processing (NLP): Understanding and generating human language
   - Computer Vision: Understanding images and videos
   - Reinforcement Learning: Learning through trial and error
   - Generative AI: Creating new content (text, images, music)

3. Popular Model Types:
   - Large Language Models (LLMs): GPT, Claude, etc. - what they do
   - Diffusion Models: Image generators like DALL-E, Stable Diffusion
   - Multimodal Models: Models that handle multiple input/output types

Use concrete examples for each. Create a mental model that helps someone categorize any AI they encounter."""

        types_explanation = call_openrouter(prompt)

        # Generate comparison chart visualization
        image_prompt = "Hierarchical tree diagram showing AI classification: AI -> Narrow AI & General AI; Narrow AI branches into ML, NLP, CV, RL; ML branches into Deep Learning, LLMs, Diffusion Models. Clean organizational chart style."
        image_url = generate_image_url(image_prompt)

        return {
            "types": types_explanation,
            "visualization": image_url,
            "interactive_note": "Try to categorize these AI tools: ChatGPT, Tesla Autopilot, Netflix recommendations, Midjourney, Siri, Google Translate"
        }

    elif action == 'how_it_works':
        """Explain how AI models learn and operate."""
        prompt = """Explain how AI models, particularly machine learning models, work and learn.

Break it down into clear sections (~400 words):

1. The Basic Idea:
   - Traditional programming vs Machine Learning
   - Data + Algorithm = Model
   - Simple analogy: showing examples vs giving rules

2. Training Process:
   - What training data looks like (inputs and correct outputs)
   - The model starts with random guesses
   - Loss function: measuring error
   - Backpropagation: learning from mistakes
   - Optimization (gradient descent)
   - Epochs and iterations

3. Neural Networks (for deep learning):
   - Inspired by brain neurons (loosely)
   - Layers: input, hidden, output
   - Weights and biases
   - Activation functions (ReLU, sigmoid, softmax)
   - How deep = more complex patterns

4. What Happens During Inference:
   - Trained model vs training phase
   - Forward pass: data flows through network
   - Prediction/generation output
   - No learning happens during inference

5. Why Scale Matters:
   - More data → better learning
   - More parameters → more capability
   - More compute → more complex models
   - Emergent abilities at certain scales

Use analogies: teaching a child with examples, tuning an instrument, following a recipe.

Include a simple diagram description: training loop with forward pass, loss calculation, backpropagation."""

        how_it_works = call_openrouter(prompt)

        # Generate neural network visualization
        image_prompt = "Simplified neural network diagram: input layer nodes, hidden layer nodes with connections showing weights, output layer. Clean schematic with color gradients showing signal flow. Educational style."
        image_url = generate_image_url(image_prompt)

        return {
            "explanation": how_it_works,
            "visualization": image_url,
            "simple_summary": "AI training is essentially pattern matching: the model adjusts its internal settings until it correctly maps inputs to outputs based on many examples."
        }

    elif action == 'concepts':
        """Explain key AI terminology and concepts."""
        prompt = """Define and explain essential AI/LLM concepts that every AI user should understand.

Create clear, practical definitions (~350 words total) covering:

1. Token: What it is (roughly 4 chars or 3/4 word), why it matters (pricing, context limits), examples

2. Context Window: Maximum tokens a model can process at once, includes input + output, implications for long conversations/documents

3. Parameters: Model's "knowledge" stored as numbers, scale (billions to trillions), more params = more capability but more compute

4. Training Data: What the model learned from, data quality affects performance, cutoff dates and why models don't know recent events

5. Inference: Using a trained model (vs training), token streaming, latency considerations

6. Prompt: Input to AI model, prompt engineering, clarity matters

7. Temperature: Controls randomness/creativity, low vs high values, use cases

8. Top-p (nucleus) sampling: Another randomness control, works differently from temperature

9. Hallucination: Model making up facts, why it happens (pattern matching vs truth), how to mitigate

10. Fine-tuning: Adapting a base model for specific tasks, examples

11. Embeddings: Converting text to numbers, used for search/similarity

12. RAG (Retrieval-Augmented Generation): Adding external knowledge to LLMs

For each concept: simple definition → why it matters → practical impact on users.
Format as a numbered list with clear headings."""

        concepts_explanation = call_openrouter(prompt)

        # Generate concept map visualization
        image_prompt = "Network diagram connecting AI concepts: Tokens, Context Window, Parameters, Training, Inference, Temperature, Hallucination, RAG - all connected with lines showing relationships. Info graphic style."
        image_url = generate_image_url(image_prompt)

        return {
            "concepts": concepts_explanation,
            "visualization": image_url,
            "quick_reference": "Tokens count everything. Context limits how much you can send. Parameters determine capability. Temperature controls creativity."
        }

    elif action == 'applications':
        """Show real-world AI applications across industries."""
        prompt = """Survey of real-world AI applications across various industries.

Organize by domain (~400 words):

1. Healthcare:
   - Medical imaging analysis (cancer detection, X-rays)
   - Drug discovery and molecular design
   - Personalized treatment recommendations
   - Administrative automation

2. Business & Productivity:
   - Customer service chatbots
   - Document processing and data extraction
   - Meeting summarization and transcription
   - Email drafting and scheduling

3. Creative Industries:
   - Image generation for design and marketing
   - Video editing and effects
   - Music composition and audio production
   - Writing assistance and content creation

4. Science & Research:
   - Climate modeling and weather prediction
   - Protein folding (AlphaFold)
   - Scientific literature review and summarization
   - Simulation and hypothesis testing

5. Transportation:
   - Autonomous vehicles (Tesla, Waymo)
   - Traffic flow optimization
   - Route planning and logistics
   - Predictive maintenance

6. Education:
   - Personalized learning systems
   - Automated grading and feedback
   - Language learning tutors
   - Content creation for courses

7. Code & Software:
   - Code completion (GitHub Copilot)
   - Code review and bug detection
   - Documentation generation
   - Test case creation

For each, give 1-2 specific examples of tools/companies and describe the AI's role.
Emphasize that AI is augmenting human work, not replacing it entirely.
End with a forward-looking paragraph about emerging applications."""

        applications = call_openrouter(prompt)

        # Generate industry application visualization
        image_prompt = "Grid of 6 icons representing AI in different sectors: healthcare (medical cross), business (briefcase), creative (paintbrush), science (microscope), transportation (car), education (graduation cap). Modern flat design with colors."
        image_url = generate_image_url(image_prompt)

        return {
            "applications": applications,
            "visualization": image_url,
            "key_insight": "AI excels at pattern recognition, prediction, and automation - freeing humans for creative, strategic, and interpersonal work."
        }

    elif action == 'ethics':
        """Discuss AI ethics, safety, and responsible use."""
        prompt = """Comprehensive overview of AI ethics, safety concerns, and responsible development.

Cover (~400 words):

1. Major Ethical Concerns:
   - Bias and discrimination (training data reflects societal biases, real examples like gender/race bias in hiring, lending)
   - Privacy implications (data collection, surveillance, consent)
   - Transparency and explainability (black box problem, right to explanation)
   - Accountability (who is responsible when AI causes harm?)
   - Job displacement and economic impact
   - Environmental cost (energy consumption of large models)
   - Misinformation and deepfakes
   - Concentration of power (few companies control most AI)

2. AI Safety Research:
   - Alignment problem: making AI goals match human values
   - Control problem: ensuring humans can override AI
   - Reward hacking: AI finding loopholes in objectives
   - Emergent behaviors at scale

3. Current Mitigation Approaches:
   - Diverse training data and bias testing
   - Explainable AI (XAI) techniques
   - Human-in-the-loop systems
   - AI ethics boards and guidelines
   - Regulatory efforts (EU AI Act, etc.)
   - Red teaming and safety evaluations

4. Responsible AI Use for Individuals:
   - Verify AI outputs before relying on them
   - Understand limitations and avoid anthropomorphizing
   - Protect sensitive data when using AI tools
   - Be aware of potential biases in results
   - Use AI as assistant, not oracle

5. The Path Forward:
   - Need for diverse perspectives in AI development
   - Balancing innovation with safety
   - Global cooperation on AI governance
   - Public education and literacy

Write in a balanced way: acknowledge concerns without fearmongering, recognize progress while highlighting ongoing challenges."""

        ethics_content = call_openrouter(prompt)

        # Generate ethics/safety visualization
        image_prompt = "Balance scale with AI icon on one side and human icon on other, with shield and heart symbols representing protection and empathy. Clean, symbolic illustration in blue and green tones."
        image_url = generate_image_url(image_url)

        return {
            "ethics": ethics_content,
            "visualization": image_url,
            "action_items": [
                "Always fact-check important AI outputs",
                "Use AI as a tool, not an authority",
                "Be conscious of data privacy when sharing with AI",
                "Stay informed about AI capabilities and limitations"
            ]
        }

    elif action == 'quiz':
        """Generate or retrieve quiz questions to test knowledge."""
        quiz_type = data.get('quiz_type', 'comprehensive')  # comprehensive, basics, advanced
        num_questions = data.get('num_questions', 10)

        prompt = f"""Create {num_questions} multiple-choice quiz questions to test understanding of AI fundamentals.

Question style: Clear, practical, educational. Each question should:
- Test genuine understanding, not just memorization
- Have 4 options (A, B, C, D)
- Include the correct answer
- Provide a brief explanation of why the answer is correct

Topic focus: {quiz_type}
If comprehensive = mix of all topics
If basics = overview, types, basic concepts
If advanced = deeper technical concepts, ethics, applications

Format as JSON array of objects with:
- question: string
- options: array of 4 strings
- correct_index: 0-3
- explanation: string

Example:
[
  {{
    "question": "What does 'narrow AI' refer to?",
    "options": ["AI that only works on narrow tasks", "AI with limited capabilities", "AI specialized for a specific domain", "AI that is physically small"],
    "correct_index": 2,
    "explanation": "Narrow AI, also called weak AI, refers to AI systems designed for specific tasks like image recognition or language translation, as opposed to general human-like intelligence."
  }}
]

Make questions progressively challenging. Ensure options are plausible but clearly right/wrong."""

        quiz_text = call_openrouter(prompt)
        questions = extract_json(quiz_text) or []

        # If extraction failed, provide fallback questions
        if not questions:
            questions = [
                {
                    "question": "What is the primary method modern AI uses to learn?",
                    "options": [
                        "Following explicit programmed rules",
                        "Learning patterns from data",
                        "Copying human decision-making",
                        "Random trial and error only"
                    ],
                    "correct_index": 1,
                    "explanation": "Modern AI, especially machine learning, learns by identifying patterns in large datasets rather than following hand-coded rules."
                },
                {
                    "question": "What is a 'token' in the context of language models?",
                    "options": [
                        "A security token for API access",
                        "A unit of text (roughly 4 characters or 3/4 word)",
                        "A parameter in the model",
                        "A type of AI model architecture"
                    ],
                    "correct_index": 1,
                    "explanation": "Tokens are units of text that models process. A token is roughly 4 characters or 3/4 of a word on average. Tokens determine pricing and context limits."
                },
                {
                    "question": "What is 'hallucination' in AI?",
                    "options": [
                        "When the AI generates offensive content",
                        "When the AI makes up plausible but false information",
                        "When the AI refuses to answer certain questions",
                        "When the AI outputs images instead of text"
                    ],
                    "correct_index": 1,
                    "explanation": "Hallucination occurs when AI models generate convincing but incorrect or fabricated information, because they're predicting likely text, not retrieving facts."
                },
                {
                    "question": "What does RAG stand for in AI systems?",
                    "options": [
                        "Random Access Generation",
                        "Retrieval-Augmented Generation",
                        "Recursive Algorithmic Graph",
                        "Rationalized Answer Generator"
                    ],
                    "correct_index": 1,
                    "explanation": "RAG (Retrieval-Augmented Generation) combines retrieval from external knowledge sources with generative models to produce accurate, up-to-date responses."
                },
                {
                    "question": "Which of these is an example of narrow AI?",
                    "options": [
                        "A hypothetical AI that can do any intellectual task a human can",
                        "An AI that can diagnose specific diseases from medical images",
                        "An AI with consciousness and self-awareness",
                        "An AI that can learn any task without retraining"
                    ],
                    "correct_index": 1,
                    "explanation": "Disease diagnosis systems are narrow AI - they perform a specific task well, but cannot do unrelated tasks like hold a conversation or drive a car."
                }
            ]

        score = 0
        user_answers = data.get('answers', [])

        if user_answers and len(user_answers) == len(questions):
            for i, answer in enumerate(user_answers):
                if answer == questions[i]['correct_index']:
                    score += 1
            percentage = (score / len(questions)) * 100

            # Generate performance feedback
            if percentage >= 90:
                feedback = "Outstanding! You have mastered AI fundamentals."
            elif percentage >= 70:
                feedback = "Great job! You understand AI concepts well. Review the areas you missed to solidify your knowledge."
            elif percentage >= 50:
                feedback = "Good start! You have a basic understanding. Revisit the learning modules to strengthen your knowledge."
            else:
                feedback = "Keep learning! We recommend going through the AI Fundamentals modules again to build a solid foundation."

            return {
                "score": score,
                "total": len(questions),
                "percentage": round(percentage, 1),
                "feedback": feedback,
                "questions": questions,
                "answers_review": [
                    {
                        "question": q['question'],
                        "your_answer": user_answers[i],
                        "correct_answer": q['correct_index'],
                        "explanation": q['explanation'],
                        "correct": user_answers[i] == q['correct_index']
                    }
                    for i, q in enumerate(questions)
                ]
            }

        # New quiz - return questions without scoring
        return {
            "questions": questions,
            "num_questions": len(questions),
            "instructions": "Answer all questions to receive your score and feedback."
        }

    elif action == 'glossary':
        """Provide AI terminology glossary."""
        prompt = """Create a comprehensive AI glossary with clear, concise definitions.

Provide a JSON dictionary where:
- Keys are term names (lowercase, underscores for spaces)
- Values are objects with:
  - term: display name (with capitalization)
  - definition: clear, beginner-friendly explanation (1-2 sentences)
  - category: one of "General", "Technical", "LLM-specific", "Ethics"
  - example: practical example or use case (optional but preferred)

Include at least 40 terms covering:
- Basic AI/ML terms
- Neural network terms
- LLM-specific concepts
- Ethics and safety terms
- Common abbreviations

Essential terms to include: AI, ML, DL, NLP, LLM, Transformer, Parameters, Tokens, Embeddings, Prompt, Temperature, Top-p, Hallucination, Fine-tuning, RAG, Inference, Training, Backpropagation, Gradient Descent, Neural Network, Layer, Activation Function, Overfitting, Underfitting, Bias, Fairness, Explainability, Alignment, AGI, Narrow AI, Computer Vision, Reinforcement Learning, Generative AI, Diffusion Model, Context Window, System Prompt, Few-shot Learning, Zero-shot Learning, Chain of Thought, Token Limit, API, Model, Weights, Biases, Loss Function, Optimizer, Epoch, Batch, Dataset, Features, Labels, Classification, Regression, Clustering, Unsupervised Learning, Supervised Learning

Make definitions accessible to beginners."""

        glossary_text = call_openrouter(prompt)
        glossary = extract_json(glossary_text) or {}

        if not glossary:
            # Fallback minimal glossary
            glossary = {
                "ai": {
                    "term": "AI",
                    "definition": "Artificial Intelligence - computer systems that perform tasks typically requiring human intelligence, such as perception, reasoning, learning, and decision-making.",
                    "category": "General"
                },
                "ml": {
                    "term": "ML",
                    "definition": "Machine Learning - a subset of AI where systems learn patterns from data without explicit programming.",
                    "category": "General"
                },
                "llm": {
                    "term": "LLM",
                    "definition": "Large Language Model - AI models trained on vast text corpora to understand and generate human-like text.",
                    "category": "LLM-specific"
                },
                "token": {
                    "term": "Token",
                    "definition": "The basic unit of text processed by language models; roughly 4 characters or 3/4 of a word.",
                    "category": "LLM-specific"
                },
                "hallucination": {
                    "term": "Hallucination",
                    "definition": "When AI generates plausible but false or fabricated information, often presented confidently.",
                    "category": "LLM-specific"
                }
            }

        return {"glossary": glossary, "total_terms": len(glossary)}

    elif action == 'visualize':
        """Generate visual explanations of AI concepts."""
        concept = data.get('concept', 'neural network')

        # Map concept to visualization prompt
        concept_prompts = {
            'neural network': "Neural network diagram showing input layer, multiple hidden layers with colored nodes, output layer. Clean schematic with flow lines showing signal direction. Educational infographic style.",
            'training process': "Three-panel diagram: 1) random weights, 2) make prediction, 3) measure error and adjust weights. Show cycle repeating. Clean vector illustration.",
            'attention mechanism': "Transformer attention visualization: query, key, value with connection lines showing weighted importance. Heat map style showing which words attend to others.",
            'generative process': "Step-by-step: noise -> gradual image formation -> final image. Like diffusion process visualization.",
            'tokenization': "Text being split into tokens: 'Artificial Intelligence' -> 'Artificial', 'Intelligence' or ['Art', 'ific', 'ial', ' Intel', 'ligence']. Show token boundaries.",
            'bias': "Illustration of AI bias: same resume with different names (John vs Jamal) getting different outcomes. Chart showing disparate results.",
            'context window': "Visual metaphor: window sliding over long text, showing what fits inside. Token count indicator.",
            'embeddings': "Words positioned in 2D space based on meaning similarity. King - Man + Woman = Queen vector math shown.",
            'rag': "Diagram: User question -> retrieve documents from database -> combine with question -> generate answer. Show knowledge base separate from model.",
            'fine-tuning': "Base model -> add specialized dataset -> adapted model. Show before/after capabilities."
        }

        prompt = concept_prompts.get(concept, f"Clear educational diagram explaining {concept}. Technical illustration style with labels. Blue and green color scheme.")

        image_url = generate_image_url(prompt, width=800, height=600)

        explanation_prompt = f"Explain the concept of '{concept}' in AI in 2-3 sentences, focusing on why it's important and how it's used in practice."

        explanation = call_openrouter(explanation_prompt)

        return {
            "concept": concept,
            "visualization": image_url,
            "explanation": explanation,
            "related_concepts": [c for c in concept_prompts.keys() if c != concept][:3]
        }

    else:
        return {"error": f"Unknown action: {action}. Available actions: start, overview, types, how_it_works, concepts, applications, ethics, quiz, glossary, visualize"}


# Metadata for projects.json
META = {
    "name": "AI Fundamentals Explorer",
    "description": "An interactive guide to understanding Artificial Intelligence. Learn about AI concepts, types, how models work, key terminology, real-world applications, ethics, and test your knowledge with quizzes.",
    "category": "Education",
    "tags": ["ai", "education", "fundamentals", "learning", "beginner", "literacy"],
    "difficulty": "Beginner",
    "date": "2026-02-10"
}