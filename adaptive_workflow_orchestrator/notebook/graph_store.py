"""
Analyst Notebook - Graph store

Stdlib-only in-memory graph store with JSON persistence. Sufficient for
single-user notebook use up to ~10^5 entities. For larger / multi-user / live
ingestion deployments, swap this for a Neo4j or Kuzu backend (the public API
on Notebook is designed to be backend-agnostic).
"""

from __future__ import annotations

import json
from collections import defaultdict, deque
from pathlib import Path
from typing import Iterable, Iterator, Optional

from .schema import Edge, EdgeType, Entity, EntityType


class GraphStore:
    """In-memory directed multigraph with typed edges."""

    def __init__(self) -> None:
        self._entities: dict[str, Entity] = {}
        self._edges: dict[str, Edge] = {}
        # adjacency: entity_id -> set[edge_id]
        self._out: dict[str, set[str]] = defaultdict(set)
        self._in: dict[str, set[str]] = defaultdict(set)

    # ---- mutation -----------------------------------------------------

    def add_entity(self, entity: Entity) -> Entity:
        self._entities[entity.id] = entity
        return entity

    def add_edge(self, edge: Edge) -> Edge:
        if edge.source_id not in self._entities:
            raise KeyError(f"source entity {edge.source_id} not found")
        if edge.target_id not in self._entities:
            raise KeyError(f"target entity {edge.target_id} not found")
        self._edges[edge.id] = edge
        self._out[edge.source_id].add(edge.id)
        self._in[edge.target_id].add(edge.id)
        return edge

    def remove_entity(self, entity_id: str) -> None:
        for edge_id in list(self._out[entity_id] | self._in[entity_id]):
            self.remove_edge(edge_id)
        self._entities.pop(entity_id, None)
        self._out.pop(entity_id, None)
        self._in.pop(entity_id, None)

    def remove_edge(self, edge_id: str) -> None:
        edge = self._edges.pop(edge_id, None)
        if edge is None:
            return
        self._out[edge.source_id].discard(edge_id)
        self._in[edge.target_id].discard(edge_id)

    # ---- lookup -------------------------------------------------------

    def get_entity(self, entity_id: str) -> Optional[Entity]:
        return self._entities.get(entity_id)

    def get_edge(self, edge_id: str) -> Optional[Edge]:
        return self._edges.get(edge_id)

    def entities(self, type: Optional[EntityType] = None) -> Iterator[Entity]:
        for e in self._entities.values():
            if type is None or e.type == type:
                yield e

    def edges(self, type: Optional[EdgeType] = None) -> Iterator[Edge]:
        for e in self._edges.values():
            if type is None or e.type == type:
                yield e

    def find_by_label(self, label: str, fuzzy: bool = False) -> list[Entity]:
        """Exact match by default. fuzzy=True does case-insensitive substring."""
        if fuzzy:
            needle = label.lower()
            return [
                e for e in self._entities.values()
                if needle in e.label.lower()
                or any(needle in a.lower() for a in e.aliases)
            ]
        return [
            e for e in self._entities.values()
            if e.label == label or label in e.aliases
        ]

    # ---- traversal ----------------------------------------------------

    def neighbors(
        self,
        entity_id: str,
        edge_type: Optional[EdgeType] = None,
        direction: str = "both",
    ) -> list[tuple[Edge, Entity]]:
        """Return (edge, neighbor_entity) pairs. direction in {out, in, both}."""
        if direction not in ("out", "in", "both"):
            raise ValueError("direction must be 'out', 'in', or 'both'")
        edge_ids: Iterable[str] = ()
        if direction in ("out", "both"):
            edge_ids = list(self._out[entity_id])
        if direction in ("in", "both"):
            edge_ids = list(edge_ids) + list(self._in[entity_id])

        results: list[tuple[Edge, Entity]] = []
        for eid in edge_ids:
            edge = self._edges[eid]
            if edge_type is not None and edge.type != edge_type:
                continue
            other_id = edge.target_id if edge.source_id == entity_id else edge.source_id
            other = self._entities.get(other_id)
            if other is not None:
                results.append((edge, other))
        return results

    def shortest_path(
        self,
        source_id: str,
        target_id: str,
        max_hops: int = 6,
    ) -> Optional[list[str]]:
        """Undirected BFS. Returns entity-id path or None."""
        if source_id == target_id:
            return [source_id]
        seen = {source_id}
        queue: deque[tuple[str, list[str]]] = deque([(source_id, [source_id])])
        while queue:
            node, path = queue.popleft()
            if len(path) > max_hops:
                continue
            for _edge, neighbor in self.neighbors(node, direction="both"):
                if neighbor.id in seen:
                    continue
                new_path = path + [neighbor.id]
                if neighbor.id == target_id:
                    return new_path
                seen.add(neighbor.id)
                queue.append((neighbor.id, new_path))
        return None

    def ego_subgraph(self, entity_id: str, hops: int = 1) -> set[str]:
        """Entity ids within `hops` of the seed (inclusive)."""
        seen = {entity_id}
        frontier = {entity_id}
        for _ in range(hops):
            next_frontier: set[str] = set()
            for nid in frontier:
                for _edge, nb in self.neighbors(nid, direction="both"):
                    if nb.id not in seen:
                        next_frontier.add(nb.id)
                        seen.add(nb.id)
            frontier = next_frontier
            if not frontier:
                break
        return seen

    # ---- persistence --------------------------------------------------

    def to_dict(self) -> dict:
        return {
            "entities": [e.to_dict() for e in self._entities.values()],
            "edges": [e.to_dict() for e in self._edges.values()],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "GraphStore":
        g = cls()
        for ed in data.get("entities", []):
            g.add_entity(Entity.from_dict(ed))
        for ed in data.get("edges", []):
            g.add_edge(Edge.from_dict(ed))
        return g

    def save(self, path: str | Path) -> None:
        Path(path).write_text(json.dumps(self.to_dict(), indent=2))

    @classmethod
    def load(cls, path: str | Path) -> "GraphStore":
        return cls.from_dict(json.loads(Path(path).read_text()))

    # ---- summary ------------------------------------------------------

    def stats(self) -> dict[str, int]:
        return {
            "entities": len(self._entities),
            "edges": len(self._edges),
        }
