import { Handle, Position, type NodeProps } from "@xyflow/react";
import type { Entity } from "@/domain/types";
import { typeColorVar } from "@/domain/typeColors";
import "./PhotoNode.css";

export interface PhotoNodeData extends Record<string, unknown> {
  entity: Entity;
}

/** Returns initials from a label: "Alice Carter" -> "AC", "ACME Holdings" -> "AH". */
function initials(label: string): string {
  return label
    .split(/\s+/)
    .map((w) => w[0])
    .filter(Boolean)
    .slice(0, 2)
    .join("")
    .toUpperCase();
}

export function PhotoNode({ data }: NodeProps) {
  const entity = (data as PhotoNodeData).entity;
  const color = typeColorVar[entity.type];

  return (
    <div
      className="photo-node"
      style={{ ["--type-color" as never]: color }}
      title={entity.label}
    >
      <div className="photo-node__frame">
        {entity.imageUrl ? (
          <img src={entity.imageUrl} alt={entity.label} />
        ) : (
          <div className="photo-node__placeholder">
            <span>{initials(entity.label)}</span>
          </div>
        )}
        <div className="photo-node__pill">
          <span className="photo-node__dot" />
          <span>{entity.type.toUpperCase()}</span>
        </div>
      </div>
      <Handle type="target" position={Position.Top} className="rf-handle" />
      <Handle type="source" position={Position.Bottom} className="rf-handle" />
    </div>
  );
}
