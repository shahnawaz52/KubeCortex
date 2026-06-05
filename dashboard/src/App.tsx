import { useState, useEffect } from "react";
import Sidebar from "./components/Sidebar";
import StatsBar from "./components/StatsBar";
import IncidentTable from "./components/IncidentTable";
import IncidentDetail from "./components/IncidentDetail";
import { useIncidents, useHealth } from "./hooks";
import type { Incident } from "./types";
import "./App.css";

export default function App() {
  const { incidents, loading } = useIncidents();
  const health = useHealth();
  const [activeView, setActiveView] = useState("dashboard");
  const [selectedIncident, setSelectedIncident] = useState<Incident | null>(null);
  const [theme, setTheme] = useState(() =>
    localStorage.getItem("theme") || "dark"
  );

  useEffect(() => {
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem("theme", theme);
  }, [theme]);

  const toggleTheme = () => setTheme(theme === "dark" ? "light" : "dark");

  const handleSelect = (id: number) => {
    const inc = incidents.find((i) => i.id === id) ?? null;
    setSelectedIncident(inc);
  };

  return (
    <div className="app-layout">
      <Sidebar
        health={health}
        activeView={activeView}
        onNavigate={setActiveView}
      />

      <main className="main-content">
        <header className="page-header">
          <div>
            <h2 className="page-title">
              {activeView === "dashboard" ? "Dashboard" : "Incidents"}
            </h2>
            <p className="page-subtitle">
              {activeView === "dashboard"
                ? "Real-time incident overview"
                : "All incidents from alert ingestion"}
            </p>
          </div>
          <div className="header-actions">
            <button className="theme-toggle" onClick={toggleTheme} aria-label="Toggle theme">
              <i className={`fa-solid ${theme === "dark" ? "fa-sun" : "fa-moon"}`} />
            </button>
            <span className="live-badge">
              <span className="live-dot" />
              Live
            </span>
          </div>
        </header>

        <StatsBar incidents={incidents} />

        <section className="content-section">
          <div className="section-header">
            <h3>Recent Incidents</h3>
            <span className="count-badge">{incidents.length}</span>
          </div>
          <IncidentTable
            incidents={incidents}
            selectedId={selectedIncident?.id ?? null}
            onSelect={handleSelect}
            loading={loading}
          />
        </section>
      </main>

      {selectedIncident && (
        <IncidentDetail
          incident={selectedIncident}
          onClose={() => setSelectedIncident(null)}
        />
      )}
    </div>
  );
}
