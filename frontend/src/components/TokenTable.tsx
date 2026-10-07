import React from 'react';
import { Token } from '../types/compiler';

const TokenTable: React.FC<{ tokens: Token[] }> = ({ tokens }) => (
  <div className="flex flex-col h-full rounded border border-custom-border overflow-hidden bg-white">
    <div className="px-4 py-2.5 border-b border-custom-border bg-custom-panel">
      <h3 className="text-sm font-semibold text-custom-text">Token Stream</h3>
      <p className="text-xs text-custom-sub mt-0.5">The lexer converts source characters into meaningful tokens.</p>
    </div>
    <div className="flex-1 overflow-auto">
      <table className="w-full text-left text-sm">
        <thead className="text-xs uppercase text-custom-sub sticky top-0 bg-custom-panel">
          <tr>
            <th className="px-4 py-2.5 font-semibold tracking-wider border-b border-custom-border">Token Type</th>
            <th className="px-4 py-2.5 font-semibold tracking-wider border-b border-custom-border">Lexeme</th>
            <th className="px-4 py-2.5 font-semibold tracking-wider border-b border-custom-border">Line</th>
            <th className="px-4 py-2.5 font-semibold tracking-wider border-b border-custom-border">Col</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-custom-border">
          {tokens.map((token, i) => (
            <tr key={i} className="hover:bg-custom-bg transition-colors">
              <td className="px-4 py-2 font-mono text-custom-sub text-xs">{token.type}</td>
              <td className="px-4 py-2">
                <span className="font-mono text-custom-text text-xs bg-custom-bg border border-custom-border px-1.5 py-0.5 rounded">
                  {token.value}
                </span>
              </td>
              <td className="px-4 py-2 text-custom-muted text-xs">{token.line}</td>
              <td className="px-4 py-2 text-custom-muted text-xs">{token.column}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  </div>
);

export default TokenTable;
