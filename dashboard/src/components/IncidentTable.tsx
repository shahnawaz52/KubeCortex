import type { Incident } from "../types";

interface IncidentTableProps {
  incidents: Incident[];
  selectedId: number | null;
  onSelect: (id: number) => void;
  loading: boolean;
}

function statusClass(status: string): string {
  switch (status) {
    case "received":
      return "badge-blue";
    case "processing":
      return "badge-amber";
    case "classified":
      return "badge-green";
    case "failed":
    case "queued_failed":
      return "badge-red";
    default:
      return "badge-gray";
  }
}

function timeAgo(dateStr: string): string {
  const now = Date.now();
  const then = new Date(dateStr).getTime();
  const seconds = Math.floor((now - then) / 1000);

  if (seconds < 60) return `${seconds}s ago`;
  const minutes = Math.floor(seconds / 60);
  if (minutes < 60) return `${minutes}m ago`;
  const hours = Math.floor(minutes / 60);
  if (hours < 24) return `${hours}h ago`;
  const days = Math.floor(hours / 24);
  return `${days}d ago`;
}

export default function IncidentTable({
  incidents,
  selectedId,
  onSelect,
  loading,
}: IncidentTableProps) {
  if (loading) {
    return (
      <div className="table-empty">
        <div className="loader" />
        <p>Loading incidents...</p>
      </div>
    );
  }

  if (incidents.length === 0) {
    return (
      <div className="table-empty">
        <div className="empty-icon">
          <i className="fa-solid fa-brain" />
        </div>
        <h3>No incidents yet</h3>
        <p>When alerts arrive, they'll appear here.</p>
        <code className="hint-code">
          curl -X POST http://localhost:8000/alerts ...
        </code>
      </div>
    );
  }

  return (
    <div className="table-container">
      <table className="incident-table" id="incident-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Status</th>
            <th>Type</th>
            <th>Summary</th>
            <th>Source</th>
            <th>Steps</th>
            <th>Created</th>
          </tr>
        </thead>
        <tbody>
          {incidents.map((inc) => (
            <tr
              key={inc.id}
              className={`table-row ${selectedId === inc.id ? "selected" : ""}`}
              onClick={() => onSelect(inc.id)}
            >
              <td className="cell-id">#{inc.id}</td>
              <td>
                <span className={`badge ${statusClass(inc.status)}`}>
                  {inc.status}
                </span>
              </td>
              <td className="cell-type">{inc.incident_type ?? "—"}</td>
              <td className="cell-summary">
                {inc.summary
                  ? inc.summary.length > 60
                    ? `${inc.summary.slice(0, 60)}…`
                    : inc.summary
                  : "—"}
              </td>
              <td className="cell-source">{inc.source}</td>
              <td className="cell-steps">{inc.steps.length}</td>
              <td className="cell-time">{timeAgo(inc.created_at)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
