"""AI Embeddings Explorer - February 8, 2026

Understand vector embeddings: how they capture meaning, visualize semantic
relationships, and explore applications in search, recommendations, and clustering.
"""

from ..base import call_openrouter, generate_image_url, extract_json
import json


def handle(action: str, data: dict) -> dict:
    """Handle project actions.

    Args:
        action: 'start', 'visualize', 'compare', 'applications', 'interactive'
        data: Request data from frontend

    Returns:
        dict: Response to send to frontend
    """

    if action == 'start':
        """Initialize with introduction to embeddings."""
        prompt = """Explain AI embeddings in clear, practical terms.

        Cover:
        - What embeddings are (dense vector representations of meaning)
        - How they capture semantic relationships (similar words have similar vectors)
        - Why they're better than one-hot encoding
        - Common dimensions (384, 768, 1024, 1536) and what they mean
        - How embeddings are created (training objectives: word2vec, BERT, sentence-transformers)
        - Real-world applications: semantic search, recommendations, clustering, classification
        - Cosine similarity and distance metrics
        - The concept of embedding space as a "meaning map"

        Make it engaging with concrete examples. ~300 words."""

        intro = call_openrouter(prompt)

        # Overview of popular embedding models
        models = [
            {
                "id": "text-embedding-ada-002",
                "name": "OpenAI Ada 002",
                "provider": "OpenAI",
                "dimensions": 1536,
                "context_limit": 8191,
                "description": "Versatile general-purpose embeddings",
                "strengths": "General purpose, widely supported"
            },
            {
                "id": "text-embedding-3-small",
                "name": "OpenAI Embedding 3 Small",
                "provider": "OpenAI",
                "dimensions": 1536,
                "context_limit": 8191,
                "description": "Compact performance",
                "strengths": "Smaller size, good accuracy"
            },
            {
                "id": "text-embedding-3-large",
                "name": "OpenAI Embedding 3 Large",
                "provider": "OpenAI",
                "dimensions": 3072,
                "context_limit": 8191,
                "description": "Maximum accuracy",
                "strengths": "Best quality, larger dimension"
            },
            {
                "id": "all-MiniLM-L6-v2",
                "name": "Sentence Transformers MiniLM",
                "provider": "Sentence Transformers",
                "dimensions": 384,
                "context_limit": 512,
                "description": "Fast and efficient",
                "strengths": "Lightweight, local deployment, fast inference"
            },
            {
                "id": "all-mpnet-base-v2",
                "name": "Sentence Transformers MPNet",
                "provider": "Sentence Transformers",
                "dimensions": 768,
                "context_limit": 384,
                "description": "Balanced performance",
                "strengths": "Better quality, still reasonably fast"
            },
            {
                "id": "multilingual-e5-large",
                "name": "Multilingual E5 Large",
                "provider": "Microsoft",
                "dimensions": 1024,
                "context_limit": 512,
                "description": "100+ languages support",
                "strengths": "Cross-lingual embeddings"
            }
        ]

        return {
            "introduction": intro,
            "models": models
        }

    elif action == 'visualize':
        """Generate visualization of embedding relationships."""
        concept = data.get('concept', 'king - man + woman')

        prompt = f"""Create an educational diagram illustrating how embeddings capture semantic relationships.

        Concept being visualized: "{concept}"

        Show:
        - A 2D/3D projection of an embedding space
        - Points representing words/concepts, positioned by semantic similarity
        - Arrows showing vector arithmetic (like king - man + woman = queen)
        - Color coding: similar concepts grouped together
        - Distance between points representing dissimilarity
        - A title: "Embedding Space: Semantic Similarity Visualization"

        Style: Clean, modern, educational infographic. Use blue/purple gradient colors.
        Make it look like a machine learning research paper figure."""

        image_url = generate_image_url(prompt)

        # Generate explanation
        explanation_prompt = f"""Explain the concept of vector arithmetic in embeddings, using the example: {concept}

        Cover:
        - What vector arithmetic reveals about semantic relationships
        - Why similar concepts cluster together in embedding space
        - How this enables analogical reasoning
        - Limitations and caveats

        ~200 words, educational tone."""

        explanation = call_openrouter(explanation_prompt)

        return {
            "concept": concept,
            "visualization_url": image_url,
            "explanation": explanation
        }

    elif action == 'compare':
        """Compare different embedding models for a use case."""
        use_case = data.get('use_case', 'semantic search')
        requirements = data.get('requirements', {})

        # Extract requirements
        need_speed = requirements.get('speed', 'medium')
        need_accuracy = requirements.get('accuracy', 'high')
        need_multilingual = requirements.get('multilingual', False)
        need_local = requirements.get('local_deployment', False)

        prompt = f"""Analyze the best embedding model for this use case:

        Use Case: {use_case}
        Requirements:
        - Speed: {need_speed}
        - Accuracy: {need_accuracy}
        - Multilingual: {need_multilingual}
        - Local deployment: {need_local}

        Consider these models:
        1. OpenAI Ada 002 (1536 dims, cloud API)
        2. OpenAI Embedding 3 Small (1536 dims, cloud)
        3. OpenAI Embedding 3 Large (3072 dims, cloud)
        4. Sentence Transformers MiniLM (384 dims, local)
        5. Sentence Transformers MPNet (768 dims, local)
        6. Microsoft Multilingual E5 (1024 dims, cloud/local)

        Provide:
        1. Recommended model with reasoning
        2. Trade-offs (speed vs accuracy vs cost vs privacy)
        3. Alternative options
        4. Implementation tips

        ~250 words."""

        analysis = call_openrouter(prompt)

        # Also provide a comparison table
        comparison = {
            "models": [
                {
                    "name": "OpenAI Ada 002",
                    "best_for": "General purpose, cloud apps",
                    "pros": ["High quality", "Easy API", "Large context"],
                    "cons": ["Cost per request", "Privacy concerns", "Cloud-only"],
                    "cost_per_1M_tokens": 0.10,
                    "latency_ms": 150
                },
                {
                    "name": "OpenAI Embedding 3 Small",
                    "best_for": "Cost-effective cloud",
                    "pros": ["Lower cost", "Good quality"],
                    "cons": ["Still cloud-only", "Slightly lower accuracy"],
                    "cost_per_1M_tokens": 0.02,
                    "latency_ms": 100
                },
                {
                    "name": "OpenAI Embedding 3 Large",
                    "best_for": "Maximum quality",
                    "pros": ["Best accuracy", "Large dimensions"],
                    "cons": ["Higher cost", "Cloud-only"],
                    "cost_per_1M_tokens": 0.13,
                    "latency_ms": 200
                },
                {
                    "name": "Sentence Transformers MiniLM",
                    "best_for": "Local/free applications",
                    "pros": ["Completely free", "Privacy", "Fast", "Offline"],
                    "cons": ["Lower quality", "Small context (512)"],
                    "cost_per_1M_tokens": 0,
                    "latency_ms": 20
                },
                {
                    "name": "Sentence Transformers MPNet",
                    "best_for": "Local with good quality",
                    "pros": ["Free", "Better quality than MiniLM", "Offline"],
                    "cons": ["Medium context (384)", "Slower than MiniLM"],
                    "cost_per_1M_tokens": 0,
                    "latency_ms": 40
                },
                {
                    "name": "Microsoft Multilingual E5",
                    "best_for": "100+ languages",
                    "pros": ["Multilingual", "Good quality", "Can run locally"],
                    "cons": ["Larger model size", "More resource needs"],
                    "cost_per_1M_tokens": 0,
                    "latency_ms": 60
                }
            ]
        }

        return {
            "use_case": use_case,
            "analysis": analysis,
            "comparison_table": comparison
        }

    elif action == 'applications':
        """Explore real-world applications of embeddings."""
        application_type = data.get('type', 'all')

        applications = {
            "semantic_search": {
                "name": "Semantic Search",
                "description": "Find documents by meaning, not just keywords.",
                "how_it_works": "Documents and queries are embedded into the same space. Search finds nearest neighbors by cosine similarity.",
                "example_use_cases": [
                    "E-commerce product search",
                    "Document retrieval",
                    "Code search",
                    "Support ticket routing"
                ],
                "trade_offs": "No keyword exact match; needs good embedding model"
            },
            "recommendations": {
                "name": "Recommendation Systems",
                "description": "Suggest items based on content similarity and user behavior.",
                "how_it_works": "Items are embedded; collaborative filtering uses embedding space for user-item interactions.",
                "example_use_cases": [
                    "Movie/music recommendations",
                    "Product recommendations",
                    "Content discovery",
                    "Similar items"
                ],
                "trade_offs": "Cold start for new items; needs diverse training data"
            },
            "clustering": {
                "name": "Clustering & Categorization",
                "description": "Group similar items automatically using vector similarity.",
                "how_it_works": "Apply clustering algorithms (K-means, DBSCAN) in embedding space to discover natural groupings.",
                "example_use_cases": [
                    "Topic modeling",
                    "Customer segmentation",
                    "Content categorization",
                    "Anomaly detection"
                ],
                "trade_offs": "Choosing cluster count; interpreting results"
            },
            "classification": {
                "name": "Text Classification",
                "description": "Classify text into categories using embeddings as features.",
                "how_it_works": "Embed text, then train a classifier (SVM, neural net) on top of embeddings.",
                "example_use_cases": [
                    "Sentiment analysis",
                    "Spam detection",
                    "Content moderation",
                    "Intent classification"
                ],
                "trade_offs": "May not capture task-specific nuances; fine-tuning may be needed"
            },
            "duplicate_detection": {
                "name": "Duplicate Detection",
                "description": "Identify near-duplicate or paraphrased content.",
                "how_it_works": "Compare embeddings; similar vectors indicate duplicate or highly similar content.",
                "example_use_cases": [
                    "Deduplicate documents",
                    "Plagiarism detection",
                    "Support ticket deduplication",
                    "Review spam detection"
                ],
                "trade_offs": "Threshold tuning; may miss semantic duplicates with different embeddings"
            }
        }

        # Generate an applications overview image
        image_prompt = "Infographic showing 5 applications of AI embeddings: semantic search (magnifying glass over documents), recommendations (personalized suggestions), clustering (grouped dots), classification (tagged items), duplicate detection (matching documents). Connected network background. Modern tech style, blue and purple colors."
        image_url = generate_image_url(image_prompt)

        # Filter if specific type requested
        if application_type != 'all' and application_type in applications:
            result_apps = {application_type: applications[application_type]}
        else:
            result_apps = applications

        return {
            "applications": result_apps,
            "overview_image": image_url,
            "total_applications": len(result_apps)
        }

    elif action == 'similarity_calculator':
        """Calculate similarity between two text inputs."""
        text1 = data.get('text1', '')
        text2 = data.get('text2', '')

        if not text1 or not text2:
            return {"error": "Both text1 and text2 are required"}

        # Note: In a real implementation, we would actually compute embeddings
        # and calculate cosine similarity. For this demo, we'll simulate with AI.

        prompt = f"""You are an embedding similarity estimator.

        Estimate the semantic similarity between these two texts on a scale of 0-1 (0 = completely unrelated, 1 = identical meaning):

        Text 1: "{text1}"
        Text 2: "{text2}"

        Factors to consider:
        - Topic similarity
        - Intent alignment
        - Context overlap
        - Semantic equivalence

        Return a JSON object with:
        {{
          "similarity_score": <float between 0 and 1>,
          "reasoning": "<brief explanation>",
          "shared_concepts": ["list", "of", "common", "themes"]
        }}

        Be honest—if they're unrelated, score low. If paraphrasing same idea, score high."""

        result_text = call_openrouter(prompt)
        similarity_result = extract_json(result_text, default={
            "similarity_score": 0.5,
            "reasoning": "Unable to estimate similarity accurately.",
            "shared_concepts": []
        })

        # Generate a visual representation of similarity
        score = similarity_result.get('similarity_score', 0.5)
        visualization_prompt = f"""Create a simple visualization of semantic similarity score: {score:.2f}

        Design: Two overlapping circles (Venn diagram style) with:
        - Left circle: "Text 1"
        - Right circle: "Text 2"
        - Overlap proportion showing similarity percentage
        - Clean, minimal design
        - Color: gradient blue to purple
        - Show similarity score prominently in overlap area"""

        visualization_url = generate_image_url(visualization_prompt)

        return {
            "text1": text1,
            "text2": text2,
            "similarity": similarity_result,
            "visualization_url": visualization_url
        }

    else:
        return {"error": f"Unknown action: {action}"}


# Metadata for projects.json
META = {
    "name": "AI Embeddings Explorer",
    "description": "Dive deep into vector embeddings—the foundation of semantic AI. Understand how embeddings capture meaning, visualize semantic relationships, compare embedding models, and explore applications in search, recommendations, and clustering. Perfect for developers and AI enthusiasts.",
    "category": "AI Education",
    "tags": ["embeddings", "vectors", "semantic-search", "recommendations", "clustering", "ml-basics", "educational"],
    "difficulty": "Intermediate",
    "created_at": "2026-02-08"
}
