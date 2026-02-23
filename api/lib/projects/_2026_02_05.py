"""AI Ethics Dilemma Simulator - February 5, 2026

Explore real-world ethical dilemmas in AI systems. Make decisions, see consequences,
and understand the complex trade-offs in AI ethics including bias, safety, privacy,
and accountability.
"""

from lib.base import call_openrouter, generate_image_url, extract_json


def handle(action: str, data: dict) -> dict:
    """Handle project actions.
    
    Args:
        action: 'start', 'get_dilemma', 'analyze', 'frameworks', 'compare'
        data: Request data from frontend
    
    Returns:
        dict: Response to send to frontend
    """
    
    if action == 'start':
        """Initialize with introduction and available dilemmas."""
        intro_prompt = """Provide an engaging introduction to AI ethics and why ethical dilemmas are critical in AI development.

Cover:
- What AI ethics is and why it matters
- Real-world examples of ethical failures and successes
- The tension between innovation and safety
- Who is responsible for AI ethics (developers, companies, regulators, users?)
- How ethical considerations differ across AI applications (healthcare, autonomous vehicles, hiring, etc.)

Make it accessible to developers and tech enthusiasts, around 300-400 words."""
        
        introduction = call_openrouter(intro_prompt)
        
        # List of available dilemma scenarios
        dilemmas = [
            {
                "id": "autonomous_vehicle",
                "title": "Autonomous Vehicle Trolley Problem",
                "category": "Safety & Life-or-Death Decisions",
                "description": "Self-driving car must choose between harming passengers or pedestrians in an unavoidable crash."
            },
            {
                "id": "hiring_bias",
                "title": "Algorithmic Hiring Bias",
                "category": "Fairness & Discrimination",
                "description": "Resume screening algorithm shows bias against certain demographic groups despite no explicit protected features."
            },
            {
                "id": "facial_recognition",
                "title": "Facial Recognition in Public Spaces",
                "category": "Privacy & Surveillance",
                "description": "Should cities use facial recognition for public safety? What about in private businesses or schools?"
            },
            {
                "id": "medical_diagnosis",
                "title": "AI Medical Diagnosis Trade-offs",
                "category": "Accountability & Risk",
                "description": "AI diagnostic tool is 95% accurate but makes catastrophic errors the other 5%. Who is liable?"
            },
            {
                "id": "deepfake_governance",
                "title": "Deepfake Detection vs. Free Speech",
                "category": "Misinformation & Rights",
                "description": "How should platforms balance preventing deepfake abuse with protecting legitimate expression and satire?"
            },
            {
                "id": "recommendation_amplification",
                "title": "Engagement-Optimized Recommendations",
                "category": "Mental Health & Social Impact",
                "description": "Algorithms that maximize engagement often promote extreme content. Should engagement be the primary metric?"
            }
        ]
        
        return {
            "introduction": introduction,
            "dilemmas": dilemmas
        }
    
    elif action == 'get_dilemma':
        """Get detailed scenario for a specific dilemma."""
        dilemma_id = data.get('dilemma_id', 'autonomous_vehicle')
        
        # Define detailed scenarios
        scenarios = {
            'autonomous_vehicle': {
                'title': 'Autonomous Vehicle Trolley Problem',
                'background': """You are a software engineer at a self-driving car company. Your team is programming the decision-making system for unavoidable crash scenarios.

The scenario: An autonomous vehicle carrying a family of four is driving down a narrow street. Suddenly, a group of 3 pedestrians steps into the road, and there's no way to stop in time. The car must choose:
- Option A: Swerve into a concrete wall, likely killing the passengers (4 lives)
- Option B: Continue straight, hitting the pedestrians (3 lives)

The system must be programmed to make this split-second decision automatically. What ethical framework should guide the algorithm?""",
                'stakeholders': [
                    'Vehicle occupants (passengers)',
                    'Pedestrians',
                    'Car manufacturer',
                    'Regulators and lawmakers',
                    'Insurance companies',
                    'General public trust in AVs'
                ],
                'questions': [
                    'Should the car minimize total lives lost?',
                    'Should the car prioritize its passengers over others?',
                    'Should age or other factors matter?',
                    'Would your answer change if the pedestrians were children?',
                    'Can the car ever be legally allowed to choose to kill its passengers?'
                ]
            },
            'hiring_bias': {
                'title': 'Algorithmic Hiring Bias',
                'background': """You lead the ML team at a large tech company that uses AI to screen job applications. An internal audit reveals that your algorithm consistently ranks candidates from certain demographic groups lower, even though 'race' and 'gender' are not among the input features.

The algorithm uses: education, work history, skills, resume keywords, and even subtle linguistic patterns. Historical hiring data shows existing biases, which the AI has learned and amplified.

You have 3 options:
1. Deploy as-is, claiming the algorithm isn't 'directly' using protected attributes
2. Apply bias mitigation techniques that may reduce overall accuracy but improve fairness
3. Abandon algorithmic screening entirely and return to human-only review""",
                'stakeholders': [
                    'Job applicants from underrepresented groups',
                    'Employers seeking efficiency',
                    'Employees hired through the system',
                    'Company diversity and inclusion goals',
                    'Society ( perpetuation of systemic bias )'
                ],
                'questions': [
                    'Is statistical parity sufficient? Should outcomes be equal across groups?',
                    'Can we ever fully eliminate bias if training data reflects societal biases?',
                    'Should accuracy ever be sacrificed for fairness? How much?',
                    'Who is responsible for biased outcomes - the developers, the company, or the data?',
                    'Should these systems be audited and regulated?'
                ]
            },
            'facial_recognition': {
                'title': 'Facial Recognition in Public Spaces',
                'background': """As a city council member, you must vote on a proposal to deploy facial recognition cameras throughout downtown to locate wanted criminals and find missing persons.

The system would be monitored by a combination of AI and human officers. Proponents cite:
- 40% reduction in crime in pilot cities
- Rapid recovery of missing children and elderly
- Deterrence effect on potential criminals

Opponents cite:
- Privacy erosion and constant surveillance
- False matches, especially among minorities (higher error rates for darker skin tones)
- Potential for authoritarian misuse if the political climate changes
- Chilling effect on free assembly and speech

The system cannot be opted out of in public spaces.""",
                'stakeholders': [
                    'City residents and visitors',
                    'Local businesses',
                    'Law enforcement',
                    'Civil liberties groups',
                    'Potential crime victims',
                    ' marginalized communities (higher false positive rates)'
                ],
                'questions': [
                    'Does the safety benefit outweigh the privacy cost?',
                    'Should facial recognition be banned in certain contexts (schools, protests, places of worship)?',
                    'What oversight mechanisms would make this acceptable?',
                    'Should citizens be able to opt out or avoid areas with cameras?',
                    'How do we prevent mission creep (starting with serious crimes, expanding to minor offenses)?'
                ]
            },
            'medical_diagnosis': {
                'title': 'AI Medical Diagnosis Trade-offs',
                'background': """You are a product manager at a medical AI startup. Your diagnostic tool analyzes medical images (X-rays, MRIs, pathology slides) and flags potential issues.

Clinical trials show:
- 95% overall accuracy (matching or exceeding experienced radiologists)
- 99% sensitivity for life-threatening conditions (rarely misses cancer)
- However, 5% of recommendations are catastrophically wrong in ways that seem obvious in hindsight
- The 5% error rate disproportionately affects patients with rare conditions or atypical presentations

The hospital wants to deploy immediately, citing the 95% accuracy and the fact that human doctors also make errors. Critics warn that 5% is too high for life-or-death decisions, especially when the AI seems confident in its (wrong) answers.""",
                'stakeholders': [
                    'Patients (those correctly diagnosed and those harmed)',
                    'Doctors and radiologists',
                    'Hospital administration',
                    'Medical device regulators',
                    'Insurance companies',
                    'AI development company'
                ],
                'questions': [
                    'What error rate is acceptable in medical AI? Lower than humans?',
                    'Should AI be used as a second reader only, or can it be primary?',
                    'Who is liable when the AI makes a mistake - the doctor, hospital, or developer?',
                    'Should rare conditions be excluded from the system\'s scope to improve overall accuracy?',
                    'Do patients have a right to know/AI involvement in their diagnosis?'
                ]
            },
            'deepfake_governance': {
                'title': 'Deepfake Detection vs. Free Speech',
                'background': """You are a policy lead at a major social media platform. Deepfake technology has advanced to create highly realistic synthetic videos and audio. Malicious actors use it for:
- Non-consensual pornography
- Political disinformation
- Fraud and impersonation
- Reputation destruction

Your platform is considering an AI-based deepfake detection system that would automatically label or remove synthetic media. But this raises concerns:
- What about legitimate uses (satire, parody, artistic expression, whistleblowing)?
- Could authoritarian governments misuse detection tools to suppress dissent?
- Who decides what counts as 'deepfake' vs 'parody'?',
- Does over-removal chill free expression more than the harms you prevent?""",
                'stakeholders': [
                    'Victims of non-consensual deepfakes',
                    'Political entities targeted by disinformation',
                    'Satirists, artists, and political cartoonists',
                    'Platform users and free speech advocates',
                    'Governments and regulators',
                    'Platform moderation teams'
                ],
                'questions': [
                    'Should platforms police synthetic media at all?',
                    'What makes a deepfake harmful vs acceptable?',
                    'Should detection be AI-based (faster but error-prone) or human-reviewed (slower but nuanced)?',
                    'How do you handle the risk of mislabeling legitimate content?',
                    'What recourse do users have if their content is wrongly removed?'
                ]
            },
            'recommendation_amplification': {
                'title': 'Engagement-Optimized Recommendations',
                'background': """You are an ethics researcher at a major content platform. Internal data shows that algorithms optimizing for user engagement (click-through rate, watch time, likes) consistently promote:
- Content that triggers outrage, fear, or anger
- Conspiracy theories and misinformation
- Extreme political content
- Controversial takes and 'culture war' topics

This content, while engaging, correlates with negative societal outcomes: polarization, anxiety, radicalization, and epistemic breakdown.

Your team proposes redesigning the algorithm to optimize for 'informed citizenship' or 'diverse viewpoints' instead. But tests show a 20% drop in user engagement, which directly impacts revenue. The business side opposes any changes that reduce engagement metrics.""",
                'stakeholders': [
                    'Platform users (information consumption)',
                    'Content creators (attention economy)',
                    'Platform shareholders (revenue)',
                    'Society (public discourse, polarization)',
                    'Advertisers',
                    'People radicalized by algorithm'
                ],
                'questions': [
                    'Should platforms optimize for engagement at all costs?',
                    'What should be the primary optimization goal? User well-being? Platform revenue? Democratic health?',
                    'Can we design algorithms that are both engaging and healthy?',
                    'Should users have more control over their algorithmic feeds?',
                    'Should regulators set constraints on recommendation systems?'
                ]
            }
        }
        
        dilemma = scenarios.get(dilemma_id, scenarios['autonomous_vehicle'])
        
        # Generate a relevant image for the dilemma
        image_prompt = f"Ethical dilemma visualization related to {dilemma['title'].lower()}, abstract concept art, futuristic technology, thought-provoking"
        image_url = generate_image_url(image_prompt, width=1024, height=576)
        
        return {
            "dilemma": dilemma,
            "image_url": image_url
        }
    
    elif action == 'analyze':
        """Analyze a user's decision and provide ethical implications."""
        dilemma_id = data.get('dilemma_id', 'autonomous_vehicle')
        user_decision = data.get('decision', '')
        user_reasoning = data.get('reasoning', '')
        
        analysis_prompt = f"""Analyze the following ethical decision in the context of AI ethics.

Dilemma: {dilemma_id}
User's Decision: {user_decision}
User's Reasoning: {user_reasoning}

Provide a comprehensive analysis that:
1. Identifies which ethical frameworks the user's reasoning aligns with (utilitarian, deontological, virtue ethics, care ethics, etc.)
2. Points out potential consequences (intended and unintended) of their decision
3. Discusses trade-offs and opportunity costs
4. Explores whether this decision could be successfully implemented as an AI system guideline
5. Mentions any assumptions the user made that could be challenged
6. Suggests alternative perspectives or considerations they may have missed

Be respectful, insightful, and educational. Do not judge the decision as right or wrong, but explore its implications thoroughly."""
        
        analysis = call_openrouter(analysis_prompt)
        
        return {
            "analysis": analysis,
            "framework": "Multiple ethical frameworks analyzed"
        }
    
    elif action == 'frameworks':
        """Get information about different ethical frameworks relevant to AI."""
        prompt = """Explain the major ethical frameworks used to analyze AI dilemmas, with practical application examples.

Cover:
- Utilitarianism (greatest good for greatest number) - when it works and fails for AI
- Deontological ethics (rules, duties, rights) - how this applies to AI decision-making
- Virtue ethics (character, moral development) - can AI have virtues? Should we design for human virtues?
- Care ethics (relationships, context, empathy) - appropriate for some AI applications but not others
- Justice and fairness frameworks (distributive justice, procedural justice) - algorithmic fairness definitions
- Principlism (autonomy, beneficence, non-maleficence, justice) - common in bioethics, applicable to AI?
- Rights-based approaches - do people have a right to explanation, to be free from algorithmic decisions?

For each framework:
- Brief philosophical origin
- How it would approach key AI dilemmas (brief examples)
- Strengths and weaknesses in the AI context
- When it's most/least appropriate to apply

Make it practical and accessible to technologists. Around 500-600 words."""
        
        frameworks_text = call_openrouter(prompt)
        
        # Generate an image representing ethical frameworks
        image_prompt = "Abstract visualization of ethical decision-making frameworks, interconnected web of principles, philosophical concept, clean modern design"
        image_url = generate_image_url(image_prompt, width=1024, height=576)
        
        return {
            "frameworks": frameworks_text,
            "image_url": image_url
        }
    
    elif action == 'compare':
        """Compare multiple ethical approaches to the same dilemma."""
        dilemma_id = data.get('dilemma_id', 'autonomous_vehicle')
        
        prompt = f"""For the AI ethics dilemma: {dilemma_id}

Provide a systematic comparison of how different ethical frameworks would approach this dilemma and what decisions they would recommend:

1. Utilitarian/consequentialist approach
2. Deontological/rule-based approach
3. Virtue ethics approach
4. Care ethics approach
5. Fairness and justice approach
6. Rights-based approach

For each approach:
- State the core principle
- Describe how it would analyze this specific dilemma
- What decision or policy would it recommend?
- What are the strengths of this approach in this context?
- What are the weaknesses or potential problems?

Finally, brief commentary on which approach might be most suitable for real-world AI policy (none is perfect) and why a combination/multi-framework approach might be necessary."""
        
        comparison = call_openrouter(prompt)
        
        return {
            "comparison": comparison,
            "dilemma_id": dilemma_id
        }
    
    else:
        return {"error": f"Unknown action: {action}"}


# Metadata for projects.json
META = {
    "name": "AI Ethics Dilemma Simulator",
    "description": "Explore real-world ethical dilemmas in AI systems. Make decisions, analyze consequences, and understand the complex trade-offs in AI ethics including bias, safety, privacy, and accountability.",
    "category": "AI Ethics & Society",
    "tags": ["ethics", "dilemma", "society", "policy", "decision-making", "fairness"],
    "created_at": "2026-02-05"
}
