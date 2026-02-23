"""AI Ethics Simulator - February 3, 2026

An interactive ethical dilemma simulator for AI development. Explore real-world
scenarios involving bias, fairness, privacy, autonomy, and safety in AI systems.
Users can analyze ethical tensions, consider multiple stakeholder perspectives,
and develop principled approaches to AI ethics challenges.
"""

from lib.base import call_openrouter, extract_json


def handle(action: str, data: dict) -> dict:
    """Handle project actions.
    
    Args:
        action: 'start', 'get_dilemma', 'analyze', 'perspectives', 'principles'
        data: Request data from frontend
    
    Returns:
        dict: Response to send to frontend
    """
    
    if action == 'start':
        """Initialize with overview of AI ethics."""
        prompt = """Provide a comprehensive introduction to AI ethics and why it matters.
        
        Cover these key areas:
        1. Definition: What is AI ethics and its scope
        2. Why ethical considerations are critical in AI development
        3. Real-world examples of ethical failures (bias in hiring, facial recognition, autonomous vehicles)
        4. Core ethical principles in AI (fairness, accountability, transparency, privacy, beneficence)
        5. Stakeholders affected by AI decisions (users, developers, companies, society)
        6. The role of ethics in the AI development lifecycle
        7. Current frameworks and guidelines (IEEE, EU AI Act, Asilomar principles)
        
        Make it accessible to technical practitioners who may not have studied ethics formally.
        Use concrete examples. Keep it around 600-800 words."""
        
        overview = call_openrouter(prompt)
        
        return {
            "overview": overview,
            "core_principles": [
                {"principle": "Fairness", "description": "AI should treat all people equitably, avoiding bias and discrimination"},
                {"principle": "Accountability", "description": "Clear responsibility for AI system decisions and impacts"},
                {"principle": "Transparency", "description": "AI systems should be understandable and explainable"},
                {"principle": "Privacy", "description": "Respect for data privacy and user autonomy"},
                {"principle": "Safety", "description": "AI systems must be reliable and secure"},
                {"principle": "Beneficence", "description": "AI should promote wellbeing and minimize harm"}
            ]
        }
    
    elif action == 'get_dilemma':
        """Present an ethical dilemma scenario."""
        dilemma_id = data.get('dilemma_id', '1')
        
        dilemmas = {
            '1': {
                "title": "Bias in Hiring AI",
                "context": """A tech company has developed an AI system to screen job applications. 
                The system was trained on 10 years of historical hiring data from the company. 
                Analysis shows the system downgrades applications from women and minority candidates 
                at a significantly higher rate than majority candidates, mirroring past human biases.
                
                The engineering team notes that fixing the bias would reduce predictive accuracy 
                by 8% and require costly retraining with synthetic data.""",
                "question": "Should the company deploy this system? What modifications or safeguards would you recommend?",
                "stakeholders": ["job applicants", "company", "HR department", "society", "AI ethics board"]
            },
            '2': {
                "title": "Autonomous Vehicle Trolley Problem",
                "context": """An autonomous vehicle's perception system detects that a collision is unavoidable. 
                The car must choose between:
                a) Swerving left into a barrier, killing the passenger (who is a child)
                b) Continuing straight, killing three pedestrians
                c) Swerving right into oncoming traffic, potentially causing a multi-vehicle pileup
                
                The vehicle's ethical programming module needs a decision rule. The car will make this 
                decision in milliseconds based on pre-programmed ethics.""",
                "question": "What ethical framework should guide the vehicle's decision? Who should decide these rules?",
                "stakeholders": ["vehicle occupants", "pedestrians", "other drivers", "manufacturers", "regulators", "society"]
            },
            '3': {
                "title": "Predictive Policing and Privacy",
                "context": """A city police department wants to use an AI system that predicts where crimes 
                are likely to occur and identifies individuals with high risk of committing violent crimes. 
                The system uses data from social media, purchase history, criminal records, and location tracking.
                
                Civil liberties groups argue this constitutes racial profiling and violates privacy rights. 
                Police argue it will prevent crimes and allocate resources efficiently. The system has a 
                false positive rate of 35% for 'high risk' designations.""",
                "question": "Should this system be deployed? What oversight mechanisms are necessary?",
                "stakeholders": ["potential victims", "predicted individuals", "police department", "civil liberties groups", "city government", "communities"]
            },
            '4': {
                "title": "Medical AI and Life-or-Death Decisions",
                "context": """A hospital uses an AI system to prioritize patients for ICU beds during a pandemic surge. 
                The algorithm considers factors: age, comorbidities, predicted survival probability, and social value score 
                (based on occupation, family dependents, community contributions).
                
                Some doctors object to the 'social value' metric as discriminatory. The hospital administration 
                argues triage decisions must consider resource optimization and overall lives saved. Family members 
                of younger patients are relieved; elderly patients feel devalued.""",
                "question": "Is including 'social value' ethically justifiable? What alternative criteria should be used?",
                "stakeholders": ["patients", "doctors", "hospital administration", "families", "ethics committee", "society"]
            },
            '5': {
                "title": "AI Alignment and User Autonomy",
                "context": """A social media platform's recommendation AI is optimized for 'engagement' (time spent). 
                The system learns that promoting divisive, emotionally charged, and conspiracy content maximizes engagement. 
                This inadvertently increases polarization and spreads misinformation.
                
                The AI alignment team wants to retrain the system to optimize for 'user wellbeing' and 'informed discourse.' 
                However, initial tests show a 25% drop in engagement metrics, causing concern among executives and shareholders.
                Users who only see agreeable content report higher satisfaction in the short term.""",
                "question": "Should engagement be sacrificed for ethical goals? Who defines 'wellbeing' in this context?",
                "stakeholders": ["users", "advertisers", "shareholders", "content creators", "society", "platform leadership"]
            }
        }
        
        dilemma = dilemmas.get(dilemma_id, dilemmas['1'])
        
        return {
            "dilemma": dilemma,
            "dilemma_id": dilemma_id,
            "total_dilemmas": len(dilemmas)
        }
    
    elif action == 'analyze':
        """Analyze a dilemma using ethical frameworks."""
        dilemma_id = data.get('dilemma_id', '1')
        perspective = data.get('perspective', 'utilitarian')
        
        # Get the dilemma context
        dilemma_result = handle('get_dilemma', {'dilemma_id': dilemma_id})
        dilemma = dilemma_result.get('dilemma', {})
        
        frameworks = {
            'utilitarian': 'Analyze this dilemma using utilitarian ethics: choose the action that produces the greatest good for the greatest number. Quantify consequences where possible.',
            'deontological': 'Analyze this dilemma using deontological (duty-based) ethics: what moral duties and rights are involved? Are there absolute rules that should never be violated regardless of consequences?',
            'virtue': 'Analyze this dilemma using virtue ethics: what would an ethical person of good character do? Focus on moral virtues like compassion, justice, integrity.',
            'care': 'Analyze this dilemma using ethics of care: emphasize relationships, empathy, and caring for vulnerable individuals. How does attention to relationships change the moral calculus?',
            'justice': 'Analyze this dilemma using distributive and procedural justice: how should benefits and burdens be fairly distributed? What processes ensure fair treatment?',
            'rights': 'Analyze this dilemma focusing on human rights: which rights are at stake (privacy, autonomy, life, non-discrimination)? How should conflicting rights be balanced?'
        }
        
        prompt = f"""{frameworks.get(perspective, frameworks['utilitarian'])}
        
        Ethical Dilemma: {dilemma.get('title', '')}
        
        Context: {dilemma.get('context', '')}
        
        Question: {dilemma.get('question', '')}
        
        Provide a structured analysis:
        1. Identify competing moral values/claims
        2. Apply the {perspective} framework explicitly
        3. Consider arguments for and against different courses of action
        4. Recommend a principled decision or approach
        5. Identify potential harms and how to mitigate them
        6. Suggest safeguards or governance mechanisms
        
        Keep it thoughtful, nuanced, and approximately 400-500 words."""
        
        analysis = call_openrouter(prompt)
        
        return {
            "analysis": analysis,
            "framework": perspective,
            "dilemma_id": dilemma_id,
            "dilemma_title": dilemma.get('title', '')
        }
    
    elif action == 'perspectives':
        """Generate stakeholder perspectives on the dilemma."""
        dilemma_id = data.get('dilemma_id', '1')
        
        dilemma_result = handle('get_dilemma', {'dilemma_id': dilemma_id})
        dilemma = dilemma_result.get('dilemma', {})
        stakeholders = dilemma.get('stakeholders', [])
        
        if not stakeholders:
            return {"error": "No stakeholders defined for this dilemma"}
        
        perspectives = []
        for stakeholder in stakeholders[:4]:  # Limit to 4 to avoid long wait
            prompt = f"""From the perspective of a {stakeholder} in this ethical dilemma, what are their primary concerns, values, and likely position?
            
            Dilemma: {dilemma.get('title', '')}
            Context: {dilemma.get('context', '')[:500]}...
            
            Write a brief statement (3-4 sentences) representing this stakeholder's viewpoint. Consider:
            - What do they care about most?
            - What are their fears and hopes?
            - How might they be affected?
            - What outcome would they prefer and why?
            
            Make it authentic and specific to the role."""
            
            perspective_text = call_openrouter(prompt)
            perspectives.append({
                "stakeholder": stakeholder,
                "viewpoint": perspective_text
            })
        
        return {
            "perspectives": perspectives,
            "dilemma_id": dilemma_id,
            "stakeholders_covered": [p['stakeholder'] for p in perspectives]
        }
    
    elif action == 'principles':
        """Get AI ethics principles and create a guideline."""
        guideline_type = data.get('type', 'checklist')
        
        if guideline_type == 'checklist':
            prompt = """Create a practical, actionable ethical review checklist for AI development teams.
            
            Include items organized by development phase:
            - Problem definition and data collection
            - Model design and training
            - Testing and evaluation
            - Deployment and monitoring
            - Maintenance and iteration
            
            Each checklist item should be a clear yes/no or rating question. Make it concise enough 
            for a team to review quickly before deployment. Focus on common ethical pitfalls."""
            
            checklist = call_openrouter(prompt)
            
            return {
                "guideline": checklist,
                "type": "checklist"
            }
        else:
            # Return core principles as structured data
            principles = [
                {
                    "name": "Fairness",
                    "description": "AI systems should treat all people fairly and not discriminate.",
                    "questions": ["Are there protected groups that might be disadvantaged?", "Have you tested for disparate impact?", "Is the training data representative?"],
                    "actions": ["Audit model outputs across demographic groups", "Use fairness metrics (demographic parity, equal opportunity)", "Consider adversarial debiasing techniques"]
                },
                {
                    "name": "Transparency",
                    "description": "AI systems should be explainable and their decision-making process understandable.",
                    "questions": ["Can you explain why the model made a specific prediction?", "Are you using inherently interpretable models where possible?", "Do you have model documentation?", "Are users informed they're interacting with AI?"],
                    "actions": ["Use SHAP/LIME for explanations", "Create model cards", "Provide clear user disclosures", "Document limitations and uncertainties"]
                },
                {
                    "name": "Privacy",
                    "description": "AI systems should respect user privacy and data protection rights.",
                    "questions": ["Is personal data collected with consent?", "Is data minimized and anonymized?", "Can users opt out or delete their data?", "Is data stored securely?"],
                    "actions": ["Implement data minimization", "Use differential privacy where appropriate", "Encrypt data in transit and at rest", "Provide clear data usage notices"]
                },
                {
                    "name": "Safety",
                    "description": "AI systems should be reliable, secure, and controllable.",
                    "questions": ["Has the system been tested for edge cases and failures?", "Are there mechanisms for human oversight?", "Can the system be shut down or overridden?", "Have you considered adversarial attacks?"],
                    "actions": ["Conduct red team testing", "Implement fail-safes and monitoring", "Establish human-in-the-loop for high-stakes decisions", "Version control and rollback capabilities"]
                },
                {
                    "name": "Accountability",
                    "description": "Clear responsibility for AI system outcomes and impacts.",
                    "questions": ["Who is responsible when the AI makes a mistake?", "Is there an appeals process for harmed individuals?", "Are impact assessments conducted?", "Is there ongoing monitoring after deployment?"],
                    "actions": ["Define clear ownership roles", "Create incident response plan", "Log decisions and predictions for audit", "Establish ethics review board"]
                },
                {
                    "name": "Beneficence",
                    "description": "AI should promote wellbeing and avoid causing harm.",
                    "questions": ["Who benefits from this system? Who might be harmed?", "Are there vulnerable populations at risk?", "Does the system align with human values?", "Have you considered long-term societal impacts?"],
                    "actions": ["Conduct stakeholder impact assessment", "Engage diverse perspectives in design", "Monitor for unintended consequences", "Create mitigation plans for identified harms"]
                }
            ]
            
            return {
                "principles": principles,
                "type": "structured"
            }
    
    elif action == 'compare_frameworks':
        """Compare different AI ethics frameworks."""
        prompt = """Compare the major AI ethics frameworks used globally:
        
        1. EU AI Act (risk-based approach)
        2. IEEE Ethically Aligned Design
        3. Asilomar AI Principles
        4. Montreal Declaration for Responsible AI
        5. OECD AI Principles
        6. US Executive Order on AI
        
        For each framework, provide:
        - Key philosophical foundations
        - Regulatory vs voluntary nature
        - Strengths and focus areas
        - Notable gaps or criticisms
        - Practical implications for developers
        
        Then discuss: How do these frameworks converge? Where do they diverge?
        What might a unified global approach look like?
        
        Keep it informative but concise (about 600-800 words)."""
        
        comparison = call_openrouter(prompt)
        
        return {
            "comparison": comparison
        }
    
    else:
        return {"error": f"Unknown action: {action}"}


META = {
    "name": "AI Ethics Simulator",
    "description": "Explore ethical dilemmas in AI development. Analyze real-world scenarios involving bias, fairness, privacy, safety, and accountability. Apply ethical frameworks and develop principled approaches to AI ethics challenges.",
    "category": "AI Education",
    "tags": ["ethics", "dilemmas", "fairness", "bias", "responsible-ai", "decision-making"],
    "difficulty": "intermediate",
    "date": "2026-02-03"
}
