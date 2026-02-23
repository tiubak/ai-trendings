"""AI Fundamentals & Insights - February 23, 2026

A comprehensive guide to understanding artificial intelligence: core concepts,
historical context, current state, practical applications, and future directions.
Perfect for beginners, students, and professionals looking to understand AI deeply.
"""

from ..base import call_openrouter, generate_image_url, extract_json


def handle(action: str, data: dict) -> dict:
    """Handle project actions.

    Args:
        action: 'start', 'overview', 'concepts', 'history', 'current_state',
                'applications', 'ethics', 'glossary', 'deep_dive'
        data: Request data from frontend

    Returns:
        dict: Response to send to frontend
    """

    if action == 'start':
        """Initialize with introduction to AI."""
        prompt = """Welcome to AI Fundamentals! Provide an engaging introduction to artificial intelligence.

        Cover:
        - What AI is (simple definition)
        - Why AI matters today
        - Brief history in 3 acts: early days, machine learning revolution, deep learning era
        - Current impact on daily life
        - Why understanding AI is essential for everyone

        Make it welcoming and accessible. ~300-400 words."""

        intro = call_openrouter(prompt)

        return {
            "introduction": intro,
            "date": "February 23, 2026",
            "quick_facts": [
                "AI is transforming every industry",
                "Not magic—just math and data",
                "Humans and AI are better together",
                "Ethics and safety are crucial",
                "AI literacy is becoming as important as digital literacy"
            ],
            "available_sections": [
                "overview", "concepts", "history", "current_state",
                "applications", "ethics", "glossary", "deep_dive"
            ]
        }

    elif action == 'overview':
        """High-level overview of artificial intelligence."""
        prompt = """Provide a comprehensive overview of artificial intelligence for someone new to the topic.

        Include:
        - Definition: What is intelligence? What is artificial intelligence?
        - Types of AI: Narrow vs General, Reactive vs Self-aware
        - How AI differs from traditional programming
        - The three waves of AI: symbolic, statistical, connectionist
        - Current capabilities vs science fiction
        - Common misconceptions

        Make it thorough but accessible. ~500-600 words."""

        overview = call_openrouter(prompt)

        # Generate an AI landscape diagram
        image_prompt = "Conceptual diagram showing AI landscape: Narrow AI (many examples), AGI (one large central), ASI (future). Show connections to Machine Learning and Deep learning as subsets. Clean infographic style with icons."
        image_url = generate_image_url(image_prompt, width=1000, height=700)

        return {
            "overview": overview,
            "visualization_url": image_url
        }

    elif action == 'concepts':
        """Explain core AI/ML concepts."""
        concept_category = data.get('category', 'all')

        categories = {
            'all': "Explain the fundamental concepts that underpin modern AI and machine learning. Cover essential ideas everyone should know.",
            'ml_basics': "Explain what machine learning is: supervised, unsupervised, reinforcement learning; training vs inference; features and labels; overfitting and underfitting; model evaluation metrics.",
            'neural_networks': "Explain neural networks: neurons and layers, activation functions, backpropagation, gradient descent, loss functions, how they learn from data.",
            'deep_learning': "Explain deep learning: what makes networks 'deep', convolutional neural networks (CNNs), recurrent neural networks (RNNs), transformers, attention mechanism.",
            'nlp': "Explain natural language processing: tokenization, embeddings, language models, how models understand and generate text, current state of LLMs.",
            'computer_vision': "Explain computer vision: image classification, object detection, segmentation, how CNNs process images, vision transformers, multimodal models.",
            'generative': "Explain generative AI: how generative models work, diffusion models, GANs, VAEs, text-to-image, video generation, code generation.",
            'embeddings': "Explain embeddings: what they are, how they represent meaning, vector spaces, similarity search, RAG, retrieval systems."
        }

        prompt = categories.get(concept_category, categories['all']) + """

        For each concept:
        - Clear definition in plain language
        - Analogy or example when helpful
        - Why it matters
        - How it's used in practice

        Avoid unnecessary jargon, but define terms when introduced.
        Format with headings and bullet points for readability. ~400-500 words."""

        concepts = call_openrouter(prompt)

        return {
            "concepts": concepts,
            "category": concept_category
        }

    elif action == 'history':
        """Explore the history of AI."""
        timeline_period = data.get('period', 'full')

        periods = {
            'full': "Provide a chronological history of artificial intelligence from the 1940s to early 2026. Highlight key moments, breakthroughs, and paradigm shifts.",
            'early': "Cover the early years of AI (1940s-1960s): Turing test, perceptrons, early symbolic AI, Dartmouth workshop, first AI programs.",
            'winters': "Explain the AI winters: what they were, why they happened, funding cycles, promises vs reality, lessons learned.",
            'ml_rise': "Detail the rise of machine learning (1990s-2010s): support vector machines, decision trees, ensemble methods, the shift from rules to statistics.",
            'deep_learning': " chronicle the deep learning revolution (2012-present): AlexNet breakthrough, ImageNet, seq2seq, attention, transformers, GPT era, current frontier.",
            'future': "Where is AI heading? Speculate on next breakthroughs based on current research trends and trajectory."
        }

        prompt = periods.get(timeline_period, periods['full']) + """

        Structure:
        - Timeline with key years and events
        - Important figures and their contributions
        - Pivotal papers and models
        - Shifts in research focus and funding
        - Connecting threads between eras

        Make it engaging, not just a list. Tell the story of AI. ~500 words."""

        history = call_openrouter(prompt)

        # Generate timeline visualization
        image_prompt = "Timeline infographic of AI history: 1950s (Turing, Dartmouth), 1960s-70s (early AI), 1980s (expert systems), 1990s (machine learning), 2012 (AlexNet), 2017 (Transformer), 2018-2023 (GPT era), 2024-2026 (multimodal agents). Show evolutionary progression, clean design."
        image_url = generate_image_url(image_prompt, width=1200, height=600)

        return {
            "history": history,
            "period": timeline_period,
            "visualization_url": image_url
        }

    elif action == 'current_state':
        """Describe the current state of AI (early 2026)."""
        aspect = data.get('aspect', 'overview')

        aspects = {
            'overview': "What is the current state of AI in early 2026? Provide a snapshot of capabilities, limitations, and the overall landscape.",
            'models': "What are the most significant AI models as of early 2026? Include frontier models (GPT, Claude, Gemini), open source models (Llama, Mistral), and specialized models. Compare their capabilities.",
            'capabilities': "What can AI do today? Explain current capabilities in language, vision, reasoning, coding, math, creative tasks, and multimodal understanding. Also what can't it do?",
            'adoption': "How widely is AI adopted in 2026? Cover enterprise adoption, consumer apps, developer ecosystem, investment trends, and regulatory environment.",
            'research': "What are the active research frontiers in early 2026? What problems are researchers trying to solve? What papers and breakthroughs are shaping the field?",
            'infrastructure': "What infrastructure powers modern AI? Discuss compute requirements, training clusters, inference optimization, specialized hardware, and scaling trends."
        }

        prompt = aspects.get(aspect, aspects['overview']) + """

        Include:
        - Specific model names and their release timeframe
        - Performance benchmarks where relevant
        - Major players and their positioning
        - Notable trends and shifts
        - Real-world impact today

        Be factual and current. ~450-550 words."""

        state = call_openrouter(prompt)

        return {
            "current_state": state,
            "aspect": aspect
        }

    elif action == 'applications':
        """Explore AI applications across domains."""
        domain = data.get('domain', 'all')

        domains = {
            'all': "How is AI being applied across different fields in 2026? Provide a survey of real-world AI applications and their impact.",
            'healthcare': "AI in healthcare: medical imaging analysis, drug discovery, personalized treatment plans, health monitoring, clinical decision support, robotic surgery.",
            'science': "AI in scientific research: protein folding (AlphaFold), material discovery, climate modeling, astronomy, particle physics, hypothesis generation.",
            'education': "AI in education: personalized learning, automated tutoring, content generation, assessment, accessibility tools, administrative efficiency.",
            'business': "AI in business: customer service (chatbots), sales automation, marketing personalization, supply chain optimization, financial analysis, HR.",
            'creativity': "AI in creative fields: writing assistance, art and design generation, music composition, video editing, game content creation, architecture.",
            'coding': "AI in software development: code completion, bug detection, code review, test generation, documentation, architecture suggestions, low-code platforms.",
            'robotics': "AI in robotics: autonomous vehicles, warehouse robots, drones, humanoid robots, manufacturing, surgical robotics, home assistants.",
            'government': "AI in government and public sector: policy analysis, fraud detection, citizen services, cybersecurity, smart cities, emergency response."
        }

        prompt = domains.get(domain, domains['all']) + """

        For each application:
        - What AI technique is used
        - Example systems or companies
        - Measurable benefits or outcomes
        - Challenges and limitations
        - Future potential

        Provide concrete examples and avoid hype. ~400-500 words."""

        applications = call_openrouter(prompt)

        # Generate application metaphor visualization
        image_prompt = "AI as a Swiss Army knife or multi-tool, with different tools representing different applications: healthcare (medical cross), education (graduation cap), science (microscope), business (graph rising), creativity (paintbrush), coding (</>), robotics (robot). Central AI brain icon connecting them all. Modern infographic style."
        image_url = generate_image_url(image_prompt, width=1000, height=700)

        return {
            "applications": applications,
            "domain": domain,
            "visualization_url": image_url
        }

    elif action == 'ethics':
        """Cover AI ethics, safety, and societal implications."""
        topic = data.get('topic', 'overview')

        topics = {
            'overview': "What are the key ethical considerations in AI? Provide a comprehensive overview of AI ethics and safety.",
            'bias': "AI bias and fairness: sources of bias (data, labeling, design), real-world harms, detection methods, mitigation strategies, fairness metrics.",
            'safety': "AI safety: alignment problem, reward hacking, adversarial attacks, robustness, monitoring, control problem, research directions.",
            'privacy': "AI and privacy: data collection, surveillance, inference attacks, differential privacy, federated learning, regulations like GDPR.",
            'accountability': "Accountability in AI: who is responsible when AI fails? Transparency, explainability, audit trails, legal frameworks, standards.",
            'labor': "AI and the workforce: job displacement vs augmentation, reskilling, economic impacts, universal basic income, policy responses.",
            'misuse': "Misuse of AI: deepfakes, disinformation, cybersecurity attacks, autonomous weapons, plagiarism, fraud. Detection and countermeasures.",
            'environment': "Environmental impact of AI: energy consumption of training and inference, carbon footprint, efficiency improvements, sustainable AI.",
            'governance': "AI governance: international cooperation, regulations (EU AI Act, US Executive Order), standards bodies, industry self-regulation, open vs closed models."
        }

        prompt = topics.get(topic, topics['overview']) + """

        Structure:
        - The ethical challenge or issue clearly stated
        - Why it matters (real-world consequences)
        - Current approaches to address it
        - Debates and differing viewpoints
        - What individuals and organizations can do

        Be balanced, nuanced, and practical. ~450-550 words."""

        ethics = call_openrouter(prompt)

        return {
            "ethics": ethics,
            "topic": topic
        }

    elif action == 'glossary':
        """Generate an AI glossary with definitions."""
        letter = data.get('letter', 'all')
        custom_terms = data.get('terms', [])

        all_terms = [
            "Algorithm", "Alignment", "Attention", "Autoencoder", "Backpropagation",
            "Bias", "ChatGPT", "Classification", " Claude", "Convolution",
            "Dataset", "Deep Learning", "Embedding", "Fine-tuning", "GPT",
            "GPT-4", "Hallucination", "Inference", "LLM", "Loss Function",
            "Machine Learning", "Model", "Multimodal", "Neural Network", "Normalization",
            "OpenAI", "Overfitting", "Parameters", "Perplexity", "Prompt",
            "Quantization", "Reinforcement Learning", "Retrieval", "RAG", "Supervised Learning",
            "Tensor", "Token", "Transformer", "Underfitting", "Unsupervised Learning",
            "Vector", "Weights", "Zero-shot"
        ]

        if custom_terms:
            all_terms.extend(custom_terms)
            all_terms = list(set(all_terms))  # Deduplicate

        if letter != 'all':
            all_terms = [t for t in all_terms if t[0].upper() == letter.upper()]

        prompt = f"""Define the following AI/ML terms concisely and clearly: {', '.join(all_terms[:30])}

        For each term:
        - Definition (1-2 sentences)
        - Simple explanation or analogy if helpful
        - Context of use in AI

        Format as a clean glossary: Term: definition. One term per line, no markdown."""

        glossary_text = call_openrouter(prompt)

        # If there are more terms, we might need multiple calls or group them
        if len(all_terms) > 30:
            prompt2 = f"""Define these additional AI terms: {', '.join(all_terms[30:60])}

        Same format: Term: definition. One term per line."""
            glossary_text += "\n\n" + call_openrouter(prompt2)

        return {
            "glossary": glossary_text,
            "terms_total": len(all_terms),
            "letter": letter
        }

    elif action == 'deep_dive':
        """Deep dive into a specific AI topic."""
        topic = data.get('topic', 'transformer architecture')
        depth = data.get('depth', 'intermediate')  # beginner, intermediate, advanced

        prompt = f"""Provide a deep dive into {topic} for a {depth} level audience.

        Structure:
        1. Introduction and importance
        2. Core mechanics and how it works
        3. Historical development and key papers
        4. Current state and variations
        5. Practical applications and examples
        6. Limitations and challenges
        7. Future directions
        8. Further learning resources

        Make it educational and thorough, with technical depth appropriate for {depth} level.
        Use diagrams concepts, code snippets if helpful for explaining.
        ~700-900 words."""

        deep_dive = call_openrouter(prompt)

        # Generate topic-specific visualization
        image_prompt = f"Technical diagram explaining {topic}. Show components, flow, connections. Clean, educational style with labels. Blue and orange color scheme."
        image_url = generate_image_url(image_prompt, width=1000, height=700)

        return {
            "deep_dive": deep_dive,
            "topic": topic,
            "depth": depth,
            "visualization_url": image_url
        }

    elif action == 'quiz':
        """Generate a quiz about AI fundamentals."""
        prompt = """Generate 5 multiple-choice quiz questions about artificial intelligence fundamentals.

        Topics to cover:
        - Basic definitions and concepts
        - History and key milestones
        - How machine learning works
        - Types of AI and applications
        - Ethics and societal impact

        Questions should test understanding, not just trivia.

        Format as JSON array:
        [
          {
            "question": "string",
            "options": ["A) ...", "B) ...", "C) ...", "D) ..."],
            "correct": 0-3,
            "explanation": "Brief explanation with context"
          }
        ]

        Make sure correct answer is accurate and explanations are educational."""

        result = call_openrouter(prompt)
        quiz_data = extract_json(result)

        if not quiz_data:
            quiz_data = [
                {
                    "question": "What is the key difference between AI and traditional programming?",
                    "options": [
                        "A) AI uses if-else statements, traditional uses data",
                        "B) Traditional programming gives rules + data → answers; AI gives rules + answers → model",
                        "C) AI is only for large corporations",
                        "D) Traditional programming is faster"
                    ],
                    "correct": 1,
                    "explanation": "In traditional programming, we write rules (code) and apply them to data to get answers. In machine learning (a subset of AI), we give data and answers (labels) and the program learns the rules (model) that map them."
                }
            ]

        return {"quiz": quiz_data}

    elif action == 'resources':
        """Get curated learning resources for AI."""
        resource_type = data.get('type', 'all')

        types = {
            'all': "Provide comprehensive learning resources for AI: books, courses, websites, communities, tools, and more.",
            'books': "Recommend essential books for learning AI, from beginner to advanced. Include classic texts and modern books.",
            'courses': "List top online courses and MOOCs for learning AI and machine learning. Include free and paid options, with brief descriptions.",
            'websites': "Share must-visit websites for AI news, tutorials, research, and communities: blogs, arXiv, newsletters, forums.",
            'tools': "Introduce tools and platforms for AI development: frameworks (PyTorch, TensorFlow), cloud services, datasets, notebooks, visualization tools.",
            'papers': "Guide to reading AI research papers: how to approach them, seminal papers to start with, where to find papers, how to stay current."
        }

        prompt = types.get(resource_type, types['all']) + """

        For each resource:
        - Name and author/platform
        - Why it's valuable
        - Level (beginner/intermediate/advanced)
        - Link or where to find it

        Provide variety and practical value. ~400 words."""

        resources = call_openrouter(prompt)

        return {"resources": resources, "type": resource_type}

    else:
        return {"error": f"Unknown action: {action}"}


# Metadata for projects.json
META = {
    "name": "AI Fundamentals & Insights",
    "description": "A comprehensive guide to understanding artificial intelligence: core concepts, historical context, current state, practical applications, ethics, and future directions. Perfect for beginners and professionals seeking deep AI literacy.",
    "category": "About AI",
    "tags": ["education", "fundamentals", "concepts", "history", "ethics", "applications", "glossary", "literacy"],
    "difficulty": "Beginner Friendly"
}