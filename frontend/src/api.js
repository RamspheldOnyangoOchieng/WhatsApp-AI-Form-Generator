export async function fetchFormSchema(id) {
  try {
    const res = await fetch(`https://whatsapp-ai-form-generator.onrender.com/api/form/${id}`);
    if (!res.ok) throw new Error("Form fetch failed");
    return await res.json();
  } catch (e) {
    console.error("❌ Error:", e);
    return null;
  }
}
