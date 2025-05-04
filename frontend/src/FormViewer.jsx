// frontend/src/FormViewer.jsx
import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { fetchFormSchema } from './api';

export default function FormViewer() {
  const { id } = useParams();
  const [form, setForm] = useState(null);

  useEffect(() => {
    fetchFormSchema(id).then((data) => {
      if (data) {
        const fields = Object.entries(data.properties || {}).map(([name, props]) => ({
          name,
          label: props.title || name,
          type: props.type === 'string' ? 'text' : props.type,
        }));
        setForm({ title: data.title, description: data.description, fields });
      }
    });
  }, [id]);

  if (!form) return <p>Loading form...</p>;

  return (
    <div className="p-8 max-w-xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">{form.title || "Form"}</h1>
      <p className="mb-4">{form.description}</p>
      <form>
        {form.fields.map((field, idx) => (
          <div key={idx} className="mb-4">
            <label className="block mb-1">{field.label}</label>
            <input
              type={field.type}
              name={field.name}
              className="w-full border p-2 rounded"
            />
          </div>
        ))}
        <button type="submit" className="bg-blue-500 text-white px-4 py-2 rounded">
          Submit
        </button>
      </form>
    </div>
  );
}
