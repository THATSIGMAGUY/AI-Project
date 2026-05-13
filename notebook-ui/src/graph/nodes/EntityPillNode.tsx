import { Handle, Position, type NodeProps } from "@xyflow/react";
import type { Entity } from "@/domain/types";
import { typeColorVar } from "@/domain/typeColors";
import "./EntityPillNode.css";

export interface PillNodeData extends Record<string, unknown> {
  entity: Entity;
}

export function EntityPillNode({ data }: NodeProps) {
  const entity = (data as PillNodeData).entity;
  const color = typeColorVar[entity.type];

  return (
    <div
      className="entity-pill"
      style={{ ["--type-color" as never]: color }}
      title={entity.label}
    >
      <span className="entity-pill__dot" />
      <span className="entity-pill__label">{entity.label.toUpperCase()}</span>
      <Handle type="target" position={Position.Top} className="rf-handle" />
      <Handle type="source" position={Position.Bottom} className="rf-handle" />
    </div>
  );
}
