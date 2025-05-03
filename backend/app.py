from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
import os
import openai

# Load environment variables
load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')

print(f"🧪 Loaded API Key: {os.getenv('OPENAI_API_KEY')}")

# Local import after loading env to ensure access to API key
from backend.form_builder import generate_form_schema

app = Flask(__name__)

@app.route('/whatsapp', methods=['POST'])
def whatsapp():
    incoming_msg = request.form.get('Body')
    schema = generate_form_schema(incoming_msg)

    resp = MessagingResponse()
    msg = resp.message()

    if schema:
        form_link = f"https://yourdomain.com/form/{schema['form_id']}"
        msg.body(f"✅ Your form is ready: {form_link}")
    else:
        msg.body("❌ Sorry, I couldn't generate your form right now. Please try again later.")

    return str(resp)

@app.route('/status', methods=['POST'])
def status():
    message_status = request.form.get('MessageStatus')
    message_sid = request.form.get('MessageSid')
    print(f"Message SID: {message_sid}, Status: {message_status}")
    return '', 200

if __name__ == '__main__':

    print(f"✅ Using OpenAI API Key: {os.getenv('OPENAI_API_KEY')[:8]}...")  # Show only first chars for safety
    app.run(debug=True)
