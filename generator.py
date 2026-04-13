import os
from dotenv import load_dotenv

# Flexible Import Logic
try:
    from mistralai import Mistral
except ImportError:
    # Fallback for older versions of the SDK
    try:
        from mistralai.client import MistralClient as Mistral
    except ImportError:
        Mistral = None

load_dotenv()

def generate_aeo_article(topic, gap_context):
    if Mistral is None:
        return "### Error: Mistral library is installed but incompatible. Please check requirements.txt"

    api_key = os.getenv("MISTRAL_API_KEY")
    # Initialize client inside the function
    client = Mistral(api_key=api_key)
    
    prompt = f"ACT AS: SEO Architect. TOPIC: {topic}. CONTEXT: {gap_context}" # Simplified for brevity
    
    try:
        # Check if we are using the new 'chat.complete' or old 'chat' method
        if hasattr(client, 'chat') and hasattr(client.chat, 'complete'):
            response = client.chat.complete(
                model="mistral-large-latest",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        else:
            # Legacy method
            response = client.chat(
                model="mistral-large-latest",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
    except Exception as e:
        return f"### AI Generation Error: {str(e)}"