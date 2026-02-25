"""MicroGPT Trainer — Train a tiny GPT in your browser, inspired by Karpathy's microGPT"""

from ..base import call_openrouter, extract_json

def handle(action: str, data: dict) -> dict:
    """Handle project actions. This project is mostly client-side JS,
    but the backend can provide datasets and AI-powered explanations."""
    
    if action == 'info':
        return {"name": META["name"], "description": META["description"]}
    
    if action == 'explain':
        concept = data.get('concept', 'transformer')
        prompt = f"""Explain this neural network concept in 2-3 simple sentences for someone watching a tiny GPT train in their browser: '{concept}'. 
Be specific about what's happening mathematically. Format as JSON: {{"explanation": "...", "analogy": "...", "key_insight": "..."}}"""
        raw = call_openrouter(prompt)
        parsed = extract_json(raw)
        return {"result": parsed or {"text": raw}}
    
    if action == 'dataset':
        name = data.get('name', 'names')
        datasets = {
            "names": "emma olivia ava sophia isabella mia charlotte amelia harper evelyn abigail emily ella elizabeth avery sofia chloe victoria madison luna grace nora riley zoey hannah lily layla lillian natalie hazel aurora penelope stella violet nova ellie ivy ariana cora genesis emilia gianna quinn kaylee anna serenity",
            "shakespeare": "to be or not to be that is the question whether tis nobler in the mind to suffer the slings and arrows of outrageous fortune or to take arms against a sea of troubles and by opposing end them to die to sleep no more and by a sleep to say we end the heartache and the thousand natural shocks that flesh is heir to",
            "code": "def hello name return f hello name def add a b return a plus b def factorial n if n equals 0 return 1 return n times factorial n minus 1 def fibonacci n if n less 2 return n return fibonacci n minus 1 plus fibonacci n minus 2",
            "music": "do re mi fa sol la ti do re mi fa sol la ti do mi sol do mi sol ti re fa la do mi sol ti re fa la ti sol mi do la fa re ti sol mi do",
        }
        text = datasets.get(name, datasets["names"])
        return {"text": text, "name": name}
    
    return {"error": f"Unknown action: {action}"}

META = {
    "name": "MicroGPT Trainer",
    "description": "Train a tiny GPT neural network right in your browser — watch weights update, loss decrease, and generate text in real-time. Inspired by Karpathy's microGPT.",
    "category": "AI Education",
    "date": "2026-02-18"
}
