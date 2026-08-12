# CoopTrack

CoopTrack is a three-tier database application for students,
employers, and system administrators. It centralizes position discovery,
application tracking, recruiting workflows, employer verification, and platform
moderation in one database-backed application.

This project was developed for **CS 3200: Database Design, Summer B 2026**.

## Team Members

- Erica Cheng
- Jiayun Pan

## User Personas

CoopTrack's Phase 3 implementation focuses on three personas:

- **Sofia — Student:** discovers positions, saves opportunities, tracks applications,
  and monitors deadlines.
- **Marcus — Employer:** manages position listings, reviews applicants, and tracks the
  hiring pipeline.
- **Nikki — System Administrator:** verifies employers, reviews reported positions,
  manages students, and maintains skill data.

The landing page uses buttons to simulate signing in as each persona. CoopTrack does
not implement account creation or real authentication.

## Technology Stack

- **Frontend:** Streamlit
- **REST API:** Flask with Blueprints
- **Database:** MySQL 9
- **Infrastructure:** Docker and Docker Compose
- **Languages:** Python and SQL

## Architecture

```text
Streamlit UI  <---- HTTP/JSON ---->  Flask REST API  <---- SQL ---->  MySQL
   :8501                              :4000                          :3200
```

The application is divided into three Docker services:

| Service | Container | Purpose | Host URL/Port |
| --- | --- | --- | --- |
| `app` | `web-app` | Streamlit frontend | <http://localhost:8501> |
| `api` | `web-api` | Flask REST API | <http://localhost:4000> |
| `db` | `mysql_db` | MySQL database | `localhost:3200` |

## Repository Structure

```text
CoopTrack/
├── api/                    # Flask API, Blueprints, and database connection
│   ├── backend/
│   ├── tests/              # End-to-end API integration test
│   ├── .env.template      # Safe environment-variable template
│   └── backend_app.py
├── app/src/                # Streamlit application
│   ├── assets/             # CoopTrack branding
│   ├── modules/            # Shared navigation and UI helpers
│   ├── pages/              # Persona dashboards and feature pages
│   └── Home.py             # Persona-selection landing page
├── database-files/
│   ├── 01_schema.sql       # Database schema; runs first
│   └── 02_sample_data.sql  # Demonstration data; runs second
├── docs/                   # API matrix, route list, and testing guide
├── docker-compose.yaml
└── README.md
```

## Prerequisites

Install and start [Docker Desktop](https://www.docker.com/products/docker-desktop/).
Confirm that both Docker commands are available:

```bash
docker --version
docker compose version
```

## Environment Configuration

The real environment file is intentionally excluded from Git. Create it from the
provided template:

```bash
cp api/.env.template api/.env
```

Then open `api/.env` and replace the values inside angle brackets:

```dotenv
SECRET_KEY=<replace-with-a-random-secret>
DB_USER=root
DB_HOST=db
DB_PORT=3306
DB_NAME=cooptrack
MYSQL_ROOT_PASSWORD=<replace-with-a-strong-password>
```

The angle brackets are placeholders and should not remain in the finished `.env`
file. `SECRET_KEY` may be any long random string. Do not commit `api/.env` or expose
its passwords in screenshots.

## Start the Application

From the repository root, build and start all three services:

```bash
docker compose up -d --build
```

After the first build, the requirement's shorter command also starts all services:

```bash
docker compose up -d
```

Check that the services are running:

```bash
docker compose ps
```

Then open:

- Streamlit application: <http://localhost:8501>
- Flask API: <http://localhost:4000>
- MySQL from a database client: host `localhost`, port `3200`, database `cooptrack`

To follow service logs:

```bash
docker compose logs -f app api db
```

To stop the services without deleting the database volume:

```bash
docker compose down
```

## Database Initialization and Sample Data

When MySQL creates a new database volume, it automatically executes every `.sql`
file in `database-files/` in alphabetical order. CoopTrack therefore loads:

1. `01_schema.sql` — creates the `cooptrack` schema and tables.
2. `02_sample_data.sql` — inserts realistic, foreign-key-valid demonstration data.

Restarting an existing container does **not** rerun these files. After changing the
schema or sample data, recreate the MySQL volume:

```bash
docker compose down -v
docker compose up -d --build
```

> **Warning:** `docker compose down -v` deletes the current Docker database volume.
> Use it only when the database should be rebuilt from the SQL initialization files.

## Using the Streamlit Application

Open <http://localhost:8501> and select one of the sample personas:

1. **Continue as Sofia** for the student dashboard.
2. **Continue as Marcus** for the employer dashboard.
3. **Continue as Nikki** for the administrator dashboard.

Use **Log out** in the sidebar to return to persona selection. Persona selection,
role-aware navigation, branding, dashboards, and all nine feature pages are
implemented. Every feature page communicates with MySQL through the Flask API;
the Streamlit application never connects directly to the database.

## REST API

CoopTrack implements **29 routes** across five Flask Blueprints:

| Blueprint | Routes | Primary responsibility |
| --- | ---: | --- |
| `students` | 6 | Profiles, applications, saved positions, account status |
| `positions` | 7 | Search, details, applicants, counts, and posting management |
| `applications` | 5 | Submission, details, status updates, and withdrawal |
| `skills` | 6 | Skill taxonomy and demand analytics |
| `admin` | 5 | Reports, employer verification, and placement analytics |

The API uses GET, POST, PUT, and DELETE. See
[the REST API matrix](docs/CoopTrack_REST_API_Matrix.md) and
[route list](docs/CoopTrack_Route_List.md) for the complete contract.

## Testing

The reproducible test process is documented in [docs/Testing.md](docs/Testing.md).
With all containers running, execute the API integration test with:

```bash
python3 api/tests/integration_test.py
```

A verified clean build contains 18 tables and 1,288 sample rows. All 29 planned API
routes and all 12 persona dashboards/feature pages passed integration/runtime tests.

## Current Phase 3 Status

- [x] MySQL schema
- [x] Realistic SQL sample data
- [x] Ordered automatic database initialization
- [x] Streamlit persona selection and persona dashboards
- [x] CoopTrack logo and application theme
- [x] Final REST API matrix
- [x] Five Flask Blueprints and 29 routes
- [x] Nine persona feature pages connected to all API routes
- [x] Final clean-volume Docker integration testing
- [x] Unused project-template code removed
- [ ] Pitch and demo video

## Troubleshooting

### `zsh: command not found: docker`

Install Docker Desktop, open it, and wait until the Docker engine reports that it is
running. Then open a new terminal and rerun `docker --version`.

### `ModuleNotFoundError: No module named 'flask'`

The recommended setup runs Flask inside Docker. Run `docker compose up -d --build`
instead of launching `api/backend_app.py` with a system Python installation.

### Database changes are not appearing

The SQL initialization scripts only execute for a new MySQL volume. Recreate it with
`docker compose down -v`, then run `docker compose up -d --build`.

### Inspect service errors

```bash
docker compose ps
docker compose logs --tail=100 app api db
```

## Demo Video

The required public 6–8 minute pitch and demo video will be linked here before the
Phase 3 submission.

**Public video link:** Coming soon.
