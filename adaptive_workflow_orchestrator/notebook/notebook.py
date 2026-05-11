"""
Analyst Notebook - top-level facade

Ties together the GraphStore (shared truth) and Workspaces (scoped
investigations). This is the surface the rest of the orchestrator imports.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from .graph_store import GraphStore
from .schema import Edge, EdgeType, Entity, EntityType, Provenance
from .workspace import Workspace


class Notebook:
    """Analyst notebook: one graph, many workspaces."""

    def __init__(self, graph: Optional[GraphStore] = None) -> None:
        self.graph = graph or GraphStore()
        self.workspaces: dict[str, Workspace] = {}

    # ---- entity/edge convenience -------------------------------------

    def add_entity(
        self,
        type: EntityType,
        label: str,
        provenance: Provenance,
        **kwargs,
    ) -> Entity:
        entity = Entity(type=type, label=label, provenance=provenance, **kwargs)
        return self.graph.add_entity(entity)

    def add_edge(
        self,
        type: EdgeType,
        source: Entity | str,
        target: Entity | str,
        provenance: Provenance,
        **kwargs,
    ) -> Edge:
        source_id = source.id if isinstance(source, Entity) else source
        target_id = target.id if isinstance(target, Entity) else target
        edge = Edge(
            type=type,
            source_id=source_id,
            target_id=target_id,
            provenance=provenance,
            **kwargs,
        )
        return self.graph.add_edge(edge)

    # ---- workspaces ---------------------------------------------------

    def open_workspace(self, name: str, owner: str) -> Workspace:
        ws = Workspace(name=name, graph=self.graph, owner=owner)
        self.workspaces[ws.id] = ws
        return ws

    def get_workspace(self, workspace_id: str) -> Optional[Workspace]:
        return self.workspaces.get(workspace_id)

    # ---- persistence --------------------------------------------------

    def save(self, path: str | Path) -> None:
        data = {
            "graph": self.graph.to_dict(),
            "workspaces": [w.to_dict() for w in self.workspaces.values()],
        }
        Path(path).write_text(json.dumps(data, indent=2))

    @classmethod
    def load(cls, path: str | Path) -> "Notebook":
        data = json.loads(Path(path).read_text())
        nb = cls(graph=GraphStore.from_dict(data["graph"]))
        for wdata in data.get("workspaces", []):
            ws = Workspace.from_dict(wdata, nb.graph)
            nb.workspaces[ws.id] = ws
        return nb
