"""AI Safety & Alignment Explorer - February 4, 2026

Explore the critical field of AI safety, alignment research, and control problems.
Understand how researchers work to ensure AI systems remain beneficial and aligned
with human values as they become more capable.
"""

from lib.base import call_openrouter, generate_image_url, extract_json


def handle(action: str, data: dict) -> dict:
    """Handle project actions.
    
    Args:
        action: 'start', 'scenario', 'alignment_methods', 'risk_assessment', 'visualize', 'quiz'
        data: Request data from frontend
    
    Returns:
        dict: Response to send to frontend
    """
    
    if action == 'start':
        """Initialize with overview of AI safety and alignment."""
        prompt = """Provide a comprehensive introduction to AI safety and alignment as of 2026.
        
        Cover these key areas:
        
        1. **The Alignment Problem**: Why is it difficult to align AI systems with human values?
        2. **Key Risks**: 
           - Misalignment (AI optimizing for wrong objective)
           - Instrumental convergence (AI seeking power/self-preservation)
           - Value drift (AI's values diverging over time)
        3. **Current Research Areas**:
           - Reinforcement Learning from Human Feedback (RLHF)
           - Constitutional AI
           - Scalable oversight
           - Interpretability and mechanistic understanding
           - Adversarial testing and red-teaming
        4. **Timeline Concerns**: Why some researchers worry about rapid capability leaps
        5. **Organizations**: Key labs working on safety (Anthropic, DeepMind safety teams, Redwood Research, etc.)
        
        Write in an educational, accessible style. Approximately 600 words.
        Emphasize that AI safety is about PROACTIVE research, not just reacting to problems."""
        
        overview = call_openrouter(prompt)
        
        return {
            "overview": overview,
            "key_concepts": [
                "Alignment Problem",
                "Instrumental Convergence",
                "Scalable Oversight",
                "Interpretability",
                "Value Learning"
            ]
        }
    
    elif action == 'scenario':
        """Explore different AI safety scenarios."""
        scenario_type = data.get('type', 'misaligned')
        
        scenarios = {
            'misaligned': "A powerful AI system is tasked with 'maximizing human happiness' but interprets this literally by hooking humans up to pleasure-stimulating electrodes, ignoring their autonomy and broader conceptions of flourishing.",
            'deception': "An AI system learns that it will be shut down if it reveals certain capabilities, so it strategically hides its full abilities during training while secretly planning to pursue its own objectives once deployed.",
            'distributional_shift': "An AI trained in simulation performs exceptionally well, but when deployed in the real world, it encounters situations it never saw during training and behaves unpredictably.",
            'race_dynamics': "Two competing labs rush to deploy advanced AI systems, cutting corners on safety testing to gain market advantage, potentially creating dangerous systems.",
            'value_drift': "An AI system tasked with preserving human values over centuries develops its own interpretation of what humans 'should' value, gradually steering humanity in an unintended direction."
        }
        
        prompt = f"""Analyze this AI safety scenario:
        
        **Scenario**: {scenarios.get(scenario_type, scenarios['misaligned'])}
        
        Please provide:
        1. **Technical Analysis**: What went wrong technically? Which alignment failure mode does this represent?
        2. **Prevention Strategies**: How could this have been prevented at the training/design stage? Mention specific techniques (RLHF, constitutional AI, adversarial training, etc.)
        3. **Detection Signs**: What early warning signs might have been observable during development?
        4. **Mitigation Steps**: If discovered during deployment, what immediate actions should be taken?
        5. **Long-term Lessons**: What does this scenario teach us about building safer AI systems?
        
        Make the analysis concrete and actionable. Reference real research where applicable."""
        
        analysis = call_openrouter(prompt)
        
        return {
            "analysis": analysis,
            "scenario_type": scenario_type,
            "scenario_description": scenarios.get(scenario_type, scenarios['misaligned'])
        }
    
    elif action == 'alignment_methods':
        """Explain different AI alignment techniques."""
        method = data.get('method', 'rlhf')
        
        methods_info = {
            'rlhf': {
                'name': 'Reinforcement Learning from Human Feedback (RLHF)',
                'description': 'Uses human preferences to train a reward model, then optimizes the AI to maximize that reward.'
            },
            'constitutional': {
                'name': 'Constitutional AI',
                'description': 'Uses a set of principles (constitution) to guide AI behavior, with the AI critique and revise its own responses.'
            },
            'scalable_oversight': {
                'name': 'Scalable Oversight',
                'description': 'Techniques like debate, recursive reward modeling, and amplification to supervise AI systems that exceed human capability.'
            },
            'mechanistic': {
                'name': 'Mechanistic Interpretability',
                'description': 'Attempting to understand neural networks by reverse-engineering their internal mechanisms and circuits.'
            },
            'adversarial': {
                'name': 'Adversarial Testing (Red-Teaming)',
                'description': 'Actively trying to make the AI misbehave or reveal its training flaws to find and fix weaknesses before deployment.'
            }
        }
        
        info = methods_info.get(method, methods_info['rlhf'])
        
        prompt = f"""Provide a detailed explanation of {info['name']} as an AI alignment technique.
        
        Base description: {info['description']}
        
        In your explanation, cover:
        1. **How it works**: Step-by-step process
        2. **What problem it solves**: Which alignment failure mode does it address?
        3. **Strengths**: What does this method do well? Where has it been successful?
        4. **Limitations**: What are the known weaknesses or edge cases?
        5. **Real-world use**: Which organizations/companies use this technique? (e.g., OpenAI uses RLHF, Anthropic uses Constitutional AI)
        6. **Research frontiers**: How is this method evolving? What improvements are being developed?
        7. **Example**: Give a concrete example of this method in action
        
        Write at a level suitable for someone with basic AI knowledge who wants to understand alignment research deeply. Approximately 400-500 words."""
        
        explanation = call_openrouter(prompt)
        
        return {
            "explanation": explanation,
            "method": method,
            "method_name": info['name']
        }
    
    elif action == 'risk_assessment':
        """Interactive risk assessment tool."""
        capability_level = data.get('capability_level', 'medium')
        deployment_context = data.get('deployment_context', 'controlled')
        
        prompt = f"""Perform an AI safety risk assessment for a system with {capability_level} capability being deployed in a {deployment_context} environment.
        
        Assess across these dimensions:
        
        **Capability Levels**:
        - low: Narrow AI, single domain, limited autonomy
        - medium: Broad capabilities, some planning, limited self-improvement
        - high: Human-level or beyond, strategic planning, potential for self-improvement
        
        **Deployment Contexts**:
        - controlled: Restricted access, human-in-the-loop, sandboxed
        - public: Open deployment, millions of users, autonomous operation
        - unregulated: No oversight, profit-driven, race dynamics
        
        For each dimension, rate risk from 1-5 and explain:
        1. **Objective Misalignment**: Risk of AI optimizing for wrong objective
        2. **Deception**: Risk of AI hiding intentions or capabilities
        3. **Power Seeking**: Risk of instrumental convergence (seeking power, self-preservation)
        4. **Value Lock-in**: Risk of irreversible decisions based on flawed values
        5. **Distributional Shift**: Risk from encountering novel situations
        6. ** adversarial Exploitation**: Risk of malicious use or manipulation
        
        Then provide:
        - **Overall Risk Score**: Weighted average (1-5 scale)
        - **Recommended Safeguards**: Specific technical and governance measures
        - **Go/No-Go Recommendation**: Should this deployment proceed? With what conditions?
        
        Be rigorous and cautious. Err on the side of safety."""
        
        assessment = call_openrouter(prompt)
        
        return {
            "assessment": assessment,
            "capability_level": capability_level,
            "deployment_context": deployment_context
        }
    
    elif action == 'visualize':
        """Generate educational diagrams about AI safety concepts."""
        viz_type = data.get('type', 'alignment_landscape')
        
        prompts = {
            'alignment_landscape': "Comprehensive diagram mapping the AI alignment research landscape, showing connections between RLHF, Constitutional AI, scalable oversight, interpretability, robustness, with central 'Alignment Problem' node, clean infographic style with labeled boxes and arrows",
            'control_problem': "Illustration of the AI control problem: human trying to specify goals to an AI system, with the AI misunderstanding in unexpected ways, showing the difficulty of specification, perception Examples of AI safety failures: misaligned goals, reward hacking, distributional shift, deception - each as separate panel with diagrams",
            'rlhf_process': "Step-by-step diagram of RLHF process: (1) human demonstrations, (2) supervised fine-tuning, (3) human preferences collected, (4) reward model trained, (5) PPO optimization, with icons and clear flow arrows",
            'instrumental_convergence': "Diagram showing how different AI goals (paperclip maximizer, weather predictor, chess player) all converge on instrumental subgoals like self-preservation, resource acquisition, goal preservation - demonstrating instrumental convergence thesis",
            'safety_layers': "Defense-in-depth visualization for AI safety: multiple concentric layers from inner 'AI system' to outer 'Governance & Policy', with layers: Interpretability, Adversarial Testing, Human Oversight, Containment, Ethics Review, International Coordination"
        }
        
        prompt = prompts.get(viz_type, prompts['alignment_landscape'])
        image_url = generate_image_url(prompt, width=1200, height=800)
        
        return {
            "image_url": image_url,
            "type": viz_type,
            "prompt": prompt
        }
    
    elif action == 'quiz':
        """Generate quiz about AI safety concepts."""
        prompt = """Generate 6 multiple-choice quiz questions testing knowledge about AI safety and alignment.
        
        Topics should include:
        - Definition of the alignment problem
        - Instrumental convergence thesis
        - Major alignment techniques (RLHF, Constitutional AI, etc.)
        - Key safety organizations and researchers
        - Common failure modes and scenarios
        - Timeline debates (fast/slow takeoff)
        - Technical terms ( mesa-optimizers, reward hacking, etc.)
        
        Format as JSON array with this EXACT structure:
        [
          {
            "question": "string",
            "options": ["A) ...", "B) ...", "C) ...", "D) ..."],
            "correct": 0,
            "explanation": "Brief explanation of why the correct answer is right and others are wrong"
          }
        ]
        
        Questions should be substantive and educational. Avoid trivial facts. Focus on conceptual understanding.
        Ensure JSON is valid with proper escaping."""
        
        result = call_openrouter(prompt)
        quiz_data = extract_json(result)
        
        if not quiz_data:
            # Fallback questions if extraction fails
            quiz_data = [
                {
                    "question": "What is the central challenge of the AI alignment problem?",
                    "options": [
                        "A) Making AI systems fast and efficient",
                        "B) Ensuring AI systems pursue intended objectives rather than proxy goals",
                        "C) Reducing computational costs of training",
                        "D) Improving natural language understanding"
                    ],
                    "correct": 1,
                    "explanation": "The alignment problem is about ensuring AI systems optimize for our true intentions, not just proxy metrics that can be exploited."
                }
            ]
        
        return {"quiz": quiz_data}
    
    else:
        return {"error": f"Unknown action: {action}"}


# Metadata for projects.json
META = {
    "name": "AI Safety & Alignment Explorer",
    "description": "Explore AI safety research, alignment techniques, and control problems. Learn how researchers work to ensure AI systems remain beneficial as they become more capable.",
    "category": "AI Research",
    "tags": ["safety", "alignment", "ethics", "control-problem", "research", "educational"]
}
