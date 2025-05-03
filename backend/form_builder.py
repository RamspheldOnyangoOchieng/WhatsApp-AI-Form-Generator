import os, json, uuid
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
        json_start = raw_text.find('{')
        if json_start == -1:
            raise ValueError("No JSON object found in the response")
        schema = json.loads(raw_text[json_start:])
        return {"form_id": str(uuid.uuid4())[:8], "schema": schema}
    except json.JSONDecodeError as e:
        print("❌ JSON Decode Error:", e)
    except Exception as e:
        print("❌ Gemini Error:", e)
    return None
