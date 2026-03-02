# Exchange Ops Automation Service

Internal backend service for automating operational tasks used by crypto exchanges, with a strong focus on reliability, idempotency, and ops maturity.

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

FastAPI → Redis → Celery Worker → Job Logic → Database

APScheduler is optionally used for simple deployments or local testing.

---

## Project Structure

app/
├── api/
├── core/
├── db/
├── jobs/
├── tasks/
├── celery_app.py
├── main.py

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

## Running Locally

1. Setup environment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

2. Run API
uvicorn app.main:app --reload

3. Run Celery Worker (Windows)
celery -A app.celery_app.celery_app worker --loglevel=info --pool=solo

---

## Documentation

See docs/full-architecture.md for full architecture details.

---

## Summary

A reliability-focused internal ops service designed to demonstrate production-grade backend engineering.
