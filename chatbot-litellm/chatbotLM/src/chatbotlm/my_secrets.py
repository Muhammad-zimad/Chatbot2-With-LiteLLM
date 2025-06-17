from dotenv import load_dotenv
import os

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
gemini_model = os.getenv("GEMINI_API_MODEL")

if not gemini_api_key or not gemini_model:
    print("Please set the environment variables api_key, base_url, and model.")
    exit(1)

class Secrets:  
    def __init__(self):
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        self.gemini_model = os.getenv("GEMINI_API_MODEL") 