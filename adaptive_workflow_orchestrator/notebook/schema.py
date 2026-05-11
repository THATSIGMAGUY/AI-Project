"""
Analyst Notebook - Schema

Minimal entity/edge ontology inspired by GraphAware Hume and IBM i2 Analyst's
Notebook. Designed to be a starting point: extend EntityType / EdgeType freely.

Design choices:
- Provenance is mandatory on every node and edge. Without it, analyst output
  cannot be defended downstream.
- Time is modeled as (valid_from, valid_to) on entities and (occurred_at) on
  edges. Both are optional - much intelligence data is undated.
- Confidence is a float in [0, 1]. Source reliability and information credibility
  (the NATO Admiralty scale A1-F6) can be encoded in Provenance.source_grade.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from typing import Any, Optional


class EntityType(str, Enum):
    """Core entity types. Extend as the domain requires."""

    PERSON = "Person"
    ORGANIZATION = "Organization"
    LOCATION = "Location"
    EVENT = "Event"
    DOCUMENT = "Document"
    ASSET = "Asset"            # vehicle, device, account, weapon, etc.
    COMMUNICATION = "Communication"   # phone number, email address, handle
    TRANSACTION = "Transaction"


class EdgeType(str, Enum):
    """Core relationship types. Direction matters: source -> target."""

    KNOWS = "KNOWS"
    MEMBER_OF = "MEMBER_OF"
    OWNS = "OWNS"
    LOCATED_AT = "LOCATED_AT"
    PARTICIPATED_IN = "PARTICIPATED_IN"
    COMMUNICATED_WITH = "COMMUNICATED_WITH"
    TRANSFERRED_TO = "TRANSFERRED_TO"
    MENTIONED_IN = "MENTIONED_IN"
    DERIVED_FROM = "DERIVED_FROM"


@dataclass
class Provenance:
    """
    Where a node or edge came from. Attached to every Entity and Edge.

    source_grade follows the NATO Admiralty 2-character convention:
      letter A-F = source reliability (A = completely reliable)
      digit  1-6 = information credibility (1 = confirmed)
    e.g. "B2" = usually reliable source, probably true.
    """

    source: str                              # human-readable source name
    ingested_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    source_grade: Optional[str] = None       # e.g. "A1", "C3", "F6"
    source_uri: Optional[str] = None         # URL, file path, case ID
    analyst: Optional[str] = None            # who ingested / asserted this
    notes: Optional[str] = None


@dataclass
class Entity:
    """A node in the knowledge graph."""

    type: EntityType
    label: str                               # display name
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    properties: dict[str, Any] = field(default_factory=dict)
    aliases: list[str] = field(default_factory=list)
    valid_from: Optional[str] = None         # ISO-8601
    valid_to: Optional[str] = None
    confidence: float = 1.0
    provenance: Optional[Provenance] = None

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["type"] = self.type.value
        return d

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "Entity":
        prov = d.get("provenance")
        return cls(
            type=EntityType(d["type"]),
            label=d["label"],
            id=d.get("id", str(uuid.uuid4())),
            properties=d.get("properties", {}),
            aliases=d.get("aliases", []),
            valid_from=d.get("valid_from"),
            valid_to=d.get("valid_to"),
            confidence=d.get("confidence", 1.0),
            provenance=Provenance(**prov) if prov else None,
        )


@dataclass
class Edge:
    """A directed, typed relationship between two entities."""

    type: EdgeType
    source_id: str
    target_id: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    properties: dict[str, Any] = field(default_factory=dict)
    occurred_at: Optional[str] = None        # ISO-8601 for time-stamped events
    confidence: float = 1.0
    provenance: Optional[Provenance] = None

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["type"] = self.type.value
        return d

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "Edge":
        prov = d.get("provenance")
        return cls(
            type=EdgeType(d["type"]),
            source_id=d["source_id"],
            target_id=d["target_id"],
            id=d.get("id", str(uuid.uuid4())),
            properties=d.get("properties", {}),
            occurred_at=d.get("occurred_at"),
            confidence=d.get("confidence", 1.0),
            provenance=Provenance(**prov) if prov else None,
        )
