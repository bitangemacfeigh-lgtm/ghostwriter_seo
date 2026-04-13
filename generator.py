import os
from mistralai import Mistral
from dotenv import load_dotenv

# 1. Load Environment Variables
load_dotenv()

def get_mistral_client():
    """
    Safely retrieves the API key and initializes the Mistral client.
    Using a function ensures we don't crash on import if the key is missing.
    """
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        # On Render, this will help you debug if the Env Var was set correctly
        raise ValueError("CRITICAL: MISTRAL_API_KEY is missing from environment variables.")
    return Mistral(api_key=api_key)

def generate_aeo_article(topic, gap_context):
    """
    Generates a 'Content Hijack' article designed to outrank the competitor context.
    """
    print(f"\n[AI ARCHITECT] Executing Hijack Strategy: {topic}")
    
    # Initialize client inside the function to avoid global scope import errors
    try:
        client = get_mistral_client()
    except Exception as e:
        return f"### Configuration Error\n{str(e)}"
    
    prompt = f"""
    ACT AS: A Lead SEO Content Architect.
    GOAL: Create a 'Content Hijack' article for the topic '{topic}'.
    
    COMPETITOR CONTEXT (WHAT THEY WROTE): 
    {gap_context}

    STRATEGY & REQUIREMENTS:
    1. INFORMATION GAIN: Identify exactly what the competitor missed. Write a 2,000-word masterpiece that is 10x more valuable.
    2. DIRECT ANSWER: Start with a 50-word summary optimized for Google SGE and AI snippets.
    3. SEMANTIC TRIPLES: Structure core facts as (Subject-Predicate-Object) to help LLMs index your authority.
    4. ENTITY DENSITY: Maintain a 3-5% density of industry-specific entities.
    5. WHY THIS OUTRANKS THEM: Include a brief 'Competitive Edge' section at the top (formatted as a callout).
    6. TECHNICAL SEO: End with a valid JSON-LD FAQ Schema block.

    STYLE: Authoritative, data-driven, and exhaustive. Use Markdown formatting.
    
    INSTRUCTIONS:
    If the Competitor Data is weak or contains errors, assume a total market gap and write the definitive guide for 2026.
    """
    
    try:
        chat_response = client.chat.complete(
            model="mistral-large-latest",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7 
        )
        
        content = chat_response.choices[0].message.content
        return content

    except Exception as e:
        return f"### Error in AI Generation\n{str(e)}"