import os
from dotenv import load_dotenv
import mistralai # Import the base module only

load_dotenv()

def generate_aeo_article(topic, gap_context):
    api_key = os.getenv("MISTRAL_API_KEY")
    
    # We manually find the client regardless of what it's named
    try:
        # Check for the modern SDK 'Mistral'
        if hasattr(mistralai, "Mistral"):
            client = mistralai.Mistral(api_key=api_key)
        # Check for the older SDK 'MistralClient'
        elif hasattr(mistralai, "client") and hasattr(mistralai.client, "MistralClient"):
            client = mistralai.client.MistralClient(api_key=api_key)
        else:
            return "### Error: Mistral SDK version is incompatible with this environment."
            
    except Exception as e:
        return f"### SDK Initialization Error: {str(e)}"

    prompt = f"ACT AS: SEO Architect. TOPIC: {topic}. CONTEXT: {gap_context}"

    try:
        # This calls the chat completion in a way that works for almost all versions
        if hasattr(client, 'chat') and hasattr(client.chat, 'complete'):
            response = client.chat.complete(
                model="mistral-large-latest",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        else:
            # Fallback for older versions
            response = client.chat(
                model="mistral-large-latest",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
    except Exception as e:
        return f"### AI Generation Error: {str(e)}"