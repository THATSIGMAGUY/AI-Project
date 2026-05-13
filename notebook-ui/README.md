# notebook-ui

React + TypeScript + Vite front-end for the Analyst Notebook. Mirrors the
domain types in `../adaptive_workflow_orchestrator/notebook/schema.py` so the
two sides can speak the same schema when the backend bridge lands.

## Run

```bash
npm install
npm run dev      # http://localhost:5173
npm run build    # type-check + production bundle into dist/
npm run typecheck
```

## Layout

```
src/
  theme/      design tokens + global styles (dark / light / present modes)
  domain/     Entity / Edge / Provenance types mirroring the Python schema
  graph/      React Flow wrapper, custom node/edge components
    nodes/    EntityPillNode (capsule) and PhotoNode (image card)
    edges/    PillEdge (curved bezier with rotated pill label)
  data/       curated demo case
  screens/    six top-level screens; only Network is implemented in pass 1
```

## Pass 1 scope

- Network screen with a hand-positioned 6-node demo case
- Hume-inspired theme: pill labels with type-color dots, curved edges,
  pastel "present" mode for screenshots
- The other five screens (Timeline, Matrix, Data, Patterns, Charts) are
  stubbed with placeholder cards and wired into the top nav

## Not yet (planned passes)

- Persistence (Dexie + File System Access API)
- Entity/edge editor on the Data screen
- Timeline, Matrix, Pattern Detection, Charts implementations
- STIX 2.1 import/export
- AI smart import (Claude/OpenAI)
- Bridge to the Python notebook module over HTTP
