from flask import Flask, request, jsonify, render_template, redirect
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
from backend.form_builder import generate_form_schema
from backend.supabase_client import save_form_schema, get_form_schema
import os

load_dotenv()
app = Flask(__name__)

@app.route('/whatsapp', methods=['POST'])
def whatsapp():
    incoming_msg = request.form.get('Body')
    schema = generate_form_schema(incoming_msg)

    resp = MessagingResponse()
    msg = resp.message()

    if schema:
        save_form_schema(schema['form_id'], schema['schema'])
        form_link = f"https://whatsapp-ai-form-generator.onrender.com/form/{schema['form_id']}"
        msg.body(f"✅ Your form is ready: {form_link}")
    else:
        msg.body("❌ Sorry, I couldn't generate your form.")

    return str(resp)

@app.route('/api/form/<form_id>', methods=['GET'])
def get_form(form_id):
    schema = get_form_schema(form_id)
    if schema:
        return jsonify(schema)
    return jsonify({"error": "Form not found"}), 404

@app.route('/form/<form_id>', methods=['GET'])
def form_page(form_id):
    # Redirect to the React frontend to display the form
    return redirect(f"/form/{form_id}")

@app.route('/status', methods=['POST'])
def status():
    print(f"Message SID: {request.form.get('MessageSid')}, Status: {request.form.get('MessageStatus')}")
    return '', 200

if __name__ == '__main__':
    app.run(debug=True)



























