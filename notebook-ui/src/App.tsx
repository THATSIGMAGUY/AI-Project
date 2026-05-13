import { useEffect, useState } from "react";
import { NetworkScreen } from "@/screens/NetworkScreen";
import { Placeholder } from "@/screens/Placeholder";
import "./App.css";

type ScreenKey =
  | "network"
  | "timeline"
  | "matrix"
  | "data"
  | "patterns"
  | "charts";

type ThemeKey = "dark" | "light" | "present";

const SCREENS: { key: ScreenKey; label: string; blurb: string }[] = [
  { key: "network",  label: "Network",  blurb: "Link analysis of the case graph." },
  { key: "timeline", label: "Timeline", blurb: "Time-ordered view of events on the entities currently in scope." },
  { key: "matrix",   label: "Matrix",   blurb: "Entity-to-entity association matrix with co-occurrence counts." },
  { key: "data",     label: "Data",     blurb: "Tabular entity and edge editor with provenance fields." },
  { key: "patterns", label: "Patterns", blurb: "Auto-detected hubs, clusters, and bridges across the graph." },
  { key: "charts",   label: "Charts",   blurb: "Aggregate views: counts by type, confidence distribution, timeline density." },
];

export default function App() {
  const [screen, setScreen] = useState<ScreenKey>("network");
  const [theme, setTheme] = useState<ThemeKey>("present");

  useEffect(() => {
    const root = document.documentElement;
    root.classList.remove("theme-light", "theme-present");
    if (theme === "light") root.classList.add("theme-light");
    if (theme === "present") root.classList.add("theme-present");
  }, [theme]);

  return (
    <div className="app">
      <header className="app__header">
        <div className="app__brand">
          <span className="app__brand-dot" />
          <span className="app__brand-name">Analyst Notebook</span>
        </div>

        <nav className="app__nav">
          {SCREENS.map((s) => (
            <button
              key={s.key}
              className={`app__nav-item ${screen === s.key ? "is-active" : ""}`}
              onClick={() => setScreen(s.key)}
            >
              {s.label}
            </button>
          ))}
        </nav>

        <div className="app__theme">
          {(["dark", "light", "present"] as ThemeKey[]).map((t) => (
            <button
              key={t}
              className={`app__theme-btn ${theme === t ? "is-active" : ""}`}
              onClick={() => setTheme(t)}
              title={`${t} theme`}
            >
              {t}
            </button>
          ))}
        </div>
      </header>

      <main className="app__main">
        {screen === "network" ? (
          <NetworkScreen />
        ) : (
          <Placeholder
            title={SCREENS.find((s) => s.key === screen)!.label}
            blurb={SCREENS.find((s) => s.key === screen)!.blurb}
          />
        )}
      </main>
    </div>
  );
}
