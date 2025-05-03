import os, json, uuid
import re
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("models/gemini-1.5-flash-latest")

def generate_form_schema(prompt):
    try:
        response = model.generate_content(f"Create a JSON form schema with fields and types for: {prompt}")
        raw_text = response.text.strip()
        print("🔍 Gemini raw response:", raw_text)  # Log the raw response for debugging

        # Clean and validate the JSON response
        raw_text = re.sub(r'//.*', '', raw_text)  # Remove comments
        raw_text = raw_text.replace('\n', '').replace('\r', '').replace('\t', '')  # Remove control characters
        raw_text = raw_text.replace("'", '"')  # Replace single quotes with double quotes
        raw_text = re.sub(r'\s+', ' ', raw_text)  # Normalize whitespace

        json_start = raw_text.find('{')
        json_end = raw_text.rfind('}') + 1
        if json_start == -1 or json_end == 0:
            raise ValueError("No valid JSON object found in the response")

        cleaned_json = raw_text[json_start:json_end]
        print("🔍 Cleaned JSON:", cleaned_json)  # Log the cleaned JSON

        schema = json.loads(cleaned_json)
        return {"form_id": str(uuid.uuid4())[:8], "schema": schema}
    except json.JSONDecodeError as e:
        print("❌ JSON Decode Error:", e)
    except Exception as e:
        print("❌ Gemini Error:", e)
    return None
