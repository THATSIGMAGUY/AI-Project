import type { CaseGraph } from "@/domain/types";
import { EdgeType, EntityType } from "@/domain/types";

/**
 * Curated 6-node demo. Mirrors the Hume marketing layout (Person <-> Event,
 * with peripheral pill entities) so the network screen makes sense in a single
 * screenshot. Positions are hand-tuned, not algorithmic - per the Hume design
 * principle that analyst-arranged charts tell stories better than auto-layout.
 */

const osint = {
  source: "OSINT-feed-001",
  sourceGrade: "B2",
  analyst: "alice",
};
const caseFile = {
  source: "case-2026-0142",
  sourceGrade: "A1",
  analyst: "alice",
};

export const demoCase: CaseGraph = {
  entities: [
    {
      id: "person-suspect",
      type: EntityType.Person,
      label: "M. Larsson",
      provenance: caseFile,
      properties: { layout: { x: 80, y: 320, kind: "photo" } },
    },
    {
      id: "event-burglary",
      type: EntityType.Event,
      label: "Riverside burglary",
      validFrom: "2026-04-12T18:00:00",
      validTo: "2026-04-12T19:30:00",
      provenance: caseFile,
      properties: { layout: { x: 460, y: 60, kind: "photo" } },
    },
    {
      id: "asset-car",
      type: EntityType.Asset,
      label: "Car ABC-123",
      provenance: osint,
      properties: { layout: { x: 80, y: 80, kind: "pill" } },
    },
    {
      id: "location-house",
      type: EntityType.Location,
      label: "42 Riverside Ave",
      provenance: caseFile,
      properties: { layout: { x: 720, y: 360, kind: "pill" } },
    },
    {
      id: "asset-phone",
      type: EntityType.Asset,
      label: "Phone +66-2-555-0100",
      provenance: osint,
      properties: { layout: { x: 380, y: 560, kind: "photo" } },
    },
    {
      id: "asset-cell-tower",
      type: EntityType.Asset,
      label: "Cell tower BKK-7",
      provenance: osint,
      properties: { layout: { x: 760, y: 620, kind: "pill" } },
    },
  ],
  edges: [
    {
      id: "e1",
      type: EdgeType.MentionedIn,
      sourceId: "asset-car",
      targetId: "event-burglary",
      label: "involved",
      provenance: caseFile,
    },
    {
      id: "e2",
      type: EdgeType.ParticipatedIn,
      sourceId: "person-suspect",
      targetId: "event-burglary",
      label: "suspect",
      occurredAt: "2026-04-12T18:00:00",
      provenance: caseFile,
    },
    {
      id: "e3",
      type: EdgeType.LocatedAt,
      sourceId: "event-burglary",
      targetId: "location-house",
      label: "at",
      provenance: caseFile,
    },
    {
      id: "e4",
      type: EdgeType.LocatedAt,
      sourceId: "person-suspect",
      targetId: "location-house",
      label: "address",
      provenance: osint,
      confidence: 0.7,
    },
    {
      id: "e5",
      type: EdgeType.Owns,
      sourceId: "person-suspect",
      targetId: "asset-phone",
      label: "has phone",
      provenance: osint,
      confidence: 0.85,
    },
    {
      id: "e6",
      type: EdgeType.LocatedAt,
      sourceId: "asset-phone",
      targetId: "asset-cell-tower",
      label: "located",
      occurredAt: "2026-04-12T18:14:00",
      provenance: caseFile,
    },
  ],
};
