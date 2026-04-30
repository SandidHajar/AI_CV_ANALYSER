import React, { useState } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Home from './pages/Home';
import Dashboard from './pages/Dashboard';
import Login from './pages/Login';
import Landing from './pages/Landing';
import Navbar from './components/Navbar';

// Simple Protected Route wrapper
const ProtectedRoute = ({ children }) => {
  const token = localStorage.getItem('token');
  if (!token) {
    return <Navigate to="/login" replace />;
  }
  return children;
};

function App() {
  const [analysisResult, setAnalysisResult] = useState(null);

  return (
    <BrowserRouter>
      <div className="min-h-screen bg-[#0a0f1c] text-white flex flex-col font-sans">
        <Navbar />
        
        <main className="flex-1 max-w-6xl w-full mx-auto p-4 md:p-8">
          <Routes>
            <Route path="/" element={<Landing />} />
            <Route path="/login" element={<Login />} />
            <Route path="/app" element={
              <ProtectedRoute>
                <Home setAnalysisResult={setAnalysisResult} />
              </ProtectedRoute>
            } />
            <Route path="/dashboard" element={
              <ProtectedRoute>
                <Dashboard result={analysisResult} />
              </ProtectedRoute>
            } />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;


