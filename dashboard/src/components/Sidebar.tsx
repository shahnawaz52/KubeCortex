import type { HealthStatus } from "../types";

interface SidebarProps {
  health: HealthStatus | null;
  activeView: string;
  onNavigate: (view: string) => void;
}

export default function Sidebar({ health, activeView, onNavigate }: SidebarProps) {
  const isHealthy = health?.status === "ok";

  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <div className="logo">
          <div className="logo-icon">
            <i className="fa-solid fa-shield-halved" />
          </div>
          <div className="logo-text">
            <h1>KubeCortex</h1>
            <span className="logo-subtitle">Incident Response</span>
          </div>
        </div>
      </div>

      <nav className="sidebar-nav">
        <button
          className={`nav-item ${activeView === "dashboard" ? "active" : ""}`}
          onClick={() => onNavigate("dashboard")}
        >
          <i className="fa-solid fa-gauge-high" />
          Dashboard
        </button>
        <button
          className={`nav-item ${activeView === "incidents" ? "active" : ""}`}
          onClick={() => onNavigate("incidents")}
        >
          <i className="fa-solid fa-triangle-exclamation" />
          Incidents
        </button>
      </nav>

      <div className="sidebar-footer">
        <div className="system-status">
          <div className={`status-dot ${isHealthy ? "healthy" : "unhealthy"}`} />
          <span>System {isHealthy ? "Operational" : "Degraded"}</span>
        </div>
      </div>
    </aside>
  );
}
