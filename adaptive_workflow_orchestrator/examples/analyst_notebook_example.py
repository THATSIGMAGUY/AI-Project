"""
Analyst Notebook - end-to-end example.

Builds a tiny investigation: two people, one organization, a meeting event,
a vehicle, and the relationships between them. Opens a workspace, expands
scope, annotates a finding, saves a view, and writes the whole notebook to
JSON.

Run:
    python3 examples/analyst_notebook_example.py
"""

import os
import sys
import tempfile

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from notebook import (
    EdgeType,
    EntityType,
    Notebook,
    Provenance,
)


def build_case() -> Notebook:
    nb = Notebook()

    osint = Provenance(source="OSINT-feed-001", source_grade="B2", analyst="alice")
    case_file = Provenance(source="case-2026-0142", source_grade="A1", analyst="alice")

    alice = nb.add_entity(EntityType.PERSON, "Alice Carter", osint, aliases=["A. Carter"])
    bob = nb.add_entity(EntityType.PERSON, "Bob Lin", osint)
    acme = nb.add_entity(EntityType.ORGANIZATION, "ACME Holdings", case_file)
    meeting = nb.add_entity(
        EntityType.EVENT, "Riverside meeting", case_file,
        valid_from="2026-04-12T18:00:00",
        valid_to="2026-04-12T19:30:00",
    )
    plate = nb.add_entity(EntityType.ASSET, "Vehicle ABC-123", case_file)

    nb.add_edge(EdgeType.MEMBER_OF, alice, acme, case_file)
    nb.add_edge(EdgeType.OWNS, bob, plate, osint, confidence=0.7)
    nb.add_edge(EdgeType.PARTICIPATED_IN, alice, meeting, case_file,
                occurred_at="2026-04-12T18:00:00")
    nb.add_edge(EdgeType.PARTICIPATED_IN, bob, meeting, case_file,
                occurred_at="2026-04-12T18:05:00")
    nb.add_edge(EdgeType.KNOWS, alice, bob, osint, confidence=0.85)

    return nb


def main() -> None:
    nb = build_case()
    print(f"Graph: {nb.graph.stats()}")

    ws = nb.open_workspace("Op. Riverside", owner="alice")
    alice = nb.graph.find_by_label("Alice Carter")[0]
    ws.add_to_scope(alice.id)
    added = ws.expand_scope(hops=2)
    print(f"Scope after 2-hop expansion: {len(ws.scope)} entities (+{added})")

    bob = nb.graph.find_by_label("Bob Lin")[0]
    path = nb.graph.shortest_path(alice.id, bob.id)
    print(f"Shortest path alice -> bob: {len(path) if path else 'none'} nodes")

    ws.annotate(
        target_id=bob.id,
        text="Owner-of-vehicle link is single-source — needs corroboration.",
        author="alice",
        tags=["needs-corroboration", "vehicle"],
    )
    ws.save_view("All participants of Riverside meeting",
                 entity_ids=list(ws.scope), layout="timeline")

    print(f"Annotations: {len(ws.annotations)}")
    print(f"Saved views: {len(ws.saved_views)}")
    print(f"Audit entries: {len(ws.audit)}")

    out = os.path.join(tempfile.gettempdir(), "notebook_demo.json")
    nb.save(out)
    print(f"Saved notebook to: {out}")

    reloaded = Notebook.load(out)
    print(f"Reloaded: {reloaded.graph.stats()}, "
          f"{len(reloaded.workspaces)} workspace(s)")


if __name__ == "__main__":
    main()
