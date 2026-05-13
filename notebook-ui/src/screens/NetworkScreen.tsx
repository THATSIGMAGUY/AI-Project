import { ReactFlowProvider } from "@xyflow/react";
import { GraphCanvas } from "@/graph/GraphCanvas";
import { demoCase } from "@/data/demoCase";

export function NetworkScreen() {
  return (
    <div style={{ height: "100%", width: "100%" }}>
      <ReactFlowProvider>
        <GraphCanvas graph={demoCase} />
      </ReactFlowProvider>
    </div>
  );
}
