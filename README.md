# Exchange Ops Automation Service

Backend infrastructure service for automating operational workflows within cryptocurrency exchanges.

The system demonstrates reliability-focused backend patterns including idempotent job execution, distributed task processing, and operational health monitoring.

This project intentionally avoids:
- Blockchain node integration
- Trading bots or DeFi logic
- User authentication
- UI concerns

The goal is to demonstrate how real exchanges automate and monitor critical internal jobs.

---

## What This Service Does

### 1. Daily Reconciliation Automation
- Runs a daily reconciliation job
- Aggregates transaction statistics
- Persists immutable daily reports
- Detects anomalies (e.g. zero transactions)
- Fully idempotent (safe to retry or re-run)

### 2. Operational Health Endpoint
GET /api/health/

Exposes:
- Database connectivity
- Last successful job execution
- Whether today’s reconciliation exists
- Detection of missed daily runs

### 3. Dual Execution Modes

| Mode | Scheduler | Execution |
|----|----|----|
| Simple | APScheduler | In-process |
| Scaled | Disabled | Celery + Redis |

---

## Architecture Overview

````
FastAPI API
     ↓
Scheduler / Manual Trigger
     ↓
Redis (Task Queue)
     ↓
Celery Worker
     ↓
Operational Job Logic
     ↓
Database.
````

---

## Project Structure

````
app/
├── api/
├── core/
├── db/
├── jobs/
├── tasks/
├── celery_app.py
├── main.py
````

---

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- APScheduler
- Celery
- Redis
- SQLite / PostgreSQL

---

## Testing Strategy

This project includes a **real, meaningful automated test suite** designed to validate reliability and operational correctness - not just happy paths.

### What Is Tested

#### 1. Health Endpoint Contract
- Health endpoint returns HTTP 200
- Response schema matches the documented API contract
- Database connectivity is correctly reported
- Missed daily job detection behaves as expected

#### 2. Missed Job Detection Logic
- Detects when the daily reconciliation did not run within the expected window
- Validates time-based operational signals (critical for ops tooling)

#### 3. Reconciliation Job Idempotency
- Ensures the daily reconciliation job can be safely re-run
- Prevents duplicate daily reports for the same date
- Mirrors real exchange retry and failure-recovery behavior

#### 4. Celery Task Execution
- Confirms Celery task correctly triggers reconciliation logic
- Ensures business logic and task execution remain decoupled

---

## Why These Tests Matter

These tests intentionally:
- Caught real production bugs during development
- Forced deterministic health logic (no hidden exception paths)
- Validated API contracts between services
- Proved idempotency guarantees

This reflects how internal reliability services are tested at real exchanges.

---

## Running Tests

````bash
pytest -v
````

All tests run against an isolated in-memory database and do not require Redis or Celery workers to be running.

---

## Running Locally

1. Setup environment
````
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
````

2. Run API
````
uvicorn app.main:app --reload
````

3. Run Celery Worker (Windows)
````
celery -A app.celery_app.celery_app worker --loglevel=info --pool=solo
````

---

## Documentation

See docs/full-architecture.md for full architecture details.

---

## Summary

A reliability-focused internal ops service designed to demonstrate:

- Production-grade backend structure

- Safe, idempotent job execution

- Health monitoring and failure detection

- Test-driven hardening of operational logic

This project mirrors how real crypto exchanges build and validate internal automation systems.
