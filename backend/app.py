from flask import Flask, request, jsonify, render_template, redirect
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
from backend.form_builder import generate_form_schema
from backend.supabase_client import save_form_schema, get_form_schema
import os

load_dotenv()
app = Flask(__name__)

def save_form_as_html(form_id, schema):
    try:
        forms_dir = os.path.join(os.getcwd(), 'forms')
        os.makedirs(forms_dir, exist_ok=True)  # Ensure the forms/ directory exists

        form_path = os.path.join(forms_dir, f"{form_id}.html")
        with open(form_path, 'w') as form_file:
            form_file.write(f"<html><head><title>{schema.get('title', 'Form')}</title></head><body>")
            form_file.write(f"<h1>{schema.get('title', 'Form')}</h1>")
            form_file.write(f"<p>{schema.get('description', '')}</p>")
            form_file.write("<form>")

            for field_name, field_props in schema.get('properties', {}).items():
                form_file.write(f"<label>{field_props.get('title', field_name)}</label><br>")
                input_type = 'text' if field_props.get('type') == 'string' else field_props.get('type', 'text')
                form_file.write(f"<input type='{input_type}' name='{field_name}'><br><br>")

            form_file.write("<button type='submit'>Submit</button>")
            form_file.write("</form></body></html>")

        print(f"✅ Form saved as HTML: {form_path}")
    except Exception as e:
        print(f"❌ Error saving form as HTML: {e}")

@app.route('/whatsapp', methods=['POST'])
def whatsapp():
    incoming_msg = request.form.get('Body')
    print(f"🔍 Incoming message: {incoming_msg}")  # Log the incoming message

    schema = generate_form_schema(incoming_msg)
    print(f"🔍 Generated schema: {schema}")  # Log the generated schema

    resp = MessagingResponse()
    msg = resp.message()

    if schema:
        try:
            save_form_schema(schema['form_id'], schema['schema'])
            save_form_as_html(schema['form_id'], schema['schema'])  # Save the form as an HTML file
            print(f"✅ Form {schema['form_id']} saved successfully.")  # Log successful save
            form_link = f"https://whatsapp-ai-form-generator.onrender.com/form/{schema['form_id']}"
            msg.body(f"✅ Your form is ready: {form_link}")
        except Exception as e:
            print(f"❌ Error saving form: {e}")  # Log any save errors
            msg.body("❌ Sorry, there was an error saving your form.")
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
    frontend_base_url = "https://whatsapp-ai-form-generator-frontend.onrender.com"
    return redirect(f"{frontend_base_url}/form/{form_id}")

@app.route('/status', methods=['POST'])
def status():
    print(f"Message SID: {request.form.get('MessageSid')}, Status: {request.form.get('MessageStatus')}")
    return '', 200

if __name__ == '__main__':
    app.run(debug=True)



























