import os
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv("OPENAI_API_KEY")
print("API Key found:", bool(api_key))

# Set API key
openai.api_key = api_key

# Test API
try:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hello"}]
    )
    print("API test successful!")
    print("Response:", response)
except Exception as e:
    print("Error:", str(e)) 