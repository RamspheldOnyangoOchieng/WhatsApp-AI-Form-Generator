from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
import os
from flask import render_template, send_from_directory
import json
from flask_cors import CORS


# Load environment variables
load_dotenv()

print(f"🧪 Loaded GEMINI API Key: {os.getenv('GEMINI_API_KEY')[:8]}...")

# Local import after loading env to ensure access to API key
from backend.form_builder import generate_form_schema

app = Flask(__name__)
CORS(app)


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

@app.route('/api/form/<form_id>', methods=['GET'])
def get_form_schema(form_id):
    try:
        with open(f"forms/{form_id}.json", "r") as f:
            schema = json.load(f)
        return schema, 200
    except FileNotFoundError:
        return {"error": "Form not found"}, 404


@app.route('/status', methods=['POST'])
def status():
    message_status = request.form.get('MessageStatus')
    message_sid = request.form.get('MessageSid')
    print(f"Message SID: {message_sid}, Status: {message_status}")
    return '', 200

if __name__ == '__main__':
    app.run(debug=True)
