/**
 * Domain types - mirror the Python notebook/schema.py.
 *
 * Keep these in lock-step with the Python side: when one changes, both change.
 * That's the contract that lets the front-end and the orchestrator's notebook
 * module talk to each other (over JSON, REST, or a future GraphQL layer).
 */

export const EntityType = {
  Person: "Person",
  Organization: "Organization",
  Location: "Location",
  Event: "Event",
  Document: "Document",
  Asset: "Asset",
  Communication: "Communication",
  Transaction: "Transaction",
} as const;
export type EntityType = (typeof EntityType)[keyof typeof EntityType];

export const EdgeType = {
  Knows: "KNOWS",
  MemberOf: "MEMBER_OF",
  Owns: "OWNS",
  LocatedAt: "LOCATED_AT",
  ParticipatedIn: "PARTICIPATED_IN",
  CommunicatedWith: "COMMUNICATED_WITH",
  TransferredTo: "TRANSFERRED_TO",
  MentionedIn: "MENTIONED_IN",
  DerivedFrom: "DERIVED_FROM",
} as const;
export type EdgeType = (typeof EdgeType)[keyof typeof EdgeType];

export interface Provenance {
  source: string;
  ingestedAt?: string;
  /** NATO Admiralty: letter A-F (source reliability) + digit 1-6 (info credibility). */
  sourceGrade?: string;
  sourceUri?: string;
  analyst?: string;
  notes?: string;
}

export interface Entity {
  id: string;
  type: EntityType;
  label: string;
  /** Optional image (data URI or URL). When present, renders as photo node. */
  imageUrl?: string;
  aliases?: string[];
  properties?: Record<string, unknown>;
  validFrom?: string;
  validTo?: string;
  confidence?: number;
  provenance?: Provenance;
}

export interface Edge {
  id: string;
  type: EdgeType;
  sourceId: string;
  targetId: string;
  /** Human-readable label rendered on the edge. Defaults to type. */
  label?: string;
  occurredAt?: string;
  confidence?: number;
  properties?: Record<string, unknown>;
  provenance?: Provenance;
}

export interface CaseGraph {
  entities: Entity[];
  edges: Edge[];
}
