import openai
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def upload_file(file_path, purpose="assistants"):
    """Uploads a file to OpenAI and returns the file ID."""
    with open(file_path, "rb") as file:
        response = client.files.create(file=file, purpose=purpose)
    return response.id

# Upload the CSV file and get its file ID
file_path = "Filtered_leads.csv"
file_id = upload_file(file_path)

print(f"File uploaded successfully. File ID: {file_id}")