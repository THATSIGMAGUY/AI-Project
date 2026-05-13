import { useMemo } from "react";
import {
  ReactFlow,
  Background,
  Controls,
  MarkerType,
  type Edge as RFEdge,
  type Node as RFNode,
  type NodeTypes,
  type EdgeTypes,
} from "@xyflow/react";

import type { CaseGraph, Entity } from "@/domain/types";
import { EntityPillNode } from "./nodes/EntityPillNode";
import { PhotoNode } from "./nodes/PhotoNode";
import { PillEdge } from "./edges/PillEdge";

const nodeTypes: NodeTypes = {
  pill: EntityPillNode,
  photo: PhotoNode,
};

const edgeTypes: EdgeTypes = {
  pill: PillEdge,
};

/**
 * Layout hints are stashed in `entity.properties.layout = { x, y, kind }`.
 * `kind` selects pill vs photo rendering. We treat layout as data, not as a
 * separate concern, because in an investigation the analyst's hand-arranged
 * positions ARE part of the case record.
 */
function entityKind(entity: Entity): "pill" | "photo" {
  const hint = (entity.properties?.layout as { kind?: string } | undefined)?.kind;
  if (hint === "photo" || hint === "pill") return hint;
  return entity.imageUrl ? "photo" : "pill";
}

function entityPosition(entity: Entity, fallback: { x: number; y: number }) {
  const pos = entity.properties?.layout as { x?: number; y?: number } | undefined;
  return { x: pos?.x ?? fallback.x, y: pos?.y ?? fallback.y };
}

export interface GraphCanvasProps {
  graph: CaseGraph;
}

export function GraphCanvas({ graph }: GraphCanvasProps) {
  const nodes: RFNode[] = useMemo(
    () =>
      graph.entities.map((e, i) => ({
        id: e.id,
        type: entityKind(e),
        position: entityPosition(e, { x: i * 220, y: i * 80 }),
        data: { entity: e },
      })),
    [graph.entities],
  );

  const edges: RFEdge[] = useMemo(
    () =>
      graph.edges.map((e) => ({
        id: e.id,
        type: "pill",
        source: e.sourceId,
        target: e.targetId,
        label: e.label ?? e.type,
        markerEnd: { type: MarkerType.ArrowClosed, color: "var(--edge-color)" },
      })),
    [graph.edges],
  );

  return (
    <ReactFlow
      nodes={nodes}
      edges={edges}
      nodeTypes={nodeTypes}
      edgeTypes={edgeTypes}
      fitView
      fitViewOptions={{ padding: 0.3 }}
      proOptions={{ hideAttribution: true }}
      minZoom={0.3}
      maxZoom={2.5}
    >
      <Background gap={28} size={1} color="var(--border)" />
      <Controls showInteractive={false} />
    </ReactFlow>
  );
}
