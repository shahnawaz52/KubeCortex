import type { Incident } from "../types";

interface StatsBarProps {
  incidents: Incident[];
}

interface StatCard {
  label: string;
  value: number;
  accent: string;
  icon: string;
}

export default function StatsBar({ incidents }: StatsBarProps) {
  const total = incidents.length;
  const active = incidents.filter((i) =>
    ["received", "processing"].includes(i.status)
  ).length;
  const classified = incidents.filter((i) => i.status === "classified").length;
  const failed = incidents.filter((i) =>
    ["failed", "queued_failed"].includes(i.status)
  ).length;

  const cards: StatCard[] = [
    { label: "Total Incidents", value: total, accent: "var(--accent-blue)", icon: "fa-solid fa-chart-column" },
    { label: "Active", value: active, accent: "var(--accent-amber)", icon: "fa-solid fa-bolt" },
    { label: "Classified", value: classified, accent: "var(--accent-green)", icon: "fa-solid fa-circle-check" },
    { label: "Failed", value: failed, accent: "var(--accent-red)", icon: "fa-solid fa-circle-xmark" },
  ];

  return (
    <div className="stats-bar">
      {cards.map((card) => (
        <div
          key={card.label}
          className="stat-card"
          style={{ "--card-accent": card.accent } as React.CSSProperties}
        >
          <div className="stat-icon">
            <i className={card.icon} />
          </div>
          <div className="stat-content">
            <span className="stat-value">{card.value}</span>
            <span className="stat-label">{card.label}</span>
          </div>
        </div>
      ))}
    </div>
  );
}
