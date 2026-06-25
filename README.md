# KubeCortex

Kubernetes-native incident response system powered by agentic AI

KubeCortex ingests alerts, coordinates AI agents to investigate failures, recommends safe remediation, and records every decision in an auditable workflow

## How It Works

```
Alert → Classify → Investigate (logs + cluster state) → Recommend Fix → Human Approval → Execute
```

1. **Alert Ingestor** receives alerts from Alertmanager or webhook
2. **Planner Agent** classifies the incident type (e.g. `CrashLoopBackOff`)
3. **Specialist Tools** gather evidence — pod logs, Kubernetes state, events
4. **Remediation Planner** proposes actions with risk levels
5. **Approval Gate** blocks risky actions until a human approves
6. **Executor** runs approved actions against the cluster
7. **Event Store** records the full timeline for audit and replay

## Architecture

```
┌─────────────┐     ┌───────────┐     ┌──────────────────┐
│  Webhook /   │────▶│  FastAPI   │────▶│   PostgreSQL     │
│ Alertmanager │     │   API      │     │  (incidents,     │
└─────────────┘     └─────┬─────┘     │   steps, plans)  │
                          │           └──────────────────┘
                          ▼
                    ┌───────────┐
                    │   Redis   │
                    │  (queue)  │
                    └─────┬─────┘
                          │
                          ▼
                    ┌───────────┐     ┌──────────────────┐
                    │  Worker   │────▶│  Kubernetes API   │
                    │ (agents)  │     │  (logs, state)    │
                    └───────────┘     └──────────────────┘
```

**Key design properties:**
- Async queue-based processing with stateless workers
- Durable workflow state with retry and idempotency
- Alert deduplication
- Horizontal worker scaling
- Human-in-the-loop for risky operations

## Tech Stack

| Layer | Technology |
|---|---|
| API | Python, FastAPI |
| Database | PostgreSQL |
| Queue | Redis |
| AI | OpenAI Responses API (tool calling, structured outputs) |
| Infrastructure | Docker, Kubernetes, `kind` |
| Dashboard | React + TypeScript (Vite) |
| Observability | OpenTelemetry, Prometheus, Grafana |

## Getting Started

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and Docker Compose
- Git

### Run with Docker Compose

```bash
# Clone the repository
git clone https://github.com/shahnawaz52/KubeCortex.git
cd KubeCortex

# Copy environment config
cp .env.example .env

# Start all services (API, worker, PostgreSQL, Redis, dashboard)
docker compose up --build
```

This starts:

| Service | URL |
|---|---|
| API | http://localhost:8000 |
| Dashboard | http://localhost:5173 |
| Health check | http://localhost:8000/health |
| API Docs | http://localhost:8000/docs |

### Run Without Docker (manual setup)

```bash
# 1. Start PostgreSQL and Redis (must be running locally)
#    PostgreSQL on port 5433, Redis on port 6379

# 2. Set up Python environment
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env with your local database credentials

# 4. Start the API server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# 5. Start the worker (in a separate terminal)
python -m app.worker

# 6. Start the dashboard (in a separate terminal)
cd dashboard
npm install
npm run dev
```

## API Usage

### Send a test alert

```bash
curl -X POST http://localhost:8000/alerts \
  -H "Content-Type: application/json" \
  -d '{
    "source": "alertmanager",
    "alerts": [{
      "labels": {
        "alertname": "KubePodCrashLooping",
        "namespace": "production",
        "pod": "api-server-abc123"
      },
      "annotations": {
        "summary": "Pod api-server is crash looping"
      }
    }]
  }'
```

### View incidents

```bash
curl http://localhost:8000/incidents | python3 -m json.tool
```

### Get incident details

```bash
curl http://localhost:8000/incidents/1 | python3 -m json.tool
```

### Approve or reject remediation

```bash
# Approve
curl -X POST http://localhost:8000/incidents/1/approve

# Reject
curl -X POST http://localhost:8000/incidents/1/reject
```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/alerts` | Ingest an alert payload |
| `GET` | `/incidents` | List all incidents |
| `GET` | `/incidents/{id}` | Get incident with investigation steps |
| `POST` | `/incidents/{id}/approve` | Approve remediation plan |
| `POST` | `/incidents/{id}/reject` | Reject remediation plan |
| `GET` | `/health` | Service health check |

## Data Model

| Entity | Purpose |
|---|---|
| `Incident` | Alert record with status, severity, classification |
| `InvestigationStep` | Each tool call (logs, k8s state) with input/output |
| `RemediationPlan` | Proposed actions with risk levels and diagnosis |
| `ApprovalRecord` | Who approved/rejected and when |
| `ExecutionRecord` | What ran, result, before/after resource state |

## Project Structure

```
├── app/
│   ├── api/routes/        # FastAPI endpoints (alerts, incidents)
│   ├── core/              # Configuration
│   ├── db/                # SQLAlchemy models, session, migrations
│   ├── queue/             # Redis job queue
│   ├── schemas/           # Pydantic request/response models
│   ├── services/          # Business logic (incident processor)
│   ├── tools/             # Investigation tools (k8s state, pod logs)
│   ├── main.py            # FastAPI app entrypoint
│   └── worker.py          # Background worker process
├── dashboard/             # React + TypeScript frontend
├── tests/                 # Test suite
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

## Current Status

The MVP is under active development. Currently implemented:

- [x] Alert ingestion via webhook
- [x] Incident creation and persistence
- [x] Redis-backed async job queue
- [x] Background worker processing
- [x] Planner agent — incident classification
- [x] Kubernetes state tool (mock)
- [x] Pod logs tool (mock)
- [ ] Remediation planner
- [ ] Approval API
- [ ] Action executor
- [ ] Observability (metrics, traces)
- [ ] Kubernetes deployment (`kind`)

## License

MIT
