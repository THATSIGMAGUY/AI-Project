# Analyst's Notebook — Project state (v3 scaffold checkpoint, 2026-05-22)

## TL;DR

- v3 scaffold ทำเสร็จในสายเดียวกับ CLAUDE.md sec 5 — 5 atomic commits + tag `v2.0.0-archived`
- Build pipeline (Vite + IIFE-equivalent single HTML) ทดสอบแล้วเปิด `file://` ได้, type-check clean, output 1.3 KB
- GitHub repo https://github.com/THATSIGMAGUY/analyst-notebook ยังว่าง — ต้อง push ครั้งแรกจากเครื่องของคุณเอง (sandbox ของ Claude Code ไม่มี credential)
- โค้ดทุกไฟล์ที่ scaffold ไว้อยู่ใน "Scaffold files" ข้างล่าง — Claude session ถัดไปเอาไปใช้ต่อได้

## i2 Compliance — สถานะปัจจุบัน (เทียบ CLAUDE.md sec 9)

| ข้อ | ผ่าน? | หมายเหตุ |
|---|---|---|
| 3.1 `ENTITY_SHAPES` tokens | ✅ | ใน `src/types.ts` |
| 3.2 `LINE_STYLE_DASH` tokens | ✅ | ใน `src/types.ts` |
| 3.3 `RELIABILITY_COLORS` tokens | ✅ | ใน `src/types.ts` |
| 3.4 `sourceRef` required ใน `Link` interface | ✅ | mandatory field |
| 3.7 `confirmed` + `ViewMode` enum | ✅ | type พร้อม UI ยังไม่ landing |
| 3.8 `isPrimaryTarget` field | ✅ | optional field บน `Entity` |
| 3.10 `caseId` on `Entity`, `caseTitle` on `Case` | ✅ |  |
| Build เปิด `file://` ได้, ไม่มี `type="module"` | ✅ | smoke test ผ่าน |
| File size ≤ 5 MB | ✅ | scaffold = 1.3 KB |
| `npm run typecheck` clean | ✅ |  |
| TH/EN locales ครบทุก key ใน skeleton | ✅ |  |
| 3.5 Association Matrix view | ❌ | feature commit ถัดไป |
| 3.6 4 Layout modes | ❌ | feature commit ถัดไป |
| 3.7 Working ↔ Presentation toggle UI | ❌ | type พร้อม UI ยังไม่ทำ |
| 3.8 Primary Target halo visual | ❌ |  |
| 3.9 Hypothesis amber banner | ❌ |  |
| 3.11 Visual Legend แสดงตลอด | ❌ |  |
| 3.12 Sample NAR-2026-001 dataset | ❌ | ยังไม่ครบ hierarchy |

## Planned feature branches (จาก `v3/scaffold`)

- `v3/feature-sample-data` — `src/data/sample-NAR-2026-001.ts` ครบ hierarchy/safe houses/money/burners (sec 3.12)
- `v3/feature-graph-view` — Cytoscape canvas + shapes + line styles + reliability + Primary Target halo (3.1, 3.2, 3.3, 3.8)
- `v3/feature-legend` — Visual Legend แสดงตลอด (3.11)
- `v3/feature-layout-modes` — 4 layouts (3.6)
- `v3/feature-view-mode-toggle` — Working ↔ Presentation (3.7)
- `v3/feature-hypothesis-banner` — amber banner (3.9)
- `v3/feature-matrix-view` — Association Matrix (3.5)
- `v3/feature-case-id-chip` + Top bar — (3.10) + i18n toggle

## Architectural decisions ที่ตัดสินแล้ว

- **Stack**: Vite + TypeScript (vanilla, no framework) + `vite-plugin-singlefile` + custom plugin strip `type="module"`
- **Graph engine**: Cytoscape.js (`^3.30.2`) — map กับ i2 ครบ 4 layouts, free PNG/JSON export
- **Build target**: ES2018, IIFE-equivalent (single inlined `<script>` no `type=module`)
- **Deploy target**: `C:\Users\0123\OneDrive\Documents\Claude\Projects\Analyst's Notebook\analyst-notebook.html` (เป็น manual copy ถ้า build host ไม่ใช่ Windows)
- **No backend** — localStorage + JSON import/export เท่านั้น
- **TH default, EN secondary** — locale toggle บน top bar

## Scaffold files

ทุกไฟล์ข้างล่างคือ source ที่ committed ในสาขา `v3/scaffold` ของ sandbox Claude session ถัดไปสร้างไฟล์เหล่านี้ตามนี้ได้เลย (หรือเรียก artifact เขียนใหม่)

### `package.json`

```json
{
  "name": "analyst-notebook",
  "private": true,
  "version": "3.0.0-scaffold",
  "type": "module",
  "description": "Link-analysis tool inspired by IBM i2 Analyst's Notebook, for Thai law-enforcement use. Ships as a single HTML file that opens directly via file://.",
  "scripts": {
    "dev": "vite",
    "build": "vite build && node scripts/build-and-deploy.cjs build",
    "deploy": "vite build && node scripts/build-and-deploy.cjs deploy",
    "test": "vitest run --passWithNoTests",
    "typecheck": "tsc --noEmit",
    "check": "npm run typecheck"
  },
  "dependencies": {
    "cytoscape": "^3.30.2"
  },
  "devDependencies": {
    "@types/cytoscape": "^3.21.7",
    "@types/node": "^22.9.0",
    "typescript": "^5.6.3",
    "vite": "^5.4.10",
    "vite-plugin-singlefile": "^2.0.3",
    "vitest": "^2.1.4"
  }
}
```

### `tsconfig.json`

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "module": "ESNext",
    "lib": ["ES2022", "DOM", "DOM.Iterable"],
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "moduleDetection": "force",
    "noEmit": true,
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "exactOptionalPropertyTypes": false,
    "baseUrl": ".",
    "paths": { "@/*": ["src/*"] },
    "types": ["node", "vitest"]
  },
  "include": ["src", "scripts", "vite.config.ts"]
}
```

### `vite.config.ts`

```ts
import { defineConfig, type Plugin } from "vite";
import { viteSingleFile } from "vite-plugin-singlefile";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));

function stripScriptTypeModule(): Plugin {
  return {
    name: "analyst-notebook:strip-script-type-module",
    enforce: "post",
    apply: "build",
    transformIndexHtml: {
      order: "post",
      handler(html) {
        return html
          .replace(/\stype=["']module["']/g, "")
          .replace(/\scrossorigin(=["'][^"']*["'])?/g, "");
      },
    },
  };
}

export default defineConfig({
  plugins: [viteSingleFile(), stripScriptTypeModule()],
  resolve: { alias: { "@": path.resolve(here, "src") } },
  server: { port: 5173, host: true },
  build: {
    target: "es2018",
    minify: "esbuild",
    cssCodeSplit: false,
    assetsInlineLimit: 100_000_000,
    rollupOptions: {
      output: { inlineDynamicImports: true, manualChunks: undefined },
    },
    outDir: "dist",
    emptyOutDir: true,
  },
});
```

### `index.html`

```html
<!doctype html>
<html lang="th">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Analyst's Notebook</title>
  </head>
  <body>
    <div id="app"></div>
    <script type="module" src="/src/main.ts"></script>
  </body>
</html>
```

### `src/main.ts`

```ts
const app = document.getElementById("app");
if (app) {
  app.innerHTML = `
    <main style="font-family: system-ui, sans-serif; padding: 32px; max-width: 720px; margin: 0 auto;">
      <h1>Analyst's Notebook</h1>
      <p>v3 scaffold — UI lands in subsequent commits.</p>
      <p>See <code>CLAUDE.md</code> sec 3 for the 12 IBM i2 standards this build will implement.</p>
    </main>
  `;
}
```

### `src/types.ts`

```ts
// 3.1 ENTITY_SHAPES
export const EntityType = {
  Person: "Person", Organization: "Organization", Document: "Document",
  Location: "Location", Asset: "Asset", Vehicle: "Vehicle",
  Communication: "Communication", Event: "Event",
} as const;
export type EntityType = (typeof EntityType)[keyof typeof EntityType];

export type EntityShape = "circle" | "rectangle" | "triangle" | "diamond" | "hexagon" | "octagon";
export const ENTITY_SHAPES: Record<EntityType, EntityShape> = {
  [EntityType.Person]: "circle",
  [EntityType.Organization]: "rectangle",
  [EntityType.Document]: "rectangle",
  [EntityType.Location]: "triangle",
  [EntityType.Asset]: "diamond",
  [EntityType.Vehicle]: "hexagon",
  [EntityType.Communication]: "hexagon",
  [EntityType.Event]: "octagon",
};

// 3.2 LINE_STYLE_DASH
export const LinkStyle = { Solid: "solid", Dashed: "dashed", Dotted: "dotted" } as const;
export type LinkStyle = (typeof LinkStyle)[keyof typeof LinkStyle];
export const LINE_STYLE_DASH: Record<LinkStyle, string> = {
  [LinkStyle.Solid]: "none",
  [LinkStyle.Dashed]: "8 4",
  [LinkStyle.Dotted]: "2 4",
};

// 3.3 RELIABILITY_COLORS
export const Reliability = {
  Surveillance: "surveillance", Documents: "documents", Informant: "informant",
  ConfirmedFact: "confirmed_fact", Unverified: "unverified",
} as const;
export type Reliability = (typeof Reliability)[keyof typeof Reliability];
export const RELIABILITY_COLORS: Record<Reliability, string> = {
  [Reliability.Surveillance]: "#16a34a",
  [Reliability.Documents]: "#2563eb",
  [Reliability.Informant]: "#dc2626",
  [Reliability.ConfirmedFact]: "#374151",
  [Reliability.Unverified]: "#9ca3af",
};

// Domain interfaces
export type AdmiraltyGrade = `${"A"|"B"|"C"|"D"|"E"|"F"}${1|2|3|4|5|6}`;

export interface Entity {
  id: string;
  type: EntityType;
  label: string;
  caseId: string;
  isPrimaryTarget?: boolean;
  hierarchyLevel?: number;
  properties?: Record<string, unknown>;
  earliestEventAt?: string;
  latestEventAt?: string;
}

export interface Link {
  id: string;
  sourceId: string;
  targetId: string;
  label?: string;
  lineStyle: LinkStyle;
  reliability: Reliability;
  sourceRef: string;
  confirmed: boolean;
  admiraltyGrade?: AdmiraltyGrade;
  occurredAt?: string;
  properties?: Record<string, unknown>;
}

export interface Case {
  caseId: string;
  caseTitle: string;
  hypothesis: string;
  entities: Entity[];
  links: Link[];
  createdAt?: string;
  updatedAt?: string;
  analyst?: string;
}

export const ViewMode = { Working: "working", Presentation: "presentation" } as const;
export type ViewMode = (typeof ViewMode)[keyof typeof ViewMode];

export const LayoutMode = {
  Force: "force", Hierarchy: "hierarchy", Temporal: "temporal", Centrality: "centrality",
} as const;
export type LayoutMode = (typeof LayoutMode)[keyof typeof LayoutMode];
```

### `src/i18n.ts`

```ts
import { EntityType, LayoutMode, LinkStyle, Reliability, ViewMode } from "./types";

export const Locale = { TH: "th", EN: "en" } as const;
export type Locale = (typeof Locale)[keyof typeof Locale];
export const DEFAULT_LOCALE: Locale = Locale.TH;

export interface Translations {
  app: { title: string; tagline: string };
  topbar: { workingMode: string; presentationMode: string; toggleLocale: string; caseChipPrefix: string };
  hypothesis: { bannerPrefix: string; placeholder: string; editAction: string };
  legend: { title: string; shapesHeading: string; reliabilityHeading: string; lineStyleHeading: string; sourceRefNote: string };
  layout: { heading: string; modes: Record<LayoutMode, string> };
  viewMode: Record<ViewMode, string>;
  entityType: Record<EntityType, string>;
  reliability: Record<Reliability, string>;
  linkStyle: Record<LinkStyle, string>;
  primaryTarget: { label: string; abbreviated: string };
  inspector: { emptySelection: string; sourceRefLabel: string; confidenceLabel: string; confirmedLabel: string; unconfirmedLabel: string };
}

const th: Translations = {
  app: { title: "Analyst's Notebook", tagline: "เครื่องมือวิเคราะห์ความเชื่อมโยงสำหรับงานบังคับใช้กฎหมาย" },
  topbar: { workingMode: "โหมดทำงาน", presentationMode: "โหมดนำเสนอ", toggleLocale: "EN", caseChipPrefix: "คดี" },
  hypothesis: { bannerPrefix: "สมมติฐานคดี", placeholder: "ระบุสมมติฐานหลักของคดี (กดเพื่อแก้ไข)", editAction: "แก้ไขสมมติฐาน" },
  legend: {
    title: "คำอธิบายสัญลักษณ์",
    shapesHeading: "รูปทรงเอนทิตี",
    reliabilityHeading: "ความน่าเชื่อถือของหลักฐาน",
    lineStyleHeading: "ประเภทเส้นความสัมพันธ์",
    sourceRefNote: "ป้ายอ้างอิงพยานหลักฐานแสดงเฉพาะในโหมดทำงาน",
  },
  layout: {
    heading: "รูปแบบการจัดวาง",
    modes: {
      [LayoutMode.Force]: "แรงดึงดูด (Force)",
      [LayoutMode.Hierarchy]: "ลำดับชั้น (Hierarchy)",
      [LayoutMode.Temporal]: "ตามเวลา (Temporal)",
      [LayoutMode.Centrality]: "ความสำคัญกลาง (Centrality)",
    },
  },
  viewMode: { [ViewMode.Working]: "โหมดทำงาน", [ViewMode.Presentation]: "โหมดนำเสนอ" },
  entityType: {
    [EntityType.Person]: "บุคคล",
    [EntityType.Organization]: "องค์กร",
    [EntityType.Document]: "เอกสาร",
    [EntityType.Location]: "สถานที่",
    [EntityType.Asset]: "ทรัพย์สิน/การเงิน",
    [EntityType.Vehicle]: "ยานพาหนะ",
    [EntityType.Communication]: "การสื่อสาร",
    [EntityType.Event]: "เหตุการณ์",
  },
  reliability: {
    [Reliability.Surveillance]: "จากการสืบสวน",
    [Reliability.Documents]: "จากเอกสาร",
    [Reliability.Informant]: "จากสายลับ",
    [Reliability.ConfirmedFact]: "ข้อเท็จจริงยืนยันแล้ว",
    [Reliability.Unverified]: "ยังไม่ได้พิสูจน์",
  },
  linkStyle: {
    [LinkStyle.Solid]: "ยืนยันแล้ว",
    [LinkStyle.Dashed]: "ต้องสงสัย",
    [LinkStyle.Dotted]: "ทางอ้อม / อนุมาน",
  },
  primaryTarget: { label: "เป้าหมายหลัก", abbreviated: "★ PRIMARY TARGET" },
  inspector: {
    emptySelection: "เลือกเอนทิตีหรือความสัมพันธ์เพื่อดูรายละเอียด",
    sourceRefLabel: "อ้างอิงหลักฐาน",
    confidenceLabel: "ระดับความเชื่อมั่น",
    confirmedLabel: "ยืนยันแล้ว",
    unconfirmedLabel: "ยังไม่ยืนยัน",
  },
};

const en: Translations = {
  app: { title: "Analyst's Notebook", tagline: "Link-analysis tool for law-enforcement use" },
  topbar: { workingMode: "Working mode", presentationMode: "Presentation mode", toggleLocale: "ไทย", caseChipPrefix: "Case" },
  hypothesis: { bannerPrefix: "Case hypothesis", placeholder: "State the case hypothesis (click to edit)", editAction: "Edit hypothesis" },
  legend: {
    title: "Legend",
    shapesHeading: "Entity shapes",
    reliabilityHeading: "Evidence reliability",
    lineStyleHeading: "Link styles",
    sourceRefNote: "Source-reference labels show only in Working mode",
  },
  layout: {
    heading: "Layout",
    modes: {
      [LayoutMode.Force]: "Force",
      [LayoutMode.Hierarchy]: "Hierarchy",
      [LayoutMode.Temporal]: "Temporal",
      [LayoutMode.Centrality]: "Centrality",
    },
  },
  viewMode: { [ViewMode.Working]: "Working", [ViewMode.Presentation]: "Presentation" },
  entityType: {
    [EntityType.Person]: "Person",
    [EntityType.Organization]: "Organization",
    [EntityType.Document]: "Document",
    [EntityType.Location]: "Location",
    [EntityType.Asset]: "Asset / Financial",
    [EntityType.Vehicle]: "Vehicle",
    [EntityType.Communication]: "Communication",
    [EntityType.Event]: "Event",
  },
  reliability: {
    [Reliability.Surveillance]: "Surveillance",
    [Reliability.Documents]: "Documents",
    [Reliability.Informant]: "Informant",
    [Reliability.ConfirmedFact]: "Confirmed fact",
    [Reliability.Unverified]: "Unverified",
  },
  linkStyle: {
    [LinkStyle.Solid]: "Confirmed",
    [LinkStyle.Dashed]: "Suspected",
    [LinkStyle.Dotted]: "Indirect / Inferred",
  },
  primaryTarget: { label: "Primary target", abbreviated: "★ PRIMARY TARGET" },
  inspector: {
    emptySelection: "Select an entity or link to inspect details",
    sourceRefLabel: "Source reference",
    confidenceLabel: "Confidence",
    confirmedLabel: "Confirmed",
    unconfirmedLabel: "Unconfirmed",
  },
};

export const translations: Record<Locale, Translations> = { th, en };

let currentLocale: Locale = DEFAULT_LOCALE;
export function getLocale(): Locale { return currentLocale; }
export function setLocale(next: Locale): void { currentLocale = next; }
export function t(): Translations { return translations[currentLocale]; }
```

### `scripts/build-and-deploy.cjs`

```cjs
"use strict";
const fs = require("node:fs");
const path = require("node:path");
const os = require("node:os");

const ROOT = path.resolve(__dirname, "..");
const DIST = path.join(ROOT, "dist");
const SRC_NAME = "index.html";
const OUT_NAME = "analyst-notebook.html";
const DEPLOY_WIN = String.raw`C:\Users\0123\OneDrive\Documents\Claude\Projects\Analyst's Notebook\analyst-notebook.html`;
const SIZE_LIMIT_MB = 5;

const mode = process.argv[2] || "build";
if (mode !== "build" && mode !== "deploy") {
  console.error(`Unknown mode "${mode}". Use: build | deploy`);
  process.exit(1);
}

function renameOutput() {
  const src = path.join(DIST, SRC_NAME);
  const out = path.join(DIST, OUT_NAME);
  if (!fs.existsSync(src)) {
    console.error(`Build output not found: ${src}`);
    process.exit(1);
  }
  if (fs.existsSync(out)) fs.unlinkSync(out);
  fs.renameSync(src, out);
  return out;
}

function reportSize(out) {
  const bytes = fs.statSync(out).size;
  const mb = bytes / 1024 / 1024;
  const status = mb > SIZE_LIMIT_MB ? "OVER LIMIT" : "ok";
  console.log(`output: ${path.relative(ROOT, out)}  ${(bytes/1024).toFixed(1)} KB  (${mb.toFixed(2)} MB, limit ${SIZE_LIMIT_MB} MB) - ${status}`);
  if (mb > SIZE_LIMIT_MB) process.exit(2);
}

function assertFileProtocolSafe(out) {
  const html = fs.readFileSync(out, "utf8");
  const m = html.match(/<script[^>]*\stype=["']module["'][^>]*>/i);
  if (m) {
    console.error(`Refusing to publish: <script type="module"> would break file:// on Chromium.`);
    process.exit(3);
  }
}

function deploy(out) {
  if (process.platform !== "win32") {
    console.log(`deploy: non-Windows host (${process.platform}, ${os.release()})`);
    console.log(`artifact: ${out}`);
    console.log(`copy manually to: ${DEPLOY_WIN}`);
    return;
  }
  fs.mkdirSync(path.dirname(DEPLOY_WIN), { recursive: true });
  fs.copyFileSync(out, DEPLOY_WIN);
  console.log(`deploy: copied to ${DEPLOY_WIN}`);
}

const out = renameOutput();
assertFileProtocolSafe(out);
reportSize(out);
if (mode === "deploy") deploy(out);
```

### `.gitignore`

```gitignore
dist/
node_modules/
.vite/
*.tsbuildinfo
vite.config.js
vite.config.d.ts
coverage/
.DS_Store
Thumbs.db
*.log

# PII patterns (CLAUDE.md §8)
case-*.json
case-*.csv
evidence/
real-*.json
*.private.*
*.confidential.*
private/
classified/
NAR-real-*
AMLO-real-*
TM30-real-*
SAR-real-*
```

### `README.md`

```md
# Analyst's Notebook

เครื่องมือ link analysis แบบ IBM i2 สำหรับงานบังคับใช้กฎหมายไทย ส่งเป็นไฟล์ HTML เดี่ยว เปิดด้วย file:// ได้

ดูรายละเอียดทั้งหมดใน CLAUDE.md — single source of truth ของโปรเจกต์ ต้องอ่านก่อนแก้โค้ดทุกครั้ง

## Quick start

npm install
npm run dev
npm run build
npm run deploy
npm run typecheck

Private repo เสมอ ห้าม commit ข้อมูลคดีจริง ใช้ sample ปลอม NAR-2026-001 เท่านั้น
```

## First message — paste นี้ในการคุยกับ Claude บน Claude.ai ครั้งถัดไป

```
สวัสดี Claude. กำลังทำต่อโปรเจกต์ Analyst's Notebook v3

อ่านในลำดับนี้:
1. CLAUDE.md (single source of truth, มาตรฐาน i2 12 ข้อใน sec 3)
2. PROJECT_STATE.md (สถานะปัจจุบัน + scaffold files + planned feature branches)
3. archive/v2/analyst-notebook.html (golden reference v2 ถ้าแนบไว้)

จากนั้น:
- ยืนยันว่าอ่านครบ
- สรุปมาตรฐาน i2 12 ข้อกลับให้ผม + สถานะ checklist sec 9 ว่าผ่าน/ยังไม่ผ่านข้อไหน
- ถามว่าให้เริ่มงาน feature ไหนก่อน (ตาม planned feature branches ใน PROJECT_STATE.md)

ห้าม:
- เริ่มเขียนโค้ดก่อนผมยืนยัน
- เปลี่ยน build pipeline ที่ทำให้เปิด file:// ไม่ได้
- แก้/ลบไฟล์ใน archive/v2/
- ทำให้มาตรฐาน i2 ข้อใดข้อหนึ่ง regress โดยไม่ flag ก่อน
```
