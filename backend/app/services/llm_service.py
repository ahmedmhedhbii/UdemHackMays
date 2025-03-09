import logging
from google import genai
from app.core.config import settings

logger = logging.getLogger(__name__)

# Initialise le client avec la clé d'API
gemini_client = genai.Client(api_key=settings.LLM_API_KEY)

def generate_content(prompt: str) -> str:
    """
    Utilise l'API Gemini pour générer du contenu à partir d'un prompt.
    """
    try:
        response = gemini_client.models.generate_content(
            model=settings.LLM_MODEL_NAME,
            contents=prompt
        )
        return response.text
    except Exception as e:
        logger.error(f"Error generating content with Gemini: {e}")
        raise e
