import { useState } from "react";
import type { Incident } from "../types";

interface IncidentDetailProps {
  incident: Incident;
  onClose: () => void;
}

export default function IncidentDetail({ incident, onClose }: IncidentDetailProps) {
  const [showRaw, setShowRaw] = useState(false);

  return (
    <div className="detail-overlay" onClick={onClose}>
      <div className="detail-panel" onClick={(e) => e.stopPropagation()}>
        <div className="detail-header">
          <div>
            <h2>Incident #{incident.id}</h2>
            <span className={`badge badge-lg ${badgeClass(incident.status)}`}>
              {incident.status}
            </span>
          </div>
          <button className="close-btn" onClick={onClose} aria-label="Close">
            <i className="fa-solid fa-xmark" />
          </button>
        </div>

        <div className="detail-body">
          <div className="detail-grid">
            <div className="detail-field">
              <label>Type</label>
              <span>{incident.incident_type ?? "Unclassified"}</span>
            </div>
            <div className="detail-field">
              <label>Source</label>
              <span>{incident.source}</span>
            </div>
            <div className="detail-field">
              <label>Created</label>
              <span>{new Date(incident.created_at).toLocaleString()}</span>
            </div>
            <div className="detail-field">
              <label>Updated</label>
              <span>{new Date(incident.updated_at).toLocaleString()}</span>
            </div>
          </div>

          {incident.summary && (
            <div className="detail-section">
              <h3>Summary</h3>
              <p className="detail-summary">{incident.summary}</p>
            </div>
          )}

          {incident.steps.length > 0 && (
            <div className="detail-section">
              <h3>Investigation Timeline</h3>
              <div className="timeline">
                {incident.steps.map((step) => (
                  <div key={step.id} className="timeline-item">
                    <div className="timeline-dot" />
                    <div className="timeline-content">
                      <div className="timeline-header">
                        <span className="timeline-type">{step.step_type}</span>
                        <span className={`badge badge-sm ${badgeClass(step.status)}`}>
                          {step.status}
                        </span>
                      </div>
                      {step.output_payload && Object.keys(step.output_payload).length > 0 && (
                        <pre className="timeline-output">
                          {JSON.stringify(step.output_payload, null, 2)}
                        </pre>
                      )}
                      <span className="timeline-time">
                        {new Date(step.created_at).toLocaleString()}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          <div className="detail-section">
            <button
              className="toggle-raw-btn"
              onClick={() => setShowRaw(!showRaw)}
            >
              {showRaw ? "Hide" : "Show"} Raw Alert
              <i
                className="fa-solid fa-chevron-down"
                style={{
                  transform: showRaw ? "rotate(180deg)" : "rotate(0deg)",
                  transition: "transform 0.2s",
                }}
              />
            </button>
            {showRaw && (
              <pre className="raw-json">
                {JSON.stringify(incident.raw_alert, null, 2)}
              </pre>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

function badgeClass(status: string): string {
  switch (status) {
    case "received":
      return "badge-blue";
    case "processing":
      return "badge-amber";
    case "classified":
    case "completed":
      return "badge-green";
    case "failed":
    case "queued_failed":
      return "badge-red";
    default:
      return "badge-gray";
  }
}
