import React, { useMemo } from 'react';
import ReactFlow, { Background, Controls, Node, Edge, MarkerType } from 'reactflow';

const generateGraph = (
  astNode: any,
  x: number,
  y: number,
  idCounter = { current: 0 },
  parentId: string | null = null,
  levelWidth = 250
) => {
  const nodes: Node[] = [];
  const edges: Edge[] = [];
  if (!astNode) return { nodes, edges };

  const currentId = `node-${idCounter.current++}`;
  let label = astNode.type;
  let extra = '';
  if (astNode.name) extra = astNode.name;
  if (astNode.value !== undefined && typeof astNode.value !== 'object') extra = String(astNode.value);
  if (astNode.operator) extra = astNode.operator;

  nodes.push({
    id: currentId,
    position: { x, y },
    data: {
      label: (
        <div className="flex flex-col items-center">
          <span className="font-semibold text-[10px] text-custom-sub uppercase tracking-wide">{label}</span>
          {extra && (
            <span className="text-xs font-mono mt-1 text-custom-text bg-custom-bg border border-custom-border px-1.5 py-0.5 rounded">
              {extra}
            </span>
          )}
        </div>
      )
    },
    type: 'default',
    style: {
      background: '#FFFFFF',
      color: '#111111',
      border: '1px solid #CCCCCC',
      borderRadius: '6px',
      padding: '8px',
      minWidth: '100px',
    }
  });

  if (parentId) {
    edges.push({
      id: `edge-${parentId}-${currentId}`,
      source: parentId,
      target: currentId,
      type: 'smoothstep',
      style: { stroke: '#999999', strokeWidth: 1.5 },
      markerEnd: { type: MarkerType.ArrowClosed, color: '#999999' },
    });
  }

  let children: any[] = [];
  if (astNode.declarations) children = astNode.declarations;
  if (astNode.body && Array.isArray(astNode.body)) children = astNode.body;
  else if (astNode.body) children = [astNode.body];
  if (astNode.statements) children = astNode.statements;
  if (astNode.initializer) children.push(astNode.initializer);
  if (astNode.value && typeof astNode.value === 'object') children.push(astNode.value);
  if (astNode.condition) children.push(astNode.condition);
  if (astNode.then_branch) children.push(astNode.then_branch);
  if (astNode.else_branch) children.push(astNode.else_branch);
  if (astNode.left) children.push(astNode.left);
  if (astNode.right) children.push(astNode.right);

  const childY = y + 80;
  const totalWidth = (children.length - 1) * levelWidth;
  let startX = x - totalWidth / 2;

  children.forEach(child => {
    if (child) {
      const result = generateGraph(child, startX, childY, idCounter, currentId, levelWidth * 0.7);
      nodes.push(...result.nodes);
      edges.push(...result.edges);
      startX += levelWidth;
    }
  });

  return { nodes, edges };
};

const ASTVisualizer: React.FC<{ ast: any }> = ({ ast }) => {
  const { initialNodes, initialEdges } = useMemo(() => {
    if (!ast) return { initialNodes: [], initialEdges: [] };
    const { nodes, edges } = generateGraph(ast, 400, 30);
    return { initialNodes: nodes, initialEdges: edges };
  }, [ast]);

  return (
    <div className="flex flex-col h-full rounded border border-custom-border overflow-hidden bg-white">
      <div className="px-4 py-2.5 border-b border-custom-border bg-custom-panel z-10">
        <h3 className="text-sm font-semibold text-custom-text">Abstract Syntax Tree</h3>
        <p className="text-xs text-custom-muted mt-0.5">The parser checks token grammar and constructs an AST.</p>
      </div>
      <div className="flex-1 w-full">
        <ReactFlow nodes={initialNodes} edges={initialEdges} fitView minZoom={0.2} style={{ background: '#EBEBEB' }}>
          <Background color="#CCCCCC" gap={16} size={1} />
          <Controls className="bg-white border border-custom-border" />
        </ReactFlow>
      </div>
    </div>
  );
};

export default ASTVisualizer;
