import openai
import uuid
import os
from dotenv import load_dotenv

# Load environment variables (this is important!)
load_dotenv()

# Initialize OpenAI client
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_form_schema(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are an assistant that generates JSON form schemas."},
                {"role": "user", "content": f"Create a JSON form schema for: {prompt}"}
            ],
            max_tokens=1000,
            temperature=0.5
        )
        content = response.choices[0].message.content
        form_id = str(uuid.uuid4())[:8]
        return {
            "form_id": form_id,
            "schema": content
        }
    except Exception as e:
        print("❌ Error generating form schema:", e)
        return None
