"""
Analyst Notebook - Workspace

Hume 3.0-style Workspace: a scoped investigation environment with its own
entity scope, annotations, saved views, and an append-only audit log. A
GraphStore is the shared source of truth; Workspaces are lenses on top.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Any, Optional

from .graph_store import GraphStore


@dataclass
class Annotation:
    """An analyst's note attached to an entity or edge."""

    target_id: str                           # entity_id or edge_id
    target_kind: str                         # "entity" | "edge"
    text: str
    author: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    tags: list[str] = field(default_factory=list)


@dataclass
class SavedView:
    """A reproducible view: the entity set + display hints (timeline/map/graph)."""

    name: str
    entity_ids: list[str]
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    layout: str = "graph"                    # "graph" | "timeline" | "map" | "table"
    filters: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())


@dataclass
class AuditEntry:
    """Append-only log entry. Every write to the workspace produces one."""

    action: str                              # e.g. "add_entity", "annotate"
    actor: str
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    details: dict[str, Any] = field(default_factory=dict)


class Workspace:
    """A scoped investigation over a shared GraphStore."""

    def __init__(
        self,
        name: str,
        graph: GraphStore,
        owner: str,
        id: Optional[str] = None,
    ) -> None:
        self.id = id or str(uuid.uuid4())
        self.name = name
        self.owner = owner
        self.graph = graph
        self.created_at = datetime.utcnow().isoformat()

        # Workspace scope: which entities are "in" this investigation.
        # Empty set = full graph in scope.
        self.scope: set[str] = set()

        self.annotations: dict[str, Annotation] = {}
        self.saved_views: dict[str, SavedView] = {}
        self.audit: list[AuditEntry] = []

    # ---- scope --------------------------------------------------------

    def add_to_scope(self, entity_id: str, actor: Optional[str] = None) -> None:
        if self.graph.get_entity(entity_id) is None:
            raise KeyError(f"entity {entity_id} not in graph")
        self.scope.add(entity_id)
        self._log("add_to_scope", actor, {"entity_id": entity_id})

    def expand_scope(self, hops: int = 1, actor: Optional[str] = None) -> int:
        """Pull in N-hop neighbors of everything currently in scope."""
        added = 0
        for seed in list(self.scope):
            for nid in self.graph.ego_subgraph(seed, hops=hops):
                if nid not in self.scope:
                    self.scope.add(nid)
                    added += 1
        self._log("expand_scope", actor, {"hops": hops, "added": added})
        return added

    def in_scope(self, entity_id: str) -> bool:
        return not self.scope or entity_id in self.scope

    # ---- annotations --------------------------------------------------

    def annotate(
        self,
        target_id: str,
        text: str,
        author: str,
        target_kind: str = "entity",
        tags: Optional[list[str]] = None,
    ) -> Annotation:
        if target_kind == "entity" and self.graph.get_entity(target_id) is None:
            raise KeyError(f"entity {target_id} not found")
        if target_kind == "edge" and self.graph.get_edge(target_id) is None:
            raise KeyError(f"edge {target_id} not found")
        ann = Annotation(
            target_id=target_id,
            target_kind=target_kind,
            text=text,
            author=author,
            tags=tags or [],
        )
        self.annotations[ann.id] = ann
        self._log("annotate", author, {"target_id": target_id, "annotation_id": ann.id})
        return ann

    def annotations_for(self, target_id: str) -> list[Annotation]:
        return [a for a in self.annotations.values() if a.target_id == target_id]

    # ---- saved views --------------------------------------------------

    def save_view(
        self,
        name: str,
        entity_ids: list[str],
        layout: str = "graph",
        filters: Optional[dict[str, Any]] = None,
        actor: Optional[str] = None,
    ) -> SavedView:
        view = SavedView(
            name=name,
            entity_ids=list(entity_ids),
            layout=layout,
            filters=filters or {},
        )
        self.saved_views[view.id] = view
        self._log("save_view", actor, {"view_id": view.id, "name": name})
        return view

    # ---- audit --------------------------------------------------------

    def _log(self, action: str, actor: Optional[str], details: dict[str, Any]) -> None:
        self.audit.append(
            AuditEntry(action=action, actor=actor or self.owner, details=details)
        )

    # ---- persistence --------------------------------------------------

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "owner": self.owner,
            "created_at": self.created_at,
            "scope": sorted(self.scope),
            "annotations": [asdict(a) for a in self.annotations.values()],
            "saved_views": [asdict(v) for v in self.saved_views.values()],
            "audit": [asdict(e) for e in self.audit],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any], graph: GraphStore) -> "Workspace":
        ws = cls(name=data["name"], graph=graph, owner=data["owner"], id=data["id"])
        ws.created_at = data.get("created_at", ws.created_at)
        ws.scope = set(data.get("scope", []))
        for a in data.get("annotations", []):
            ws.annotations[a["id"]] = Annotation(**a)
        for v in data.get("saved_views", []):
            ws.saved_views[v["id"]] = SavedView(**v)
        for e in data.get("audit", []):
            ws.audit.append(AuditEntry(**e))
        return ws
