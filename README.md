# KubeCortex

Agentic AI incident commander for Kubernetes.

## Overview

KubeCortex is a distributed, Kubernetes-native incident response system that ingests alerts, coordinates AI agents to investigate failures, recommends safe remediation actions, and records every decision in an auditable workflow.

This project is intended to demonstrate three areas together:

- Distributed systems
- Agentic AI
- Kubernetes/platform engineering

The first version focuses on a narrow but realistic problem: handling Kubernetes incidents such as `CrashLoopBackOff` with AI-assisted triage and human-approved remediation.

## Problem Statement

Kubernetes incidents are noisy, repetitive, and slow to triage manually.

In a typical outage or alert scenario, engineers have to:

- inspect alerts
- switch between logs, dashboards, and `kubectl`
- check pod, deployment, and node state
- guess likely root cause
- decide whether a remediation action is safe
- document what happened afterward

This process is slow, inconsistent, and hard to audit.

KubeCortex solves this by turning incident response into a structured workflow:

1. Receive an alert
2. Create an incident record
3. Classify the incident with a planner agent
4. Collect evidence using specialist agents and tools
5. Propose remediation actions
6. Require approval for risky actions
7. Execute approved actions
8. Store the full timeline for audit and postmortem

## What Problem It Solves

KubeCortex is designed to reduce:

- alert fatigue
- manual triage effort
- slow time-to-diagnosis
- unsafe ad hoc remediation
- poor postmortem visibility

It gives operators a system that can gather evidence automatically, explain likely causes, suggest actions, and keep humans in control where necessary.

## Key Use Cases

### 1. CrashLoopBackOff Triage

When a pod keeps crashing, KubeCortex:

- receives the alert
- fetches recent pod logs
- checks events, restart counts, and deployment state
- identifies likely causes such as configuration failure or dependency issues
- recommends a safe action such as restart or rollback

### 2. Failed Rollout Investigation

When a deployment rollout gets stuck or fails, KubeCortex:

- checks deployment and ReplicaSet state
- inspects pod readiness and recent events
- identifies whether the issue is image, config, resource, or startup related
- suggests rollback or rollout pause

### 3. Node Pressure or Scheduling Failure

When a node is under pressure or workloads cannot schedule, KubeCortex:

- checks node conditions and cluster events
- identifies affected pods and workloads
- summarizes likely causes
- recommends actions such as scaling, draining, or workload movement

### 4. Faster On-Call Support

For junior engineers or overloaded on-call teams, KubeCortex acts as a guided incident assistant by collecting the first layer of evidence automatically.

### 5. Audit and Postmortem Support

Every alert, tool call, recommendation, approval, and execution result is stored so the incident can be replayed later.

## High-Level Architecture

### 1. Alert Ingestor

Receives alerts from Prometheus Alertmanager or mock webhook payloads.

Responsibilities:

- validate and normalize incoming alerts
- create incident records
- publish work to the orchestration layer

### 2. Incident Orchestrator

Coordinates the workflow for each incident.

Responsibilities:

- manage incident state
- trigger planner and specialist steps
- handle retries
- enforce idempotency
- route incidents through approval and execution stages

### 3. Planner Agent

The planner agent is the first decision-maker in the workflow.

Responsibilities:

- classify incident type
- decide which tools to invoke
- produce a structured investigation plan

### 4. Specialist Agents

Each specialist focuses on one source of truth.

- Logs Agent
  - fetches pod and container logs
  - identifies crash signatures and exceptions

- Kubernetes State Agent
  - checks pods, deployments, ReplicaSets, nodes, and events
  - identifies restarts, scheduling failures, rollout issues, and node problems

- Metrics Agent
  - queries Prometheus for latency, CPU, memory, and error rates
  - correlates alert symptoms with time-series behavior

### 5. Remediation Agent

Combines all collected evidence and proposes next actions.

Responsibilities:

- summarize likely root cause
- rank remediation options
- assign confidence and risk level

### 6. Approval Service

Prevents unsafe automation.

Responsibilities:

- block risky actions
- require explicit human approval
- record who approved or rejected a recommendation

### 7. Action Executor

Runs approved actions against Kubernetes.

Responsibilities:

- execute allowed operations
- record result and resource state
- keep execution constrained and auditable

### 8. Event Store and Audit Trail

Stores the full incident history:

- incoming alert
- planner output
- tool invocations
- tool results
- remediation proposal
- approval decisions
- execution outcome

### 9. Observability Layer

KubeCortex must also observe itself.

Core signals:

- logs
- metrics
- traces
- token and cost tracking per incident

## Distributed Systems Design

KubeCortex is intentionally structured as a distributed system.

Core design properties:

- asynchronous queue-based processing
- multiple stateless workers
- persistent workflow state
- retry and failure recovery
- deduplication of repeated alerts
- horizontal scaling during incident bursts
- eventual consistency between investigation steps
- explicit control over side effects

This is the main systems-design value of the project.

## Agentic AI Design

KubeCortex uses multiple bounded agents instead of one general prompt.

Agent roles:

- planner agent
- logs investigator
- cluster state investigator
- metrics investigator
- remediation planner
- optional incident summarizer

Why this approach:

- easier to reason about
- easier to test
- safer tool access boundaries
- clearer observability
- better debugging and evaluation

## Core Challenges

### 1. Unsafe or Hallucinated Remediation

Challenge:
An LLM may suggest commands that are technically valid but operationally dangerous.

Mitigation:

- allowlisted actions only
- strict schemas for tool arguments
- read-only defaults
- approval gate for risky changes

### 2. Incomplete or Noisy Evidence

Challenge:
Alerts often do not contain enough context for a confident diagnosis.

Mitigation:

- gather evidence from multiple sources
- support low-confidence outputs
- escalate uncertain cases to humans

### 3. Distributed Workflow Reliability

Challenge:
Workers can fail in the middle of an incident workflow.

Mitigation:

- durable workflow state
- retries with idempotency keys
- queue-backed step execution

### 4. Kubernetes Access and Security

Challenge:
Cluster permissions must be tightly controlled.

Mitigation:

- least-privilege RBAC
- namespace-scoped access where possible
- separation of read-only and write-capable execution

### 5. Cost Control

Challenge:
Multi-step agent workflows can become expensive.

Mitigation:

- bounded tool depth
- model selection per step
- caching repeated evidence
- token and cost telemetry

### 6. Human Trust

Challenge:
Operators will not trust a black-box remediation system.

Mitigation:

- transparent evidence summaries
- explicit approval flow
- complete audit trail

## MVP Scope

The MVP should prove the architecture without overbuilding.

Included in MVP:

- one incident type: `CrashLoopBackOff`
- one alert input path: webhook
- planner agent
- pod logs tool
- Kubernetes state/events tool
- remediation recommendation
- manual approval flow
- PostgreSQL audit trail
- basic metrics and traces
- local deployment on Kubernetes

Not included in MVP:

- full UI dashboard
- many incident types
- autonomous high-risk remediation
- vector search / embeddings
- multi-cluster support
- long-term learning loops

## Proposed Tech Stack

### Backend

- Python
- FastAPI
- PostgreSQL
- Redis, NATS, or RabbitMQ

### AI Layer

- OpenAI Responses API
- tool calling
- structured outputs

### Infrastructure

- Docker
- Kubernetes
- `kind` for local development
- AWS EKS for later cloud deployment
- Helm or Kustomize

### Observability

- OpenTelemetry
- Prometheus
- Grafana
- Loki or ELK
- Tempo or Jaeger

## Core Data Model

Primary entities:

- `Incident`
- `InvestigationStep`
- `RemediationPlan`
- `ApprovalRecord`
- `ExecutionRecord`

### Incident

- `incident_id`
- `source_alert_id`
- `status`
- `severity`
- `incident_type`
- `created_at`
- `updated_at`

### InvestigationStep

- `step_id`
- `incident_id`
- `agent_name`
- `tool_name`
- `input_payload`
- `output_payload`
- `status`
- `latency_ms`

### RemediationPlan

- `plan_id`
- `incident_id`
- `root_cause_summary`
- `recommended_action`
- `risk_level`
- `confidence_score`

### ApprovalRecord

- `approval_id`
- `incident_id`
- `requested_action`
- `approver`
- `decision`
- `timestamp`

### ExecutionRecord

- `execution_id`
- `incident_id`
- `action`
- `result`
- `resource_before`
- `resource_after`

## API Surface

Planned endpoints:

- `POST /alerts`
- `GET /incidents`
- `GET /incidents/{id}`
- `POST /incidents/{id}/approve`
- `POST /incidents/{id}/reject`
- `POST /incidents/{id}/execute`
- `GET /health`
- `GET /metrics`

## Example Incident Flow

### Scenario: CrashLoopBackOff

1. Alert is received at `POST /alerts`
2. Incident record is created
3. Planner agent classifies it as a pod crash incident
4. Logs agent fetches recent container logs
5. Kubernetes state agent fetches events, restart counts, and deployment status
6. Remediation agent proposes restart or rollback
7. Approval service blocks risky actions until approved
8. Executor runs the approved action
9. Event store records the full timeline

## Expected Outcomes

By the end of the project, KubeCortex should:

- reduce time to first diagnosis
- reduce repetitive manual triage
- provide explainable AI-assisted incident handling
- demonstrate distributed worker orchestration
- show safe Kubernetes remediation design
- provide a reference architecture for agentic Kubernetes operations

## Success Metrics

- mean time to first diagnosis
- mean time to recommended action
- approval-to-execution latency
- root cause classification accuracy
- manual triage steps avoided
- cost per incident
- failed tool-call rate

## Recommended Build Order

1. Alert ingestor
2. Incident schema and persistence
3. Planner agent
4. Kubernetes state tool
5. Pod logs tool
6. Remediation recommender
7. Approval API
8. Action executor
9. Metrics and tracing
10. Kubernetes deployment

## Repository Status

This repository is currently in the planning/bootstrap stage. The architecture described here is the target design, not a finished implementation yet.

