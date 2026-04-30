import React from 'react';
import { Link } from 'react-router-dom';
import { FileText, Cpu, Zap, ShieldCheck, CheckCircle2, UploadCloud, Brain, LineChart } from 'lucide-react';

const Landing = () => {
  return (
    <div className="flex flex-col items-center justify-center min-h-[85vh] text-center px-4">
      
      {/* Hero Section */}
      <div className="max-w-4xl mx-auto space-y-8 mb-24 mt-12">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-500/10 border border-blue-500/20 text-blue-400 text-sm font-medium mb-4">
          <span className="w-2 h-2 rounded-full bg-blue-500 animate-pulse"></span>
          Hybrid AI Analysis
        </div>
        
        <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight text-white leading-tight">
          AI-Powered CV Analysis Built for <br />
          <span className="bg-gradient-to-r from-blue-400 to-indigo-500 bg-clip-text text-transparent">
            Full-Stack Careers
          </span>
        </h1>
        
        <p className="text-xl text-slate-400 max-w-2xl mx-auto">
          Get actionable insights on your CV with a hybrid AI + scoring engine. Identify your strengths, fix your weaknesses, and increase your chances of landing a job.
        </p>
        
        <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-6">
          <Link to="/app" className="w-full sm:w-auto px-8 py-4 bg-blue-600 hover:bg-blue-500 text-white rounded-xl font-semibold transition-all transform hover:scale-105 shadow-[0_0_20px_rgba(37,99,235,0.4)]">
            Analyze My CV
          </Link>
          <a href="#how-it-works" className="w-full sm:w-auto px-8 py-4 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-xl font-semibold transition-all border border-slate-700">
            View Demo
          </a>
        </div>

        {/* Trust Element */}
        <div className="flex flex-wrap items-center justify-center gap-6 pt-10 text-sm font-medium text-slate-400">
          <div className="flex items-center gap-2">
            <CheckCircle2 size={18} className="text-emerald-500" />
            <span>AI-powered analysis</span>
          </div>
          <div className="flex items-center gap-2">
            <CheckCircle2 size={18} className="text-emerald-500" />
            <span>Multi-dimensional scoring</span>
          </div>
          <div className="flex items-center gap-2">
            <CheckCircle2 size={18} className="text-emerald-500" />
            <span>Instant actionable feedback</span>
          </div>
        </div>
      </div>

      {/* How It Works Section */}
      <div id="how-it-works" className="max-w-5xl mx-auto mb-32 w-full pt-10">
        <h2 className="text-3xl font-bold text-center text-white mb-12">How It Works</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 relative">
          {/* Connecting line for desktop */}
          <div className="hidden md:block absolute top-1/2 left-[10%] right-[10%] h-0.5 bg-slate-800 -translate-y-1/2 z-0"></div>
          
          <div className="relative z-10 glass-card p-8 rounded-2xl flex flex-col items-center text-center transition-transform hover:-translate-y-2">
            <div className="w-16 h-16 rounded-full bg-slate-800 border border-slate-700 flex items-center justify-center text-blue-400 mb-6 shadow-lg shadow-blue-900/20">
              <UploadCloud size={32} />
            </div>
            <h3 className="text-xl font-bold text-white mb-3">1. Upload your CV</h3>
            <p className="text-slate-400 leading-relaxed">Securely upload your resume in PDF format. We handle the text parsing instantly.</p>
          </div>

          <div className="relative z-10 glass-card p-8 rounded-2xl flex flex-col items-center text-center transition-transform hover:-translate-y-2">
            <div className="w-16 h-16 rounded-full bg-slate-800 border border-slate-700 flex items-center justify-center text-indigo-400 mb-6 shadow-lg shadow-indigo-900/20">
              <Brain size={32} />
            </div>
            <h3 className="text-xl font-bold text-white mb-3">2. AI analyzes profile</h3>
            <p className="text-slate-400 leading-relaxed">Our hybrid engine evaluates technical skills, project complexity, and experience level.</p>
          </div>

          <div className="relative z-10 glass-card p-8 rounded-2xl flex flex-col items-center text-center transition-transform hover:-translate-y-2">
            <div className="w-16 h-16 rounded-full bg-slate-800 border border-slate-700 flex items-center justify-center text-emerald-400 mb-6 shadow-lg shadow-emerald-900/20">
              <LineChart size={32} />
            </div>
            <h3 className="text-xl font-bold text-white mb-3">3. Get actionable insights</h3>
            <p className="text-slate-400 leading-relaxed">Receive an exact score breakdown, key strengths, and specific weaknesses to fix.</p>
          </div>
        </div>
      </div>

      {/* Features Grid */}
      <div id="features" className="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-5xl mx-auto text-left mb-20 w-full pt-10">
        
        <div className="glass-card p-8 rounded-2xl flex flex-col gap-4">
          <div className="w-12 h-12 rounded-xl bg-blue-500/10 flex items-center justify-center text-blue-400">
            <Cpu size={24} />
          </div>
          <h3 className="text-xl font-bold text-white">Hybrid AI Fusion Engine</h3>
          <p className="text-slate-400">
            Combines strict rule-based keyword extraction with contextual understanding from advanced Large Language Models for unparalleled accuracy.
          </p>
        </div>

        <div className="glass-card p-8 rounded-2xl flex flex-col gap-4">
          <div className="w-12 h-12 rounded-xl bg-indigo-500/10 flex items-center justify-center text-indigo-400">
            <Zap size={24} />
          </div>
          <h3 className="text-xl font-bold text-white">Multi-Dimensional Scoring</h3>
          <p className="text-slate-400">
            We don't just count keywords. We evaluate Skill Depth, Skill Coverage, Experience Signals, and DevOps Maturity to give a realistic score.
          </p>
        </div>

        <div className="glass-card p-8 rounded-2xl flex flex-col gap-4">
          <div className="w-12 h-12 rounded-xl bg-emerald-500/10 flex items-center justify-center text-emerald-400">
            <FileText size={24} />
          </div>
          <h3 className="text-xl font-bold text-white">Instant Feedback</h3>
          <p className="text-slate-400">
            Identify your strengths and weaknesses in seconds. Receive a professional summary tailored to your exact experience level.
          </p>
        </div>

        <div className="glass-card p-8 rounded-2xl flex flex-col gap-4">
          <div className="w-12 h-12 rounded-xl bg-purple-500/10 flex items-center justify-center text-purple-400">
            <ShieldCheck size={24} />
          </div>
          <h3 className="text-xl font-bold text-white">Secure & Private</h3>
          <p className="text-slate-400">
            Your data is encrypted and securely stored. Track your resume improvements over time through your personalized dashboard.
          </p>
        </div>

      </div>
    </div>
  );
};

export default Landing;

