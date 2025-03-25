import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_openai_client():
    """Initialize and return OpenAI client."""
    return openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))