import { useState, useEffect, useCallback } from "react";
import type { Incident, HealthStatus } from "./types";
import { fetchIncidents, fetchHealth } from "./api";

const POLL_INTERVAL = 10_000;

export function useIncidents() {
  const [incidents, setIncidents] = useState<Incident[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const refresh = useCallback(async () => {
    try {
      const data = await fetchIncidents();
      setIncidents(data);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    refresh();
    const id = setInterval(refresh, POLL_INTERVAL);
    return () => clearInterval(id);
  }, [refresh]);

  return { incidents, loading, error, refresh };
}

export function useHealth() {
  const [health, setHealth] = useState<HealthStatus | null>(null);

  useEffect(() => {
    const check = async () => {
      try {
        const data = await fetchHealth();
        setHealth(data);
      } catch {
        setHealth({ status: "error" });
      }
    };
    check();
    const id = setInterval(check, POLL_INTERVAL);
    return () => clearInterval(id);
  }, []);

  return health;
}
