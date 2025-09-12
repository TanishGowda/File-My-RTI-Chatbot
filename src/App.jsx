// src/App.jsx
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';

import ChatPage from './pages/ChatPage';
import AuthPage from './pages/AuthPage';
import SignupPage from './pages/SignupPage'; // ✅ Import the signup page
import FileRTIPage from './pages/FileRTIPage';
import TermsPage from './pages/TermsPage';
import PrivacyPage from './pages/PrivacyPage';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Navigate to="/auth" replace />} />
        <Route path="/auth" element={<AuthPage />} />
        <Route path="/signup" element={<SignupPage />} /> {/* ✅ Signup route */}
        <Route path="/chat" element={<ChatPage />} />
        <Route path="/file-rti" element={<FileRTIPage />} />
        <Route path="/terms" element={<TermsPage />} />
        <Route path="/privacy" element={<PrivacyPage />} />
      </Routes>
    </Router>
  );
}

export default App;
