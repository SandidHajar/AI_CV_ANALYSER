import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Brain, Star, AlertCircle, Award, User, ArrowLeft } from 'lucide-react';
import ScoreBar from '../components/ScoreBar';
import ResultCard from '../components/ResultCard';

const Dashboard = ({ result }) => {
  const navigate = useNavigate();

  if (!result) {
    return (
      <div className="text-center py-20">
        <h2 className="text-2xl font-bold mb-4">No analysis found</h2>
        <button onClick={() => navigate('/')} className="btn-primary">Go Back</button>
      </div>
    );
  }

  return (
    <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
      <div className="flex items-center gap-4">
        <button onClick={() => navigate('/')} className="p-2 hover:bg-slate-800 rounded-full transition-colors">
          <ArrowLeft size={24} />
        </button>
        <h2 className="text-3xl font-bold">Analysis Results</h2>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="md:col-span-2 glass-card p-8 flex flex-col justify-center">
          <ScoreBar score={result.score} />
          <div className="mt-6 flex gap-3 flex-wrap">
            {result.skills.map(skill => (
              <span key={skill} className="bg-blue-500/10 text-blue-400 px-3 py-1 rounded-full text-sm font-medium border border-blue-500/20">
                {skill}
              </span>
            ))}
          </div>
        </div>

        <ResultCard title="Experience" icon={Award}>
          <div className="flex flex-col items-center justify-center h-full">
            <span className="text-4xl font-bold text-white capitalize">{result.experience_level}</span>
            <span className="text-slate-400 mt-2">Level Detection</span>
          </div>
        </ResultCard>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="md:col-span-3">
          <ResultCard title="Professional Summary" icon={User}>
            <p className="text-lg leading-relaxed italic">"{result.summary || 'AI Summary not available'}"</p>
          </ResultCard>
        </div>

        <ResultCard title="Strengths" icon={Star}>
          <ul className="space-y-3">
            {(result.strengths || []).map((s, i) => (
              <li key={i} className="flex items-start gap-2">
                <span className="text-green-500 mt-1">✓</span> {s}
              </li>
            ))}
          </ul>
        </ResultCard>

        <ResultCard title="Weaknesses" icon={AlertCircle}>
          <ul className="space-y-3">
            {(result.weaknesses || []).map((w, i) => (
              <li key={i} className="flex items-start gap-2">
                <span className="text-red-500 mt-1">⚠</span> {w}
              </li>
            ))}
          </ul>
        </ResultCard>

        <ResultCard title="AI Brain Insights" icon={Brain}>
          <p className="text-sm">
            Our neural model suggests this candidate is a strong fit for roles requiring {result.skills[0] || 'technical expertise'}.
          </p>
        </ResultCard>
      </div>
    </div>
  );
};

export default Dashboard;
