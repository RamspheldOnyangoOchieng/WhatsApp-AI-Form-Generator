import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { Route, BrowserRouter as Router, Routes } from 'react-router-dom';
import FormViewer from './FormViewer';
import './index.css';

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <Router>
      <Routes>
        <Route path="/form/:id" element={<FormViewer />} />
      </Routes>
    </Router>
  </StrictMode>,
)
