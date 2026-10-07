import React from 'react';

interface Props {
  id: string;
  title: string;
  desc: string;
  icon: React.ElementType;
  status: number; // 0=idle, 1=running, 2=success, 3=error
  active: boolean;
  onClick: () => void;
}

const PipelineStage: React.FC<Props> = ({ title, desc, icon: Icon, status, active, onClick }) => {
  let dot = 'bg-custom-border';
  if (status === 1) dot = 'bg-custom-sub animate-pulse';
  if (status === 2) dot = 'bg-custom-text';
  if (status === 3) dot = 'bg-red-500';

  const base = active
    ? 'border-custom-text bg-custom-text'
    : 'border-custom-border bg-white hover:bg-custom-bg';

  return (
    <button
      onClick={onClick}
      className={`w-full text-left p-2.5 rounded border ${base} transition-colors duration-150 focus:outline-none focus:ring-1 focus:ring-custom-text group`}
    >
      <div className="flex items-center justify-between mb-1">
        <div className="flex items-center gap-2">
          <Icon className={`w-3.5 h-3.5 ${active ? 'text-white' : 'text-custom-sub group-hover:text-custom-text'}`} />
          <h3 className={`font-semibold text-xs tracking-tight ${active ? 'text-white' : 'text-custom-text'}`}>
            {title}
          </h3>
        </div>
        <div className={`w-2 h-2 rounded-full shrink-0 ${dot}`} />
      </div>
      <p className={`text-[11px] ${active ? 'text-white/70' : 'text-custom-sub'} pl-[22px]`}>{desc}</p>
    </button>
  );
};

export default PipelineStage;
