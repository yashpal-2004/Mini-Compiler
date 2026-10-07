from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class CompileRequest(BaseModel):
    sourceCode: str

class CompileResponse(BaseModel):
    success: bool
    phase: Optional[str] = None
    tokens: List[Dict[str, Any]] = []
    ast: Dict[str, Any] = {}
    symbolTable: List[Dict[str, Any]] = []
    semanticErrors: List[Dict[str, Any]] = []
    semanticWarnings: List[Dict[str, Any]] = []
    tac: List[Dict[str, Any]] = []
    optimizedTac: List[Dict[str, Any]] = []
    optimizations: List[Dict[str, Any]] = []
    assembly: List[str] = []
    errors: List[Dict[str, Any]] = []
