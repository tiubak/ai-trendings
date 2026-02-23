"""AI Fundamentals: About Artificial Intelligence - February 22, 2026

A comprehensive educational project explaining what Artificial Intelligence is,
how it works, its history, applications, ethical considerations, and how to get
started learning about this transformative technology.
"""

from ..base import call_openrouter, generate_image_url, extract_json


def handle(action: str, data: dict) -> dict:
    """Handle project actions.

    Args:
        action: 'start', 'history', 'types', 'how-it-works', 'applications',
                'ethics', 'future', 'get-started', 'quiz', 'explain'
        data: Request data from frontend

    Returns:
        dict: Response to send to frontend
    """

    if action == 'start':
        """Initialize with a welcoming overview of AI."""
        prompt = """Provide a comprehensive, accessible introduction to Artificial Intelligence for beginners.

        Cover these key questions:
        - What is AI? (simple definition)
        - Why is AI important today?
        - Brief history: from Turing to ChatGPT
        - AI vs human intelligence: what's similar, what's different?
        - Common AI terms explained (ML, deep learning, neural networks, LLMs)
        - Current capabilities and limitations
        - How AI is already in our daily lives

        Make it engaging and jargon-free where possible. Use analogies and real-world examples.
        ~600-700 words. Aim to inspire curiosity while being accurate."""

        overview = call_openrouter(prompt)

        # Generate a friendly, educational AI visualization
        image_prompt = "Friendly educational illustration about AI: a robot and human shaking hands, surrounded by icons representing machine learning, neural networks, data, and applications. Clean, modern, approachable style with bright colors and simple shapes."
        image_url = generate_image_url(image_prompt, width=1200, height=600)

        return {
            "overview": overview,
            "visualization_url": image_url,
            "date": "2026-02-22",
            "sections": [
                "history", "types", "how-it-works", "applications",
                "ethics", "future", "get-started", "quiz"
            ],
            "next_steps": "Explore the sections to dive deeper into any topic!"
        }

    elif action == 'history':
        """Explore the history and evolution of AI."""
        era = data.get('era', 'full')  # full, early, modern, recent

        prompts = {
            'full': """Create a comprehensive timeline of Artificial Intelligence from the 1940s to 2026.

                Structure it chronologically with these eras:
                - Birth of AI (1940s-1950s): Turing, Dartmouth Conference
                - Early optimism and winters (1960s-1970s): Symbolic AI, expert systems, first AI winter
                - Revival and knowledge systems (1980s): Expert systems boom, second AI winter
                - Machine learning rise (1990s-2000s): Statistical methods, IBM Deep Blue
                - Deep learning revolution (2010s): AlexNet, AlphaGo, GPT-1
                - LLM era (2020-2023): GPT-3, ChatGPT, Claude, Llama
                - 2024-2026: Multimodal models, reasoning, agentic AI

                For each era, highlight 3-4 key milestones with dates, brief descriptions,
                and their significance. Make it informative but concise. ~600 words.""",

            'early': "Focus on the early history of AI: 1940s through 1970s. Cover Turing's contributions, the Dartmouth Conference, early perceptrons, symbolic AI, ELIZA, expert systems, and the first AI winter. What were the key ideas and why did progress slow? ~300 words.",

            'modern': "Cover AI development from the 1980s through 2010s. Include the rise of machine learning, neural networks backpropagation, IBM Deep Blue defeating Kasparov, Watson on Jeopardy, and the deep learning revolution triggered by AlexNet in 2012. ~300 words.",

            'recent': "Focus on AI from 2018 to 2026. Cover the transformer architecture (2017), GPT series, Claude, Gemini, Llama, the explosion of open-source models, multimodal capabilities, reasoning improvements, and the trend toward smaller efficient models. Include key model release dates and breakthroughs. ~400 words."
        }

        prompt = prompts.get(era, prompts['full'])
        timeline = call_openrouter(prompt)

        # Generate historical visualization
        viz_prompt = "Historical timeline of AI evolution from 1950 to 2026: vintage computer symbols transitioning to modern neural network graphics, showing progression through different eras. Clean infographic style with a timeline axis."
        image_url = generate_image_url(viz_prompt, width=1400, height=500)

        return {
            "timeline": timeline,
            "era": era,
            "visualization_url": image_url
        }

    elif action == 'types':
        """Learn about different types and categories of AI."""
        category = data.get('category', 'all')  # all, capability, functionality, application

        prompt = f"""Explain the different ways AI is categorized and classified.

        Cover these classification systems:

        1. **By Capability** (how general the intelligence is):
           - Narrow/Weak AI: What it is, examples (Siri, recommendation systems)
           - General/Strong AI: Definition, current status, AGI vs narrow AI
           - Superintelligence: Hypothetical future AI surpassing human intelligence

        2. **By Functionality** (what the AI does):
           - Reactive machines (e.g., Deep Blue)
           - Limited memory (most current AI including self-driving car systems)
           - Theory of mind (future AI that understands emotions)
           - Self-aware AI (conscious machines, speculative)

        3. **By Technical Approach** (how it's built):
           - Symbolic/GOFAI (good old-fashioned AI)
           - Machine learning (supervised, unsupervised, reinforcement)
           - Deep learning/neural networks
           - Hybrid systems

        Provide clear definitions, concrete examples for each, and explain why these distinctions matter.
        Make it educational and easy to understand. ~500 words."""

        types_explanation = call_openrouter(prompt)

        # Generate classification diagram
        viz_prompt = "Hierarchical diagram showing AI classifications: tree structure with branches for Capability (Narrow, General, Super), Functionality (Reactive, Limited Memory, Theory of Mind, Self-aware), and Technical Approaches (Symbolic, ML, Deep Learning). Modern educational infographic style."
        image_url = generate_image_url(viz_prompt, width=1200, height=800)

        return {
            "explanation": types_explanation,
            "category": category,
            "visualization_url": image_url
        }

    elif action == 'how-it-works':
        """Understand how AI systems learn and operate."""
        level = data.get('level', 'beginner')  # beginner, intermediate, technical

        prompts = {
            'beginner': """Explain how AI (specifically machine learning) works in simple, intuitive terms.

                Use analogies and everyday examples. Cover:
                - What does it mean to "train" an AI?
                - The basic concept: learning from data, finding patterns
                - Simple example: how a spam filter learns
                - What are neural networks? (compare to brain neurons, but keep it simple)
                - What's a model? What are weights?
                - How does an AI make predictions?
                - Why do we need lots of data?
                - What's the role of algorithms and math?

                Avoid heavy technical jargon. Make it understandable to someone with no CS background.
                ~500 words.""",

            'intermediate': """Provide a more detailed explanation of how machine learning and deep learning work.

                Include:
                - The training process: data preparation, feature extraction, training loop
                - Loss functions and optimization (gradient descent)
                - Neural network architecture: layers, neurons, activation functions
                - Backpropagation: how networks learn from errors
                - Different ML paradigms: supervised, unsupervised, reinforcement learning
                - What transformers are and why they revolutionized NLP
                - Overfitting, regularization, and generalization

                Use technical terms but explain them clearly. Aim for someone with basic tech literacy.
                ~600 words.""",

            'technical': """Deliver a technical deep-dive into modern AI architectures.

                Cover:
                - Mathematical foundations: linear algebra, probability, calculus in ML
                - Neural network types: CNNs, RNNs, Transformers, GNNs
                - Attention mechanism and self-attention in detail
                - Transformer architecture: encoder-decoder, positional encoding, multi-head attention
                - Training at scale: distributed training, mixed precision, optimization algorithms
                - Inference optimization: quantization, pruning, distillation
                - Emerging architectures: Mamba, RWKV, state space models
                - Hardware considerations: TPUs, GPUs, memory bandwidth

                This should be technical and detailed, suitable for developers or researchers.
                Include specific equations or concepts where relevant. ~700 words."""
        }

        prompt = prompts.get(level, prompts['beginner'])
        explanation = call_openrouter(prompt)

        # Generate educational diagram
        level_prompt = "simple cartoon neurons" if level == 'beginner' else "detailed neural network architecture diagram" if level == 'intermediate' else "advanced mathematical diagram of attention mechanism"
        viz_prompt = f"Educational visualization explaining AI: {level_prompt}, clean technical illustration style."
        image_url = generate_image_url(viz_prompt, width=1200, height=600)

        return {
            "explanation": explanation,
            "level": level,
            "visualization_url": image_url
        }

    elif action == 'applications':
        """Explore real-world AI applications across industries."""
        industry = data.get('industry', 'all')  # all, healthcare, finance, education, etc.

        prompt = f"""Survey how AI is being applied across different industries as of 2026.

        For each major sector, cover:
        - Key use cases and applications
        - Specific examples with real products/companies
        - Measurable impacts (efficiency gains, cost savings, etc.)
        - Challenges and limitations in that sector

        Sectors to include:
        • Healthcare: diagnostics, drug discovery, personalized medicine, medical imaging
        • Finance: fraud detection, algorithmic trading, risk assessment, robo-advisors
        • Education: personalized learning, automated grading, tutoring systems
        • Manufacturing: predictive maintenance, quality control, supply chain optimization
        • Retail & E-commerce: recommendations, inventory management, visual search
        • Entertainment: content creation, gaming NPCs, video generation, music composition
        • Transportation: autonomous vehicles, traffic optimization, route planning
        • Customer Service: chatbots, virtual assistants, sentiment analysis
        • Agriculture: precision farming, crop monitoring, yield prediction
        • Energy: grid optimization, demand forecasting, renewable integration

        {f"Add a detailed section specifically on {industry}." if industry != 'all' else ""}

        Use concrete examples with company/product names where possible.
        Include both successes and ongoing challenges. ~800-1000 words."""

        applications_text = call_openrouter(prompt)

        # Generate application collage
        viz_prompt = "Collage of AI applications across industries: medical cross and DNA, stock charts and finance, student with tablet, factory robot, shopping cart with recommendations, self-driving car, smart speaker, fields with drones. Connected by neural network. Vibrant, professional infographic."
        image_url = generate_image_url(viz_prompt, width=1400, height=700)

        return {
            "applications": applications_text,
            "industry": industry,
            "visualization_url": image_url
        }

    elif action == 'ethics':
        """Explore AI ethics, bias, and responsible development."""
        topic = data.get('topic', 'overview')  # overview, bias, fairness, transparency, safety

        prompt = f"""Discuss ethical considerations in AI development and deployment.

        Focus on: {topic if topic != 'overview' else 'comprehensive overview'}

        Include:
        - The main ethical challenges in AI today
        - Real-world examples of AI bias and harm (e.g., facial recognition issues, hiring algorithms, criminal justice)
        - Concepts: algorithmic fairness, explainability, transparency, accountability
        - Mitigation strategies: diverse datasets, fairness audits, interpretability methods
        - AI safety research: alignment, value loading, instrumental convergence
        - Regulatory approaches (EU AI Act, US executive orders, industry self-regulation)
        - The role of developers, companies, and users in responsible AI
        - Current best practices and frameworks (IEEE, NIST, etc.)

        Be concrete and grounded. Use specific incidents or studies to illustrate points.
        Discuss both technical and governance aspects. ~600-700 words."""

        ethics_content = call_openrouter(prompt)

        # Generate ethics-themed visual
        viz_prompt = "Balance scale symbolizing AI ethics: one side has technology icons (robot, code), the other side has human values symbols (heart, fairness shield, transparent glass). Thoughtful, balanced composition. Technology meets humanity."
        image_url = generate_image_url(viz_prompt, width=1200, height=600)

        return {
            "content": ethics_content,
            "topic": topic,
            "visualization_url": image_url
        }

    elif action == 'future':
        """Discuss the future of AI, AGI, and societal impact."""
        perspective = data.get('perspective', 'balanced')  # balanced, optimistic, cautious, timeline

        prompt = f"""Explore the future of Artificial Intelligence from a {perspective} perspective.

        Address:
        - Timeline predictions for AGI (years to decades? by 2050?)
        - Potential benefits of advanced AI: solving global challenges, scientific discovery, economic growth
        - Risks and concerns: job displacement, autonomous weapons, loss of human agency, existential risk
        - Societal transformations: changes to work, education, relationships, creativity
        - The alignment problem: how to ensure AI goals match human values
        - Governance and policy: international cooperation, regulation needs
        - The singularity concept: is it plausible? What would it mean?
        - Scenarios for different futures (near-term vs long-term)

        Present multiple viewpoints. Acknowledge uncertainty while being informed.
        Consider technical, social, and philosophical dimensions. ~700 words."""

        future_content = call_openrouter(prompt)

        # Generate visionary visual
        viz_prompt = "Futuristic vision of AI and humanity coexisting: humans and AI robots collaborating in a utopian cityscape with flying vehicles, green energy, and advanced technology. Optimistic, hopeful, not dystopian. Bright colors, harmonious composition."
        image_url = generate_image_url(viz_prompt, width=1400, height=700)

        return {
            "content": future_content,
            "perspective": perspective,
            "visualization_url": image_url
        }

    elif action == 'get-started':
        """Provide resources and roadmap for learning AI."""
        resource_type = data.get('type', 'roadmap')  # roadmap, courses, books, tools, communities

        prompts = {
            'roadmap': """Outline a learning roadmap for someone wanting to understand AI and machine learning from scratch.

                Create a structured path with stages:
                Stage 1: Foundation (math prerequisites: linear algebra, probability, calculus, Python)
                Stage 2: Introduction to ML (what is ML, basic algorithms like linear regression, decision trees)
                Stage 3: Deep Learning (neural networks, CNNs, RNNs, transformers)
                Stage 4: Specialization (NLP, computer vision, reinforcement learning, etc.)
                Stage 5: Advanced Topics (research papers, cutting-edge models, ML engineering)
                Stage 6: Building Projects (portfolio ideas, open source contributions)

                For each stage, list:
                - Key concepts to learn
                - Recommended resources (courses, books, tutorials)
                - Estimated time commitment
                - How to know when you're ready for next stage

                Make it actionable and realistic. Include both free and paid options.
                Consider self-learners, students, and career-changers.""",

            'courses': """Curate the best online courses for learning AI and machine learning in 2026.

                Include platforms like Coursera, edX, Udacity, fast.ai, etc.
                For each course provide:
                - Title and instructor/platform
                - Level (beginner/intermediate/advanced)
                - Duration and format
                - What topics it covers
                - Why it's recommended
                - Cost (free/paid)
                - URL (placeholder format)

                Categorize by:
                - Beginner-friendly introductions
                - Comprehensive ML engineering programs
                - Deep learning specializations
                - Math and theory foundations
                - Practical project-based courses

                List 15-20 top courses with variety.""",

            'books': """Recommend essential books for learning about AI, machine learning, and the implications of AI.

                Include categories:
                - Textbooks (e.g., Pattern Recognition and Machine Learning, Deep Learning)
                - Popular science (e.g., Superintelligence, Life 3.0, The Alignment Problem)
                - Practical guides (e.g., Hands-On Machine Learning)
                - Ethics and society (e.g., Weapons of Math Destruction, Human Compatible)
                - Historical perspectives (e.g., The Quest for Artificial Intelligence)

                For each book: title, author, brief description (2-3 sentences), level (technical/general), and why it's worth reading.
                Aim for 20-25 books total.""",

            'tools': """List essential tools and frameworks for AI development in 2026.

                Categories:
                - Deep Learning Frameworks (PyTorch, TensorFlow, JAX)
                - ML Libraries (scikit-learn, XGBoost, LightGBM)
                - LLM Tools (LangChain, LlamaIndex, vLLM, Ollama)
                - Data Processing (pandas, NumPy, Apache Spark)
                - Visualization (matplotlib, seaborn, Plotly, TensorBoard)
                - MLOps (MLflow, Weights & Biases, Kubeflow)
                - Cloud Platforms (AWS SageMaker, GCP Vertex AI, Azure ML)
                - Development Environments (Jupyter, VS Code with extensions)

                For each tool: name, brief description, primary use case, learning curve, and getting started tip.""",

            'communities': """Identify the best communities for AI learners and practitioners.

                Include:
                - Online forums (Reddit r/MachineLearning, Stack Overflow, AI Alignment Forum)
                - Discord/Slack communities (Hugging Face, PyTorch, TensorFlow)
                - Social media (Twitter/X AI community, LinkedIn groups)
                - Conferences and events (NeurIPS, ICML, ICLR, local meetups)
                - Open source projects to contribute to
                - Academic resources (arXiv, Papers With Code)

                For each: name, description, audience level, how to join/participate, and what makes it valuable."""
        }

        prompt = prompts.get(resource_type, prompts['roadmap'])
        resources_text = call_openrouter(prompt)

        # Try to structure as JSON if it's a list type
        if resource_type in ['courses', 'books', 'tools', 'communities']:
            resources = extract_json(resources_text)
            if resources:
                return {
                    "resources": resources,
                    "type": resource_type
                }

        return {
            "resources": resources_text,
            "type": resource_type
        }

    elif action == 'quiz':
        """Generate an interactive quiz to test AI knowledge."""
        topic = data.get('topic', 'general')  # general, history, types, how-it-works
        difficulty = data.get('difficulty', 'medium')  # easy, medium, hard

        prompt = f"""Generate a quiz with 5 multiple-choice questions to test knowledge about AI.

        Topic: {topic}
        Difficulty: {difficulty}

        Questions should cover:
        - Basic definitions and concepts
        - Historical facts
        - Technical understanding (appropriate to difficulty)
        - Real-world applications
        - Ethical considerations

        Format as a JSON array with this exact structure:
        [
          {{
            "id": 1,
            "question": "Clear, concise question text",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "correct_index": 0,
            "explanation": "Brief explanation (2-3 sentences) of why the answer is correct"
          }}
        ]

        Make questions educational - even if someone gets them wrong, they should learn something.
        Ensure explanations are informative. Avoid trick questions.
        Return ONLY valid JSON, no extra text."""

        result = call_openrouter(prompt)
        quiz_data = extract_json(result)

        if not quiz_data:
            # Fallback quiz
            quiz_data = [
                {
                    "id": 1,
                    "question": "What does AI stand for?",
                    "options": ["Automated Intelligence", "Artificial Intelligence", "Advanced Integration", "Algorithmic Implementation"],
                    "correct_index": 1,
                    "explanation": "AI stands for Artificial Intelligence, which refers to computer systems that can perform tasks typically requiring human intelligence."
                }
            ]

        return {
            "quiz": quiz_data,
            "topic": topic,
            "difficulty": difficulty,
            "total_questions": len(quiz_data)
        }

    elif action == 'explain':
        """Explain a specific AI concept on demand."""
        concept = data.get('concept', '')
        if not concept:
            return {"error": "No concept specified"}

        prompt = f"""Explain the AI/ML concept: "{concept}"

        Provide:
        1. Simple definition in one sentence
        2. More detailed explanation with analogies or examples
        3. Why it's important or what problem it solves
        4. How it relates to other concepts
        5. Real-world applications or instances

        Keep it clear and accessible. Use plain language. Make it useful for a beginner/intermediate learner.
        ~200-300 words."""

        explanation = call_openrouter(prompt)

        # Generate concept-specific visualization
        viz_prompt = f"Clear educational diagram explaining {concept}: simple icons, flow charts, or visual metaphors that make the concept easy to understand. Clean, minimalist infographic style."
        image_url = generate_image_url(viz_prompt, width=1000, height=500)

        return {
            "concept": concept,
            "explanation": explanation,
            "visualization_url": image_url
        }

    else:
        return {"error": f"Unknown action: {action}"}


# Metadata for projects.json
META = {
    "name": "AI Fundamentals: About Artificial Intelligence",
    "description": "A comprehensive educational guide to AI. Learn what AI is, how it works, its history, real-world applications, ethical considerations, and how to start your AI learning journey.",
    "category": "AI Education",
    "tags": ["fundamentals", "beginner", "educational", "history", "ethics", "tutorial", "learning"],
    "difficulty": "Beginner to Intermediate"
}