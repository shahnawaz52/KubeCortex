# KubeCortex Context

## Status
This repo is still at the planning/bootstrap stage. The architecture below is the intended system design, not an implemented codebase yet.

## Product Summary
KubeCortex is a Kubernetes-native incident response system. It ingests alerts, launches AI-assisted investigation workflows, recommends safe remediation, and records every step for audit and replay.

Primary goal: reduce manual triage during Kubernetes incidents while keeping risky actions behind explicit approval.

## Core Workflow
1. Receive an alert from Alertmanager or a mock webhook.
2. Create an incident record.
3. Planner agent classifies the incident type.
4. Specialist agents gather evidence from logs, Kubernetes state, events, and optionally metrics.
5. Remediation agent proposes actions with risk levels.
6. Approval service decides whether an action can run automatically or needs human approval.
7. Executor performs approved actions.
8. Event store records the full incident timeline.

## MVP Scope
Build the smallest version that proves the architecture:

- One incident type: `CrashLoopBackOff`
- One alert source: webhook input
- Investigation tools: pod logs and Kubernetes state/events
- One remediation path: recommend restart or rollback
- Manual approval only
- Persistent audit trail in PostgreSQL
- Basic metrics and traces
- Local deployment on `kind`

Out of scope for MVP:

- Full UI
- Many incident types
- Risky auto-remediation
- Vector search / embeddings
- Multi-cluster support

## Planned Components
- Alert Ingestor: normalizes webhook payloads
- Incident Orchestrator: manages workflow state, retries, deduplication
- Planner Agent: classifies incidents and chooses next tools
- Specialist Agents: logs, cluster state, metrics, deployment context
- Remediation Agent: summarizes evidence and proposes actions
- Approval Service: gates risky changes
- Action Executor: runs approved Kubernetes actions
- Event Store: keeps alert, evidence, decisions, and results
- Observability Layer: logs, metrics, traces, token/cost tracking

## Suggested Stack
- API/service layer: FastAPI or Go
- Agent orchestration: Python
- Database: PostgreSQL
- Queue: Redis, NATS, or RabbitMQ
- Infra: Kubernetes, `kind`, Helm or Kustomize
- Observability: OpenTelemetry, Prometheus, Grafana, Loki/ELK, Tempo/Jaeger
- AI: OpenAI Responses API with tool calling and structured outputs

## Core Data / API Shape
Key entities:
- `Incident`
- `InvestigationStep`
- `RemediationPlan`
- `ApprovalRecord`
- `ExecutionRecord`

Expected endpoints:
- `POST /alerts`
- `GET /incidents`
- `GET /incidents/{id}`
- `POST /incidents/{id}/approve`
- `POST /incidents/{id}/reject`
- `POST /incidents/{id}/execute`
- `GET /health`
- `GET /metrics`

## Non-Functional Requirements
- Idempotent incident handling
- Durable workflow state
- Horizontal worker scaling
- Least-privilege RBAC
- Clear audit trail and replay support
- Human override for risky actions
- Bounded cost and tool depth

## Recommended Build Order
1. Alert ingestor
2. Incident schema/storage
3. Planner agent
4. Kubernetes state tool
5. Pod logs tool
6. Remediation planner
7. Approval API
8. Executor
9. Metrics/tracing
10. Kubernetes deployment
