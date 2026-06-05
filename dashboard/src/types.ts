export interface InvestigationStep {
  id: number;
  incident_id: number;
  step_type: string;
  status: string;
  input_payload: Record<string, unknown>;
  output_payload: Record<string, unknown>;
  created_at: string;
}

export interface Incident {
  id: number;
  status: string;
  source: string;
  raw_alert: Record<string, unknown>;
  incident_type: string | null;
  summary: string | null;
  created_at: string;
  updated_at: string;
  steps: InvestigationStep[];
}

export interface HealthStatus {
  status: string;
}
