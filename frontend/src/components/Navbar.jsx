import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { BrainCircuit, LogIn, LogOut, LayoutDashboard } from 'lucide-react';

const Navbar = () => {
  const navigate = useNavigate();
  const token = localStorage.getItem('token');

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/');
  };

  return (
    <nav className="w-full py-4 px-6 border-b border-slate-800 bg-slate-900/50 backdrop-blur-md sticky top-0 z-50">
      <div className="max-w-6xl mx-auto flex items-center justify-between">
        <Link to="/" className="flex items-center gap-2 group">
          <BrainCircuit className="text-blue-500 group-hover:text-blue-400 transition-colors" size={28} />
          <span className="text-xl font-bold bg-gradient-to-r from-blue-400 to-indigo-500 bg-clip-text text-transparent">
            ResumeAI
          </span>
        </Link>
        
        <div className="flex items-center gap-4">
          {token ? (
            <>
              <Link to="/app" className="text-slate-300 hover:text-white transition-colors text-sm font-medium">
                Analyzer
              </Link>
              <Link to="/dashboard" className="text-slate-300 hover:text-white transition-colors text-sm font-medium">
                Dashboard
              </Link>
              <button 
                onClick={handleLogout}
                className="flex items-center gap-2 text-red-400 hover:text-red-300 transition-colors text-sm font-medium ml-4 border border-red-500/30 px-3 py-1.5 rounded-lg hover:bg-red-500/10"
              >
                <LogOut size={16} /> Logout
              </button>
            </>
          ) : (
            <>
              <Link to="/login" className="flex items-center gap-2 text-slate-300 hover:text-white transition-colors text-sm font-medium px-4 py-2">
                Login
              </Link>
              <Link to="/login" className="flex items-center gap-2 bg-blue-600 hover:bg-blue-500 text-white transition-colors text-sm font-medium px-4 py-2 rounded-lg">
                <LogIn size={16} /> Get Started
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
