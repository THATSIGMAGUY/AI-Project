import "./Placeholder.css";

export interface PlaceholderProps {
  title: string;
  blurb: string;
}

export function Placeholder({ title, blurb }: PlaceholderProps) {
  return (
    <div className="placeholder">
      <div className="placeholder__inner">
        <h1>{title}</h1>
        <p>{blurb}</p>
        <span className="placeholder__chip">Coming in a later pass</span>
      </div>
    </div>
  );
}
