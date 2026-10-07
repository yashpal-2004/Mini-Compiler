import React from 'react';

const AssemblyViewer: React.FC<{ assembly: string[] }> = ({ assembly }) => (
  <div className="flex flex-col h-full rounded border border-custom-border overflow-hidden bg-white">
    <div className="px-4 py-2.5 border-b border-custom-border bg-custom-panel flex justify-between items-center">
      <div>
        <h3 className="text-sm font-semibold text-custom-text">MiniASM — Code Generation</h3>
        <p className="text-xs text-custom-sub mt-0.5">Converts optimized TAC into educational target assembly.</p>
      </div>
      <span className="text-custom-muted bg-custom-bg border border-custom-border px-2 py-1 rounded text-xs shrink-0">
        Educational Target
      </span>
    </div>
    <div className="flex-1 overflow-auto p-4 font-mono text-sm leading-relaxed bg-custom-bg">
      {assembly.map((line, i) => {
        const isLabel = line.endsWith(':');
        const parts = line.split(' ');
        const mnemonic = isLabel ? '' : parts[0];
        const args = isLabel ? '' : parts.slice(1).join(' ');

        return (
          <div key={i} className="flex hover:bg-custom-panel px-1 rounded transition-colors">
            <span className="w-9 text-custom-muted select-none text-xs py-0.5">{i + 1}</span>
            <div className="flex-1 py-0.5">
              {isLabel ? (
                <span className="text-custom-text font-semibold text-xs">{line}</span>
              ) : (
                <div className="pl-4">
                  <span className="text-custom-sub font-semibold w-14 inline-block text-xs">{mnemonic}</span>
                  <span className="text-custom-text text-xs">{args}</span>
                </div>
              )}
            </div>
          </div>
        );
      })}
    </div>
  </div>
);

export default AssemblyViewer;
