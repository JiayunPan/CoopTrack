# CoopTrack Testing Guide

This document records the repeatable checks used to validate the Phase 3 application.

## Clean Docker Build

Create `api/.env` from `api/.env.template`, replace both placeholders, and run:

```bash
docker compose down -v
docker compose up -d --build
docker compose ps
```

Expected services:

- `web-app` on port `8501`
- `web-api` on port `4000`
- `mysql_db` on host port `3200`

The `-v` option deletes the existing database volume. MySQL then executes
`database-files/01_schema.sql` followed by `02_sample_data.sql`.

## Health Checks

```bash
curl http://localhost:8501/_stcore/health
curl http://localhost:4000/students
```

Both requests should return HTTP `200`.

## Database Baseline

A clean initialization contains:

- **18 tables**
- **1,288 sample rows** across all project tables

## API Integration Test

With the three Docker services running, execute:

```bash
python3 api/tests/integration_test.py
```

The test exercises every route in the five CoopTrack Blueprints, including all
GET, POST, PUT, and DELETE endpoints. It also verifies representative `400` and
`404` responses and reads back database mutations.

The integration test intentionally creates temporary records. Run the clean Docker
build afterward when the original sample-data baseline is required.

## Streamlit Coverage

The application contains three simulated personas and nine feature pages:

| Persona | Dashboard | Feature pages |
| --- | --- | --- |
| Sofia | Student dashboard | Position Search, Application Tracker, Upcoming Deadlines |
| Marcus | Employer dashboard | Position Management, Applicant Review, Hiring Pipeline |
| Nikki | Admin dashboard | Report Review, Employer Verification, Student & Skill Management |

Every planned Flask route is called by at least one Streamlit dashboard or feature
page. Write operations display success/error feedback, and destructive operations
require an explicit confirmation when appropriate.

## Verified Baseline

The final local verification on August 12, 2026 produced:

- 29/29 planned API routes passing integration tests
- 12/12 persona dashboards and feature pages loading without runtime exceptions
- 18 database tables loaded automatically
- 1,288 sample rows loaded automatically
- HTTP 200 from both Flask and Streamlit health checks
