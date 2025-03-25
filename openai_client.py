import openai
import os
from config import load_env_variables

# Load environment variables
load_env_variables()

def get_openai_client():
    """Initialize and return OpenAI client."""
    return openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))