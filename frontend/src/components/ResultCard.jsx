import React from 'react';

const ResultCard = ({ title, icon: Icon, children }) => {
  return (
    <div className="glass-card p-6 h-full">
      <div className="flex items-center gap-3 mb-4">
        {Icon && <Icon className="text-blue-400" size={24} />}
        <h3 className="text-lg font-semibold text-white">{title}</h3>
      </div>
      <div className="text-slate-300">
        {children}
      </div>
    </div>
  );
};

export default ResultCard;
