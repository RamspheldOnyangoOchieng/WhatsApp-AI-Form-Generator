// frontend/src/App.jsx
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import FormViewer from './FormViewer';

export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/form/:id" element={<FormViewer />} />
      </Routes>
    </Router>
  );
}
