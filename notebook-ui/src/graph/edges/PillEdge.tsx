import {
  BaseEdge,
  EdgeLabelRenderer,
  getBezierPath,
  type EdgeProps,
} from "@xyflow/react";
import "./PillEdge.css";

/**
 * Curved bezier edge with a pill-shaped label rotated along the path tangent.
 * The angle is clamped to (-90deg, 90deg] so text never appears upside-down.
 */
export function PillEdge(props: EdgeProps) {
  const {
    id,
    sourceX,
    sourceY,
    targetX,
    targetY,
    sourcePosition,
    targetPosition,
    label,
    markerEnd,
    style,
  } = props;

  const [path, labelX, labelY] = getBezierPath({
    sourceX,
    sourceY,
    sourcePosition,
    targetX,
    targetY,
    targetPosition,
    curvature: 0.35,
  });

  const dx = targetX - sourceX;
  const dy = targetY - sourceY;
  let angle = (Math.atan2(dy, dx) * 180) / Math.PI;
  if (angle > 90) angle -= 180;
  if (angle < -90) angle += 180;

  return (
    <>
      <BaseEdge id={id} path={path} markerEnd={markerEnd} style={style} />
      {label && (
        <EdgeLabelRenderer>
          <div
            className="pill-edge__label"
            style={{
              transform: `translate(-50%, -50%) translate(${labelX}px, ${labelY}px) rotate(${angle}deg)`,
            }}
          >
            {String(label).toUpperCase()}
          </div>
        </EdgeLabelRenderer>
      )}
    </>
  );
}
