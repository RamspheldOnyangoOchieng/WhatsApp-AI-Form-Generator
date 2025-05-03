import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

def save_form_schema(form_id, schema):
    try:
        supabase.table("forms").insert({"form_id": form_id, "schema": schema}).execute()
        print(f"✅ Form {form_id} saved.")
    except Exception as e:
        print("❌ Error saving to Supabase:", e)

def get_form_schema(form_id):
    try:
        result = supabase.table("forms").select("*").eq("form_id", form_id).execute()
        if result.data:
            return result.data[0]['schema']
    except Exception as e:
        print("❌ Error fetching from Supabase:", e)
    return None
