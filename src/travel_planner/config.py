from dotenv import load_dotenv
import os

def load_api_keys():

    # Retrieve API keys from environment variables
    load_dotenv()

    # Get the Hugging Face API token
    huggingface_api_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
    if not huggingface_api_token:
        raise ValueError("HUGGINGFACE_API_TOKEN is not set in environment variables.")
    
    # Get the OpenWeatherMap API key
    openweathermap_api_key = os.getenv("OPENWEATHERMAP_API_KEY")
    if not openweathermap_api_key:
        raise ValueError("OPENWEATHERMAP_API_KEY is not set in environment variables.")
    
    return huggingface_api_token, openweathermap_api_key

# Load keys at the module level for easy import
HUGGINGFACE_TOKEN, OPENWEATHERMAP_KEY = load_api_keys()
