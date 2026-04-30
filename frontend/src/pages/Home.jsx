import React, { useState } from 'react';
import { Upload, FileText, Loader2 } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { uploadCV, analyzeCV, checkAnalysisStatus } from '../services/api';

const Home = ({ setAnalysisResult }) => {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState('');
  const navigate = useNavigate();

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const pollStatus = async (jobId) => {
    return new Promise((resolve, reject) => {
      const interval = setInterval(async () => {
        try {
          const statusData = await checkAnalysisStatus(jobId);
          if (statusData.status === 'completed') {
            clearInterval(interval);
            resolve(statusData.result);
          } else if (statusData.status === 'failed') {
            clearInterval(interval);
            reject(new Error('Analysis failed on the server.'));
          } else {
            setStatus('AI is analyzing your CV (this may take a minute)...');
          }
        } catch (err) {
          clearInterval(interval);
          reject(err);
        }
      }, 2000); // Check every 2 seconds
    });
  };

  const handleAnalyze = async () => {
    if (!file) return;
    setLoading(true);
    setStatus('Extracting text from PDF...');
    try {
      const { text } = await uploadCV(file);
      setStatus('Starting background analysis job...');
      const response = await analyzeCV(text);
      
      if (response.job_id) {
        setStatus('Analysis job queued. Waiting for completion...');
        const result = await pollStatus(response.job_id);
        setAnalysisResult(result);
        navigate('/dashboard');
      } else {
        // Fallback for immediate response (if backend hasn't fully updated yet)
        setAnalysisResult(response);
        navigate('/dashboard');
      }
    } catch (err) {
      console.error(err);
      if (err.response && (err.response.status === 401 || err.response.status === 403)) {
        alert('Authentication required. Please implement login or provide a valid token.');
      } else if (err.response && err.response.status === 429) {
        alert('Daily limit reached. Please wait until tomorrow.');
      } else {
        alert('Error during analysis. Please ensure backend is running and you are logged in.');
      }
    } finally {
      setLoading(false);
      setStatus('');
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-[80vh] text-center">
      <h1 className="text-5xl font-extrabold mb-4 bg-gradient-to-r from-blue-400 to-indigo-500 bg-clip-text text-transparent">
        AI CV Analyzer
      </h1>
      <p className="text-slate-400 text-lg mb-12 max-w-2xl">
        Upload your CV in PDF format and get instant AI-powered insights, skill extraction, and scoring.
      </p>

      <div className="glass-card p-12 w-full max-w-xl">
        <label className="flex flex-col items-center justify-center border-2 border-dashed border-slate-700 rounded-2xl p-8 cursor-pointer hover:border-blue-500 transition-colors mb-8">
          <Upload className="text-slate-500 mb-4" size={48} />
          <span className="text-slate-300 font-medium">
            {file ? file.name : "Drag & drop CV or click to browse"}
          </span>
          <input type="file" className="hidden" accept=".pdf" onChange={handleFileChange} />
        </label>

        <button 
          onClick={handleAnalyze}
          disabled={!file || loading}
          className="btn-primary w-full flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? (
            <>
              <Loader2 className="animate-spin" /> {status}
            </>
          ) : (
            <>
              <FileText size={20} /> Analyze CV
            </>
          )}
        </button>
      </div>
    </div>
  );
};

export default Home;
