import React from 'react';

const ScoreBar = ({ score }) => {
  const getColor = (s) => {
    if (s > 75) return 'bg-green-500';
    if (s > 50) return 'bg-yellow-500';
    return 'bg-red-500';
  };

  return (
    <div className="w-full">
      <div className="flex justify-between items-center mb-2">
        <span className="text-sm font-medium text-slate-400">Match Score</span>
        <span className="text-2xl font-bold text-white">{score}%</span>
      </div>
      <div className="h-4 w-full bg-slate-800 rounded-full overflow-hidden">
        <div 
          className={`h-full ${getColor(score)} transition-all duration-1000 ease-out`}
          style={{ width: `${score}%` }}
        ></div>
      </div>
    </div>
  );
};

export default ScoreBar;
