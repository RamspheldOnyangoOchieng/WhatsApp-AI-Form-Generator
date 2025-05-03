import uuid
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

for model in genai.list_models():
    print(f"Model: {model.name}")
    for method in model.supported_generation_methods:
        print(f"- Supports: {method}")
# Load the model
model = genai.GenerativeModel("gemini-pro")

def generate_form_schema(prompt):
    try:
        response = model.generate_content(f"Create a JSON form schema for: {prompt}")
        content = response.text
        form_id = str(uuid.uuid4())[:8]
        return {
            "form_id": form_id,
            "schema": content
        }
    except Exception as e:
        print("❌ Error generating form schema:", e)
        return None
