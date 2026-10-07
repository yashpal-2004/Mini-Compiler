# Mini Compiler Pipeline Visualizer

An interactive educational web application that visually demonstrates the full compiler pipeline, from source code to target machine assembly, for a custom C-like language (MiniLang).

## Features
- **Interactive Source Editor**: Monaco-editor powered IDE interface.
- **Visual Pipeline**: Step-by-step animation of compiler phases.
- **Lexical Analysis**: Custom lexer that generates tokens.
- **Syntax Analysis**: Recursive descent parser building an AST, visualized visually with React Flow.
- **Semantic Analysis**: Type checking, scope validation, and symbol table generation.
- **Three Address Code (TAC)**: Intermediate representation generation.
- **Optimization**: Basic constant folding, propagation, algebraic simplification, and dead code elimination passes.
- **Code Generation**: Converts optimized TAC into "MiniASM", an educational target assembly language.

## Architecture
- **Frontend**: React, TypeScript, Vite, Tailwind CSS, React Flow, Monaco Editor.
- **Backend**: Python, FastAPI.

The backend exposes a single API endpoint (`POST /compile`) which receives the source code and returns the complete structured data output for all compiler phases. The frontend provides an interactive layout to visualize each phase.

## Compiler Phases
1. **Lexical Analysis**: Converts character stream to tokens (keywords, identifiers, literals, operators).
2. **Syntax Analysis**: Parses tokens using recursive descent and constructs an Abstract Syntax Tree (AST).
3. **Semantic Analysis**: Creates a symbol table, validates type assignments, and checks scope and conditionals.
4. **TAC**: Generates low-level three address instructions.
5. **Optimization**: Improves TAC instructions.
6. **MiniASM Code Generation**: Converts to load/store architecture educational assembly.

## MiniLang Grammar
A simple subset of a C-like language:
- Types: `int`, `float`, `bool`
- Operations: `+`, `-`, `*`, `/`, `<`, `>`, `<=`, `>=`, `==`, `!=`, `&&`, `||`
- Control flow: `if`, `else`, `while`
- Functions: Currently supports simple main blocks and returns.

## How to Run

### Backend
1. Open a terminal and navigate to `backend/`.
2. Create a virtual environment: `python -m venv venv`
3. Activate it: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Mac/Linux).
4. Install dependencies: `pip install fastapi uvicorn pydantic`
5. Run the server: `python main.py`

### Frontend
1. Open another terminal and navigate to `frontend/`.
2. Install dependencies: `npm install`
3. Run the development server: `npm run dev`
4. Open your browser at the URL shown (typically `http://localhost:5173`).

## Future Improvements
- Multi-function support (call frames, arguments).
- Arrays and pointers.
- Advanced optimizations (loop unrolling, peephole).
- Real CPU code generation (x86 or ARM).
