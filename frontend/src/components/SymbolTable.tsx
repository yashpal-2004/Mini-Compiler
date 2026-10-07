import React from 'react';
import { SymbolTableEntry } from '../types/compiler';

const SymbolTable: React.FC<{ symbols: SymbolTableEntry[]; warnings: any[] }> = ({ symbols, warnings }) => (
  <div className="flex flex-col h-full space-y-3">
    <div className="flex flex-col flex-1 rounded border border-custom-border overflow-hidden bg-white">
      <div className="px-4 py-2.5 border-b border-custom-border bg-custom-panel">
        <h3 className="text-sm font-semibold text-custom-text">Symbol Table</h3>
        <p className="text-xs text-custom-sub mt-0.5">Checks types, declarations, and scope.</p>
      </div>
      <div className="flex-1 overflow-auto">
        <table className="w-full text-left text-sm">
          <thead className="text-xs uppercase text-custom-sub sticky top-0 bg-custom-panel">
            <tr>
              <th className="px-4 py-2.5 font-semibold tracking-wider border-b border-custom-border">Name</th>
              <th className="px-4 py-2.5 font-semibold tracking-wider border-b border-custom-border">Type</th>
              <th className="px-4 py-2.5 font-semibold tracking-wider border-b border-custom-border">Scope</th>
              <th className="px-4 py-2.5 font-semibold tracking-wider border-b border-custom-border">Init.</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-custom-border">
            {symbols.map((sym, i) => (
              <tr key={i} className="hover:bg-custom-bg transition-colors">
                <td className="px-4 py-2 font-mono text-custom-text font-medium text-xs">{sym.name}</td>
                <td className="px-4 py-2 text-custom-sub text-xs">{sym.type}</td>
                <td className="px-4 py-2 text-custom-muted text-xs">{sym.scope}</td>
                <td className="px-4 py-2">
                  {sym.initialized
                    ? <span className="text-custom-text bg-custom-bg border border-custom-border px-2 py-0.5 rounded text-xs font-mono">true</span>
                    : <span className="text-red-600 bg-red-50 border border-red-200 px-2 py-0.5 rounded text-xs font-mono">false</span>
                  }
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>

    {warnings?.length > 0 && (
      <div className="border border-amber-200 rounded p-3 shrink-0 bg-amber-50">
        <h4 className="text-amber-800 font-semibold text-xs mb-1">Semantic Warnings</h4>
        <ul className="space-y-1">
          {warnings.map((w, i) => (
            <li key={i} className="text-xs text-amber-700">{w.message}</li>
          ))}
        </ul>
      </div>
    )}
  </div>
);

export default SymbolTable;
