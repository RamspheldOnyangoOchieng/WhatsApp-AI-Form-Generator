import uuid
import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

#for model in genai.list_models():
#    print(f"Model: {model.name}")
 #   for method in model.supported_generation_methods:
  #      print(f"- Supports: {method}")
# Load the model
model = genai.GenerativeModel("models/gemini-1.5-flash-latest")


def generate_form_schema(prompt):
    try:
        response = model.generate_content(f"Create a JSON form schema for: {prompt}")
        raw_text = response.text.strip()
        json_start = raw_text.find('{')
        json_str = raw_text[json_start:]

        schema = json.loads(json_str)
        form_id = str(uuid.uuid4())[:8]

        # Save schema to a file or DB (simple file approach shown here)
        with open(f"forms/{form_id}.json", "w") as f:
            json.dump(schema, f)

        return {
            "form_id": form_id,
            "schema": schema
        }
    except Exception as e:
        print("❌ Error generating form schema:", e)
        return None
