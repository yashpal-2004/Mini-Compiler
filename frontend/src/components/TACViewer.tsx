import React from 'react';
import { TACInstruction, OptimizationSummary } from '../types/compiler';

interface Props {
  tac: TACInstruction[];
  originalTac?: TACInstruction[]; // Pass original if we are showing optimization
  optimizations?: OptimizationSummary[];
  isOptimized?: boolean;
}

const TACViewer: React.FC<Props> = ({ tac, originalTac, optimizations, isOptimized }) => (
  <div className="flex flex-col h-full space-y-3">
    <div className="flex flex-col flex-1 rounded border border-custom-border overflow-hidden bg-white">
      <div className="px-4 py-2.5 border-b border-custom-border bg-custom-panel flex justify-between items-center shrink-0">
        <div>
          <h3 className="text-sm font-semibold text-custom-text">
            {isOptimized ? 'Optimized Three Address Code' : 'Three Address Code (TAC)'}
          </h3>
          <p className="text-xs text-custom-sub mt-0.5">
            {isOptimized
              ? 'Optimizer improves code without changing program behavior.'
              : 'TAC is a simple intermediate representation, easier to optimize.'}
          </p>
        </div>
        {isOptimized && (
          <span className="text-custom-text bg-custom-bg border border-custom-border px-2 py-1 rounded text-xs font-medium shrink-0">
            {optimizations && optimizations.reduce((a,b)=>a+b.count,0) > 0 ? 'Optimized ✓' : 'No optimization required'}
          </span>
        )}
      </div>
      
      {isOptimized && originalTac ? (
        <div className="flex-1 flex overflow-hidden">
          {/* Left: Original */}
          <div className="flex-1 flex flex-col border-r border-custom-border">
            <div className="px-3 py-1 border-b border-custom-border bg-custom-bg text-[10px] uppercase text-custom-muted font-semibold tracking-widest text-center">
              Before Optimization
            </div>
            <div className="flex-1 overflow-auto p-4 font-mono text-sm leading-relaxed bg-custom-bg">
              <table className="w-full text-left border-collapse">
                <tbody>
                  {originalTac.map((inst, i) => (
                    <tr key={i} className="hover:bg-custom-panel transition-colors">
                      <td className="w-8 py-0.5 text-custom-muted select-none text-xs">{i + 1}</td>
                      <td className={`py-0.5 text-xs ${inst.label ? 'text-custom-text font-semibold' : 'text-custom-sub'}`}>
                        {inst.formatted}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
          
          {/* Right: Optimized */}
          <div className="flex-1 flex flex-col">
            <div className="px-3 py-1 border-b border-custom-border bg-custom-bg text-[10px] uppercase text-[#10B981] font-semibold tracking-widest text-center">
              After Optimization
            </div>
            <div className="flex-1 overflow-auto p-4 font-mono text-sm leading-relaxed bg-custom-bg">
              <table className="w-full text-left border-collapse">
                <tbody>
                  {tac.map((inst, i) => {
                    // Check if it's potentially modified/optimized (a simple heuristic for coloring)
                    const isDiff = originalTac[i]?.formatted !== inst.formatted;
                    return (
                      <tr key={i} className={`transition-colors ${isDiff ? 'bg-green-50' : 'hover:bg-custom-panel'}`}>
                        <td className="w-8 py-0.5 text-custom-muted select-none text-xs">{i + 1}</td>
                        <td className={`py-0.5 text-xs ${inst.label ? 'text-custom-text font-semibold' : (isDiff ? 'text-green-700 font-medium' : 'text-custom-text')}`}>
                          {inst.formatted}
                        </td>
                      </tr>
                    )
                  })}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      ) : (
        <div className="flex-1 overflow-auto p-4 font-mono text-sm leading-relaxed bg-custom-bg">
          <table className="w-full text-left border-collapse">
            <thead className="text-xs text-custom-sub border-b border-custom-border">
              <tr>
                <th className="w-10 pb-2 font-normal">#</th>
                <th className="pb-2 font-normal">Instruction</th>
              </tr>
            </thead>
            <tbody>
              {tac.map((inst, i) => (
                <tr key={i} className="hover:bg-custom-panel transition-colors">
                  <td className="py-0.5 text-custom-muted select-none text-xs">{i + 1}</td>
                  <td className={`py-0.5 text-xs ${inst.label ? 'text-custom-text font-semibold' : 'text-custom-sub'}`}>
                    {inst.formatted}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>

    {optimizations && optimizations.length > 0 && (
      <div className="border border-custom-border rounded p-3 shrink-0 bg-custom-panel">
        <h4 className="text-custom-text font-semibold text-xs mb-2">Optimization Summary</h4>
        <div className="grid grid-cols-2 gap-2">
          {optimizations.map((opt, i) => (
            <div key={i} className="flex justify-between items-center px-2 py-1.5 rounded border border-custom-border bg-white">
              <span className="text-custom-sub text-xs">{opt.name}</span>
              <span className={`text-xs font-medium px-1.5 py-0.5 rounded font-mono ${opt.count > 0 ? 'bg-custom-text text-white' : 'bg-custom-bg text-custom-muted'}`}>
                {opt.count > 0 ? `${opt.count} changes` : opt.count}
              </span>
            </div>
          ))}
        </div>
      </div>
    )}
  </div>
);

export default TACViewer;
