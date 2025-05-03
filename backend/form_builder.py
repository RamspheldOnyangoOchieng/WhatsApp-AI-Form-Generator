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

        # Remove comments and sanitize invalid control characters
        raw_text = re.sub(r'//.*', '', raw_text)  # Remove comments
        raw_text = raw_text.replace('\n', '').replace('\r', '').replace('\t', '')  # Remove control characters

        json_start = raw_text.find('{')
        json_end = raw_text.rfind('}') + 1
        if json_start == -1 or json_end == 0:
            raise ValueError("No valid JSON object found in the response")
        schema = json.loads(raw_text[json_start:json_end])
        return {"form_id": str(uuid.uuid4())[:8], "schema": schema}
    except json.JSONDecodeError as e:
        print("❌ JSON Decode Error:", e)
    except Exception as e:
        print("❌ Gemini Error:", e)
    return None
