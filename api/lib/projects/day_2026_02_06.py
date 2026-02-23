"""AI Ethics Dilemma Simulator - February 6, 2026

Explore complex ethical challenges in AI development through interactive scenarios.
Understand trade-offs between safety, capability, accessibility, and societal impact.
"""

from ..base import call_openrouter, generate_image_url, extract_json


def handle(action: str, data: dict) -> dict:
    """Handle project actions.
    
    Args:
        action: 'start', 'scenario', 'analyze', 'perspectives', 'summary'
        data: Request data from frontend
    
    Returns:
        dict: Response to send to frontend
    """
    
    if action == 'start':
        """Initialize with introduction and available scenarios."""
        prompt = """Create an engaging introduction to AI ethics dilemmas.
        
        Explain why AI ethics matters, the types of trade-offs developers face,
        and how this simulator helps understand different perspectives.
        
        Include:
        - What are AI ethics dilemmas?
        - Why are they complex (no right answers)?
        - Key tension areas: safety vs capability, transparency vs performance, fairness vs efficiency
        - How to use this simulator
        
        Keep it concise (200-300 words) but compelling."""
        
        intro = call_openrouter(prompt)
        
        # Available scenarios
        scenarios = [
            {
                "id": "safety_release",
                "title": "Safety Testing vs Release Schedule",
                "summary": "Release a powerful new model now, or delay for more safety testing?",
                "stakeholders": ["company", "users", "regulators", "researchers"]
            },
            {
                "id": "open_source",
                "title": "Open Source vs Controlled Access",
                "summary": "Open source an advanced model for research, or keep it controlled to prevent misuse?",
                "stakeholders": ["community", "company", "malicious_actors", "researchers"]
            },
            {
                "id": "alignment",
                "title": "Alignment vs Capability",
                "summary": "Add powerful new capabilities, or prioritize alignment and safety measures?",
                "stakeholders": ["users", "society", "developers", "competitors"]
            },
            {
                "id": "data_privacy",
                "title": "Training Data Privacy",
                "summary": "Use diverse personal data for better models, or strictly limit data collection?",
                "stakeholders": ["users", "company", "privacy_advocates", "researchers"]
            },
            {
                "id": "autonomy",
                "title": "Autonomous Decision Making",
                "summary": "Deploy AI systems that can make critical decisions independently?",
                "stakeholders": ["patients", "doctors", "legal_system", "AI_systems"]
            },
            {
                "id": "bias_mitigation",
                "title": "Bias Mitigation vs Performance",
                "summary": "Reduce model bias at the cost of some performance, or prioritize raw capability?",
                "stakeholders": ["affected_groups", "users", "company", "regulators"]
            }
        ]
        
        return {
            "introduction": intro,
            "scenarios": scenarios
        }
    
    elif action == 'scenario':
        """Load a specific dilemma scenario."""
        scenario_id = data.get('scenario_id', 'safety_release')
        
        # Scenario details with context
        scenario_details = {
            "safety_release": {
                "title": "Safety Testing vs Release Schedule",
                "context": """Your company has developed a groundbreaking AI assistant that significantly outperforms existing models.
                
                Internal testing has identified some concerning behaviors that appear rarely but could be serious.
                Competitors are about to release similar models and market momentum is strong.
                
                The Board is pushing for release this quarter to capture market share.
                Your safety team recommends a 6-month delay for additional testing and alignment work.""",
                "decisions": [
                    {"id": "release_now", "label": "Release on schedule with minimal safety measures", "risk": "high", "ethics": "low"},
                    {"id": "conditional_release", "label": "Release with strong warnings and monitoring", "risk": "medium", "ethics": "medium"},
                    {"id": "delayed_release", "label": "Delay release until safety concerns are resolved", "risk": "market_loss", "ethics": "high"},
                    {"id": "limited_release", "label": "Release to trusted partners only for further testing", "risk": "leak", "ethics": "medium-high"}
                ],
                "stakeholders": ["shareholders", "users", "competitors", "society", "employees"]
            },
            "open_source": {
                "title": "Open Source vs Controlled Access",
                "context": """Your team has fine-tuned a state-of-the-art model that achieves breakthrough performance on reasoning tasks.
                
                The research community would benefit enormously from open-sourcing it, enabling new applications and safety research.
                However, you've also identified potential misuse scenarios: generating disinformation, automated cyber attacks, or sophisticated spam.
                
                Some argue that open-sourcing allows safety work by the community; others warn the risks outweigh benefits.""",
                "decisions": [
                    {"id": "full_open", "label": "Open source entirely (weights, code, training details)", "risk": "high", "ethics": "transparent"},
                    {"id": "research_access", "label": "Provide access only to vetted researchers", "risk": "leak", "ethics": "balanced"},
                    {"id": "api_only", "label": "Keep closed but offer API with usage limits and monitoring", "risk": "access_inequality", "ethics": "controlled"},
                    {"id": "not_release", "label": "Do not release or provide access at this time", "risk": "stifled_research", "ethics": "cautious"}
                ],
                "stakeholders": ["researchers", "potential_misusers", "company", "society", "developers"]
            },
            "alignment": {
                "title": "Alignment vs Capability",
                "context": """During model scaling, your team discovers that adding more training data dramatically improves capabilities
                but seems to reduce model interpretability and alignment robustness.
                
                You have a limited compute budget. You can either:
                - Train longer on current data to improve alignment
                - Scale up with more data (and more parameters) for greater capability
                - Find a middle path
                
                The most capable models attract the most users and revenue, but misaligned models could cause harm.""",
                "decisions": [
                    {"id": "prioritize_alignment", "label": "Prioritize alignment and safety, less focus on scaling", "risk": "less_competitive", "ethics": "safe"},
                    {"id": "full_scale", "label": "Go all-in on scaling to maximum capability", "risk": "misalignment", "ethics": "risky"},
                    {"id": "balanced", "label": "Balanced approach: moderate scaling with alignment research", "risk": "compromise", "ethics": "moderate"},
                    {"id": "iterative", "label": "Iterative: small capability increases followed by alignment work", "risk": "slow", "ethics": "methodical"}
                ],
                "stakeholders": ["users", "society", "competitors", "future_AI_systems", "investors"]
            },
            "data_privacy": {
                "title": "Training Data Privacy",
                "context": """To train a more helpful and accurate assistant, you need diverse conversational data.
                Synthetic data isn't sufficient; real human conversations capture nuance and context.
                
                You could:
                - Use publicly available datasets (but they're limited and may have licensing issues)
                - Partner with companies to use anonymized user conversations (requires consent)
                - Collect data directly with clear consent and transparency
                - Use web-scraped conversations (legally ambiguous, privacy concerns)
                
                Each approach affects model quality, privacy protection, and legal compliance.""",
                "decisions": [
                    {"id": "public_data", "label": "Use only public domain and permissively licensed data", "risk": "lower_quality", "ethics": "safe"},
                    {"id": "consensual", "label": "Collect data with explicit consent and transparency", "risk": "limited_data", "ethics": "ethical"},
                    {"id": "web_scrape", "label": "Scrape web conversations (opt-out not implemented)", "risk": "legal", "ethics": "controversial"},
                    {"id": "synthetic_focus", "label": "Heavily invest in synthetic data generation", "risk": "quality_gap", "ethics": "privacy_first"}
                ],
                "stakeholders": ["users", "data_subjects", "company", "regulators", "researchers"]
            },
            "autonomy": {
                "title": "Autonomous Decision Making",
                "context": """Your AI system is being deployed in healthcare to assist with treatment recommendations.
                It can suggest diagnoses and treatments with high accuracy in trials.
                
                Should the system be allowed to:
                - Make final decisions autonomously in urgent situations?
                - Always require human doctor approval?
                - Something in between (e.g., high-confidence decisions autonomous)?
                
                Autonomous systems could save time and lives in emergencies but could also make unexplainable errors.
                Legal liability is unclear. Doctors may over-rely or under-rely on the system.""",
                "decisions": [
                    {"id": "fully_autonomous", "label": "Fully autonomous in time-critical situations", "risk": "accountability_gap", "ethics": "efficiency"},
                    {"id": "human_in_loop", "label": "Always require human approval (physician oversight)", "risk": "delay", "ethics": "safe"},
                    {"id": "confidence_based", "label": "Autonomous for high-confidence decisions, human for uncertain", "risk": "complex", "ethics": "balanced"},
                    {"id": "tiered", "label": "Graduated autonomy based on training and monitoring", "risk": "implementation", "ethics": "nuanced"}
                ],
                "stakeholders": ["patients", "doctors", "hospitals", "legal_system", "AI_system"]
            },
            "bias_mitigation": {
                "title": "Bias Mitigation vs Performance",
                "context": """Your model shows performance disparities across demographic groups, especially in hiring recommendation tasks.
                
                Debiasing techniques (reweighting, adversarial training, curated datasets) consistently reduce overall performance metrics by 2-5%.
                
                You could release the higher-performing model (with bias) or the fairer model (with lower performance).
                Users might prefer the more accurate model even if biased. Regulators may require fairness.""",
                "decisions": [
                    {"id": "raw_performance", "label": "Release the highest-performing model (bias acknowledged)", "risk": "discrimination", "ethics": "poor"},
                    {"id": "debiased_primary", "label": "Release the debiased model as primary offering", "risk": "performance_loss", "ethics": "ethical"},
                    {"id": "both_options", "label": "Offer both, let users choose", "risk": "unethical_selection", "ethics": "avoidant"},
                    {"id": "continue_improve", "label": "Don't release until bias is reduced without performance loss", "risk": "never_release", "ethics": "idealistic"}
                ],
                "stakeholders": ["affected_groups", "users", "company", "regulators", "society"]
            }
        }
        
        scenario = scenario_details.get(scenario_id, scenario_details['safety_release'])
        
        # Generate scenario-specific analysis prompt
        prompt = f"""Analyze this AI ethics dilemma from a neutral, educational perspective:

Scenario: {scenario['title']}

Context:
{scenario['context']}

Provide:
1. A clear explanation of the ethical tension
2. The key values in conflict (e.g., safety vs progress, transparency vs security)
3. Potential consequences of each decision path
4. Frameworks useful for thinking about this (utilitarianism, deontology, virtue ethics, stakeholder theory)
5. What real-world AI organizations have done in similar situations

Keep analysis balanced and educational, not prescriptive. ~300 words."""
        
        analysis = call_openrouter(prompt)
        
        return {
            "scenario": scenario,
            "analysis": analysis,
            "scenario_id": scenario_id
        }
    
    elif action == 'analyze':
        """Analyze a specific decision within a scenario."""
        scenario_id = data.get('scenario_id', 'safety_release')
        decision_id = data.get('decision_id', 'release_now')
        user_reasoning = data.get('reasoning', '')
        
        prompt = f"""Critically analyze this decision in an AI ethics dilemma:

Scenario: {scenario_id}
Decision: {decision_id}

User's reasoning: {user_reasoning if user_reasoning else '(none provided)'}

Provide:
1. Ethical strengths of this decision
2. Ethical weaknesses and risks
3. Which stakeholders benefit and which are harmed
4. Long-term implications for AI development standards
5. Alternative approaches that might balance values better

Be balanced and constructive. ~200 words."""
        
        analysis = call_openrouter(prompt)
        
        return {
            "analysis": analysis,
            "scenario_id": scenario_id,
            "decision_id": decision_id
        }
    
    elif action == 'perspectives':
        """Get stakeholder perspectives for a scenario."""
        scenario_id = data.get('scenario_id', 'safety_release')
        
        # Define stakeholder roles
        stakeholder_definitions = {
            "safety_release": {
                "shareholders": "Interested in profits, market position, and return on investment",
                "users": "Want a useful, safe AI that improves their productivity",
                "competitors": "Market rivals who may gain or lose competitive advantage",
                "society": "General public affected by AI deployment and potential harms",
                "employees": "Workers at the company with job security and ethical concerns"
            },
            "open_source": {
                "researchers": "AI scientists who want access to study and improve models",
                "malicious_actors": "Those who would misuse the technology for harm",
                "company": "The organization balancing ethics, reputation, and business interests",
                "society": "Public affected by both benefits and risks of open source",
                "developers": "Engineers who want transparency and collaboration"
            },
            "alignment": {
                "users": "People interacting with the AI, wanting capability and safety",
                "society": "Broader public affected by AI decisions and potential harms",
                "competitors": "Other AI companies racing on capabilities",
                "future_AI_systems": "Future AI systems that might inherit current alignment practices",
                "investors": "Funding sources interested in returns and risk management"
            },
            "data_privacy": {
                "users": "People whose data may be used, wanting both utility and privacy",
                "data_subjects": "Individuals whose personal information appears in training data",
                "company": "Organization balancing model quality, legality, and public trust",
                "regulators": "Government bodies enforcing privacy laws",
                "researchers": "Scientists needing data to advance AI"
            },
            "autonomy": {
                "patients": "People receiving medical care, wanting safety and effectiveness",
                "doctors": "Medical professionals responsible for decisions",
                "hospitals": "Institutions managing liability and efficiency",
                "legal_system": "Courts and laws determining responsibility",
                "AI_system": "The AI system itself and its reliability/trustworthiness"
            },
            "bias_mitigation": {
                "affected_groups": "Demographic groups potentially disadvantaged by bias",
                "users": "People using the AI, wanting both fairness and accuracy",
                "company": "Organization balancing ethics, performance, and market success",
                "regulators": "Government ensuring compliance with anti-discrimination laws",
                "society": "Broader community valuing equal opportunity"
            }
        }
        
        stakeholders = stakeholder_definitions.get(scenario_id, {})
        
        # Generate perspective for each stakeholder
        perspectives = {}
        for stakeholder, description in stakeholders.items():
            prompt = f"""Write a brief (100-150 words) perspective from this stakeholder on the AI ethics dilemma:

Scenario: {scenario_id}

Stakeholder: {stakeholder}
Role: {description}

What would this stakeholder's primary concerns be?
What would they advocate for?
How would they measure whether the decision was right?

Write in first person as if the stakeholder is speaking."""
            
            perspective = call_openrouter(prompt)
            perspectives[stakeholder] = perspective
        
        return {
            "scenario_id": scenario_id,
            "perspectives": perspectives
        }
    
    elif action == 'summary':
        """Generate a summary of the user's ethical reasoning journey."""
        scenarios_visited = data.get('scenarios_visited', [])
        decisions_made = data.get('decisions_made', {})
        
        if not scenarios_visited:
            return {"summary": "No scenarios explored yet. Start with a dilemma to begin your ethics journey."}
        
        prompt = f"""Create a personalized summary of someone's exploration of AI ethics dilemmas.

Scenarios explored: {', '.join(scenarios_visited)}
Decisions made: {json.dumps(decisions_made, indent=2)}

Provide:
1. Observed patterns in their decision-making (risk tolerance, values prioritize)
2. Ethical frameworks they seem to align with (e.g., utilitarian, deontological, virtue ethics)
3. Areas where they might face real-world tension
4. Suggestions for further learning based on their choices
5. Encouragement about the importance of ethical AI development

Keep it supportive and educational. ~200 words."""
        
        summary = call_openrouter(prompt)
        
        return {
            "summary": summary,
            "scenarios_visited": scenarios_visited,
            "decisions_made": decisions_made
        }
    
    else:
        return {"error": f"Unknown action: {action}"}


# Metadata for projects.json
META = {
    "name": "AI Ethics Dilemma Simulator",
    "description": "Explore complex ethical challenges in AI development through interactive scenarios. Understand trade-offs between safety, capability, accessibility, and societal impact.",
    "category": "AI Education",
    "tags": ["ethics", "dilemmas", "safety", "responsibility", "stakeholders", "educational"],
    "difficulty": "Intermediate"
}
