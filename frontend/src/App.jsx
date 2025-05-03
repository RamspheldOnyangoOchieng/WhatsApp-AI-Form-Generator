import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { fetchFormSchema } from './api';

export default function App() {
  const { id } = useParams();
  const [form, setForm] = useState(null);

  useEffect(() => {
    fetchFormSchema(id).then(setForm);
  }, [id]);

  return (
    <div className="p-8 max-w-xl mx-auto">
      <h1 className="text-2xl font-bold">{form?.title || "Form"}</h1>
      <form>
        {form?.fields.map((field, idx) => (
          <div key={idx} className="mb-4">
            <label>{field.label}</label>
            <input type={field.type} className="w-full border p-2 rounded" />
          </div>
        ))}
        <button className="bg-blue-500 text-white px-4 py-2 rounded">Submit</button>
      </form>
    </div>
  );
}
// Compare this snippet from frontend/src/api.js: