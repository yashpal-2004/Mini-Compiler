export interface Token {
    type: string;
    value: string;
    line: number;
    column: number;
}

export interface SymbolTableEntry {
    name: string;
    type: string;
    scope: string;
    initialized: boolean;
}

export interface CompilerError {
    phase: string;
    type: string;
    message: string;
    line: number;
    column: number;
    suggestion: string;
}

export interface TACInstruction {
    op: string | null;
    arg1: string | null;
    arg2: string | null;
    result: string | null;
    label: string | null;
    formatted: string;
}

export interface OptimizationSummary {
    name: string;
    count: number;
}

export interface CompileResponse {
    success: boolean;
    phase?: string;
    tokens: Token[];
    ast: any;
    symbolTable: SymbolTableEntry[];
    semanticErrors: CompilerError[];
    semanticWarnings: any[];
    tac: TACInstruction[];
    optimizedTac: TACInstruction[];
    optimizations: OptimizationSummary[];
    assembly: string[];
    errors: CompilerError[];
}
