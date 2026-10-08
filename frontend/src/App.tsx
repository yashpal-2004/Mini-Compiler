import React, { useState } from 'react';
import { Play, Code2, GitMerge, FileCode, Beaker, Zap, MonitorDown, RotateCcw, XSquare, BookOpen } from 'lucide-react';
import Editor from '@monaco-editor/react';
import { compileCode } from './services/compilerApi';
import { CompileResponse } from './types/compiler';
import PipelineStage from './components/PipelineStage';
import TokenTable from './components/TokenTable';
import ASTVisualizer from './components/ASTVisualizer';
import SymbolTable from './components/SymbolTable';
import TACViewer from './components/TACViewer';
import AssemblyViewer from './components/AssemblyViewer';

const EXAMPLES: { label: string; code: string }[] = [
  {
    label: "Massive: Prime Number Checker",
    code: `#include <iostream>\nusing namespace std;\n\nint main() {\n    int target = 29;\n    int divisor = 2;\n    bool is_prime = true;\n    \n    // MiniLang lacks the modulo (%) operator, \n    // so we emulate it using division and multiplication.\n    while (divisor < target) {\n        int quotient = target / divisor;\n        int remainder = target - (quotient * divisor);\n        \n        if (remainder == 0) {\n            is_prime = false;\n        }\n        divisor = divisor + 1;\n    }\n    \n    return is_prime;\n}`
  },
  {
    label: "Massive: 5-Variable Bubble Sort",
    code: `#include <iostream>\nusing namespace std;\n\nint main() {\n    // No arrays in MiniLang! Simulating an array of size 5.\n    int v1 = 45;\n    int v2 = 12;\n    int v3 = 89;\n    int v4 = 2;\n    int v5 = 34;\n    \n    bool swapped = true;\n    int temp = 0;\n    \n    while (swapped) {\n        swapped = false;\n        \n        if (v1 > v2) {\n            temp = v1;\n            v1 = v2;\n            v2 = temp;\n            swapped = true;\n        }\n        \n        if (v2 > v3) {\n            temp = v2;\n            v2 = v3;\n            v3 = temp;\n            swapped = true;\n        }\n        \n        if (v3 > v4) {\n            temp = v3;\n            v3 = v4;\n            v4 = temp;\n            swapped = true;\n        }\n        \n        if (v4 > v5) {\n            temp = v4;\n            v4 = v5;\n            v5 = temp;\n            swapped = true;\n        }\n    }\n    \n    // Returns the largest value which bubbles up to v5\n    return v5;\n}`
  },
  {
    label: "Massive: GCD and LCM Calculator",
    code: `#include <iostream>\nusing namespace std;\n\nint main() {\n    int num1 = 252;\n    int num2 = 105;\n    int orig_n1 = num1;\n    int orig_n2 = num2;\n    \n    // Find GCD using repeated subtraction\n    while (num1 != num2) {\n        if (num1 > num2) {\n            num1 = num1 - num2;\n        } else {\n            num2 = num2 - num1;\n        }\n    }\n    \n    int gcd = num1;\n    \n    // Compute Least Common Multiple (LCM)\n    int lcm = (orig_n1 * orig_n2) / gcd;\n    \n    // Check if GCD is a prime number (emulating modulo)\n    int div = 2;\n    bool is_gcd_prime = true;\n    \n    while (div < gcd) {\n        int q = gcd / div;\n        int rem = gcd - (q * div);\n        if (rem == 0) {\n            is_gcd_prime = false;\n        }\n        div = div + 1;\n    }\n    \n    if (is_gcd_prime) {\n        return lcm;\n    } else {\n        return gcd;\n    }\n}`
  },
  {
    label: "Massive: Integer Square Root",
    code: `#include <iostream>\nusing namespace std;\n\nint main() {\n    int target = 10000;\n    int low = 0;\n    int high = target;\n    int ans = 0;\n    \n    // Binary search for integer square root\n    while (low <= high) {\n        int mid = low + (high - low) / 2;\n        int square = mid * mid;\n        \n        if (square == target) {\n            return mid;\n        }\n        \n        if (square < target) {\n            low = mid + 1;\n            ans = mid;\n        } else {\n            high = mid - 1;\n        }\n    }\n    \n    return ans;\n}`
  },
  {
    label: "Massive: Collatz Max Sequence",
    code: `#include <iostream>\nusing namespace std;\n\nint main() {\n    // Find max Collatz sequence length for numbers 1 to 20\n    int max_len = 0;\n    int max_num = 0;\n    int current = 1;\n    \n    while (current <= 20) {\n        int n = current;\n        int length = 1;\n        \n        while (n > 1) {\n            int q = n / 2;\n            int rem = n - (q * 2);\n            \n            if (rem == 0) {\n                n = n / 2;\n            } else {\n                n = (3 * n) + 1;\n            }\n            length = length + 1;\n        }\n        \n        if (length > max_len) {\n            max_len = length;\n            max_num = current;\n        }\n        \n        current = current + 1;\n    }\n    \n    return max_num;\n}`
  }
];

const DEFAULT_CODE = EXAMPLES[0].code;
type Stage = 'source' | 'lexical' | 'syntax' | 'semantic' | 'tac' | 'optimization' | 'codegen';

function App() {
  const [code, setCode] = useState(DEFAULT_CODE);
  const [isCompiling, setIsCompiling] = useState(false);
  const [result, setResult] = useState<CompileResponse | null>(null);
  const [activeStage, setActiveStage] = useState<Stage>('source');
  const [networkError, setNetworkError] = useState(false);
  const [showExamples, setShowExamples] = useState(false);

  const [stageStatus, setStageStatus] = useState<Record<Stage, number>>({
    source: 2, lexical: 0, syntax: 0, semantic: 0, tac: 0, optimization: 0, codegen: 0
  });

  const handleCompile = async () => {
    setIsCompiling(true);
    setResult(null);
    setNetworkError(false);
    setStageStatus({ source: 2, lexical: 1, syntax: 0, semantic: 0, tac: 0, optimization: 0, codegen: 0 });

    try {
      const res = await compileCode(code);
      setResult(res);

      const animateStages = async () => {
        const stages: Stage[] = ['lexical', 'syntax', 'semantic', 'tac', 'optimization', 'codegen'];
        let hasError = false;
        for (let i = 0; i < stages.length; i++) {
          const stage = stages[i];
          if (hasError) break;
          setStageStatus(prev => ({ ...prev, [stage]: 1 }));
          await new Promise(resolve => setTimeout(resolve, 280));
          if (!res.success && res.phase === stage) {
            setStageStatus(prev => ({ ...prev, [stage]: 3 }));
            hasError = true;
          } else {
            setStageStatus(prev => ({ ...prev, [stage]: 2 }));
          }
        }
        setIsCompiling(false);
        setActiveStage(hasError ? (res.phase as Stage) : 'codegen');
      };
      animateStages();
    } catch {
      setNetworkError(true);
      setIsCompiling(false);
      setStageStatus(prev => ({ ...prev, lexical: 3 }));
    }
  };

  const loadExample = (exampleCode: string) => {
    setCode(exampleCode);
    setShowExamples(false);
    setResult(null);
    setStageStatus({ source: 2, lexical: 0, syntax: 0, semantic: 0, tac: 0, optimization: 0, codegen: 0 });
    setActiveStage('source');
  };

  const lineCount = code.split('\n').length;
  const charCount = code.length;

  return (
    <div className="flex flex-col h-screen bg-custom-bg text-custom-text font-sans">
      {/* Header */}
      <header className="flex items-center justify-between px-5 py-3 border-b border-custom-border bg-custom-panel shrink-0">
        <div>
          <h1 className="text-sm font-semibold text-custom-text tracking-tight leading-tight">Mini Compiler</h1>
          <p className="text-xs text-custom-muted mt-0.5">Educational pipeline visualizer</p>
        </div>
        <div className="flex items-center gap-2">
          {networkError && (
            <span className="text-xs text-red-700 bg-red-50 border border-red-200 px-2 py-1 rounded">
              Backend unreachable — is the server running?
            </span>
          )}
          <div className="relative">
            <button
              onClick={() => setShowExamples(v => !v)}
              className="px-3 py-1.5 text-xs font-medium text-custom-sub hover:text-custom-text hover:bg-custom-bg rounded transition-colors border border-custom-border"
            >
              Examples
            </button>
            {showExamples && (
              <div className="absolute right-0 top-full mt-1 w-52 bg-custom-panel border border-custom-border rounded shadow-lg z-50">
                {EXAMPLES.map((ex, i) => (
                  <button
                    key={i}
                    onClick={() => loadExample(ex.code)}
                    className="w-full text-left px-3 py-2 text-xs text-custom-sub hover:bg-custom-bg hover:text-custom-text transition-colors border-b border-custom-border last:border-0"
                  >
                    {ex.label}
                  </button>
                ))}
              </div>
            )}
          </div>
          <button
            onClick={() => { setCode(DEFAULT_CODE); setResult(null); setActiveStage('source'); setStageStatus({ source: 2, lexical: 0, syntax: 0, semantic: 0, tac: 0, optimization: 0, codegen: 0 }); }}
            className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium text-custom-sub hover:text-custom-text hover:bg-custom-bg rounded transition-colors border border-custom-border"
          >
            <RotateCcw className="w-3.5 h-3.5" /> Reset
          </button>
          <button
            onClick={() => { setCode(''); setResult(null); setActiveStage('source'); setStageStatus({ source: 2, lexical: 0, syntax: 0, semantic: 0, tac: 0, optimization: 0, codegen: 0 }); }}
            className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium text-custom-sub hover:text-custom-text hover:bg-custom-bg rounded transition-colors border border-custom-border"
          >
            <XSquare className="w-3.5 h-3.5" /> Clear
          </button>
          <button
            onClick={handleCompile}
            disabled={isCompiling || !code.trim()}
            className="flex items-center gap-1.5 px-4 py-1.5 bg-custom-cta hover:bg-custom-sub disabled:opacity-40 text-white rounded text-xs font-semibold transition-colors"
          >
            <Play className="w-3.5 h-3.5" fill="currentColor" /> {isCompiling ? 'Compiling...' : 'Compile'}
          </button>
        </div>
      </header>

      <main className="flex flex-1 overflow-hidden">
        {/* LEFT — Editor */}
        <div className="w-[38%] flex flex-col border-r border-custom-border min-w-0 bg-white">
          <div className="flex items-center justify-between px-4 py-2 border-b border-custom-border bg-custom-panel shrink-0">
            <span className="text-xs font-semibold text-custom-sub uppercase tracking-wider">Source Editor</span>
            <span className="text-xs text-custom-sub font-mono">{lineCount} lines · {charCount} chars</span>
          </div>
          <div className="flex-1 min-h-0">
            <Editor
              height="100%"
              defaultLanguage="c"
              theme="vs-light"
              value={code}
              onChange={val => setCode(val || '')}
              options={{
                minimap: { enabled: false },
                fontSize: 13,
                fontFamily: "ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace",
                padding: { top: 12 },
                scrollBeyondLastLine: false,
                lineHeight: 1.65,
                renderLineHighlight: 'line',
              }}
            />
          </div>
        </div>

        {/* CENTER — Pipeline */}
        <div className="w-52 shrink-0 flex flex-col border-r border-custom-border bg-custom-panel overflow-y-auto scrollbar-hide">
          <div className="px-3 py-2 border-b border-custom-border shrink-0">
            <span className="text-xs font-semibold text-custom-sub uppercase tracking-wider">Pipeline</span>
          </div>
          <div className="flex flex-col gap-1.5 p-3">
            {([
              { id: 'source',       title: 'Source Code',      desc: 'Raw input', icon: Code2 },
              { id: 'lexical',      title: 'Lexical Analysis',  desc: 'Tokenization', icon: FileCode },
              { id: 'syntax',       title: 'Syntax Analysis',   desc: 'AST construction', icon: GitMerge },
              { id: 'semantic',     title: 'Semantic Analysis', desc: 'Type & scope', icon: Beaker },
              { id: 'tac',          title: '3-Address Code',    desc: 'Intermediate rep.', icon: BookOpen },
              { id: 'optimization', title: 'Optimization',      desc: 'Code improvement', icon: Zap },
              { id: 'codegen',      title: 'Code Generation',   desc: 'MiniASM output', icon: MonitorDown },
            ] as { id: Stage; title: string; desc: string; icon: any }[]).map((s, i, arr) => (
              <div key={s.id} className="flex flex-col items-stretch">
                <PipelineStage
                  id={s.id}
                  title={s.title}
                  desc={s.desc}
                  icon={s.icon}
                  status={stageStatus[s.id]}
                  active={activeStage === s.id}
                  onClick={() => setActiveStage(s.id)}
                />
                {i < arr.length - 1 && (
                  <div className="flex justify-center my-0.5">
                    <div className="w-px h-3 bg-custom-border"></div>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* RIGHT — Inspector */}
        <div className="flex-1 flex flex-col min-w-0 bg-custom-bg">
          <div className="px-4 py-2 border-b border-custom-border bg-custom-panel shrink-0">
            <span className="text-xs font-semibold text-custom-sub uppercase tracking-wider">
              Inspector — {activeStage.replace(/([A-Z])/g, ' $1').trim()}
            </span>
          </div>
          <div className="flex-1 overflow-auto p-5">

            {/* Source stats */}
            {activeStage === 'source' && (
              <div className="flex flex-col gap-4">
                <div className="grid grid-cols-3 gap-3">
                  {[
                    { label: 'Lines',      value: lineCount },
                    { label: 'Characters', value: charCount },
                    { label: 'Tokens',     value: result ? result.tokens.length : '—' },
                  ].map(stat => (
                    <div key={stat.label} className="bg-custom-panel border border-custom-border rounded p-3">
                      <p className="text-[10px] text-custom-muted uppercase tracking-widest mb-1">{stat.label}</p>
                      <p className="text-xl font-semibold text-custom-text font-mono">{stat.value}</p>
                    </div>
                  ))}
                </div>
                <p className="text-sm text-custom-sub">
                  Click <strong className="text-custom-text font-semibold">Compile</strong> to run the full pipeline, then click any stage to inspect its output.
                </p>
              </div>
            )}

            {/* Awaiting compile */}
            {!result && activeStage !== 'source' && (
              <div className="h-full flex items-center justify-center">
                <p className="text-sm text-custom-sub">Awaiting compilation...</p>
              </div>
            )}

            {result && activeStage !== 'source' && (
              <div className="h-full flex flex-col">
                {/* Error panel */}
                {!result.success && result.phase === activeStage && result.errors.length > 0 && (
                  <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded">
                    <p className="text-[10px] font-semibold text-red-700 uppercase tracking-widest mb-1">{result.errors[0].type}</p>
                    <p className="text-sm text-red-800 mb-1">{result.errors[0].message}</p>
                    <p className="text-xs text-red-500 font-mono mb-2">Line {result.errors[0].line}, Col {result.errors[0].column}</p>
                    {result.errors[0].suggestion && (
                      <p className="text-xs text-amber-800 bg-amber-50 border border-amber-200 p-2 rounded">
                        Suggestion: {result.errors[0].suggestion}
                      </p>
                    )}
                  </div>
                )}

                {activeStage === 'lexical'      && <TokenTable tokens={result.tokens} />}
                {activeStage === 'syntax'        && <ASTVisualizer ast={result.ast} />}
                {activeStage === 'semantic'      && <SymbolTable symbols={result.symbolTable} warnings={result.semanticWarnings} />}
                {activeStage === 'tac'           && <TACViewer tac={result.tac} />}
                {activeStage === 'optimization'  && <TACViewer tac={result.optimizedTac} originalTac={result.tac} optimizations={result.optimizations} isOptimized />}
                {activeStage === 'codegen'       && <AssemblyViewer assembly={result.assembly} />}
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
