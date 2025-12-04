import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
print(f"API Key found: {api_key[:5]}...{api_key[-5:] if api_key else 'None'}")

if not api_key:
    print("Error: No API key found in .env")
    exit(1)

genai.configure(api_key=api_key)

try:
    print("Listing available models...")
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(m.name)
            
    model = genai.GenerativeModel('gemini-flash-latest')
    response = model.generate_content("Hello, can you hear me?")
    print("Success! Response:")
    print(response.text)
except Exception as e:
    print(f"Error: {e}")
