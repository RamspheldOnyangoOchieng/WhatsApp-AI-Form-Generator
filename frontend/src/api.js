export async function fetchFormSchema(id) {
  try {
    const res = await fetch(`https://yourdomain.com/api/form/${id}`);
    if (!res.ok) throw new Error("Failed to fetch form");
    return await res.json();
  } catch (err) {
    console.error("❌ Error fetching form schema:", err);
    return null;
  }
}
