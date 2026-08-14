# CoopTrack REST API — Route List

Reference for the Streamlit UI: every read/write the front end performs goes
through one of these Flask API routes. The Streamlit app must **not** connect to
MySQL directly.

- Example base URL: `http://api:4000` (inside the container network) or
  `http://localhost:4000` (from the host)
- 5 Blueprints, 30 routes
- Meets Phase 3 requirements: >=4 Blueprints, >=5 routes each,
  5 POST / 5 PUT / 4 DELETE, at most one of each write verb per Blueprint

---

## Blueprint 1 — students

| Method | Path | Story | Action |
|---|---|---|---|
| GET | `/students` | 3.1 | Return all students for account management |
| GET | `/students/<student_id>` | 3.1 | Return one student's profile |
| GET | `/students/<student_id>/applications` | 1.4 | All applications and statuses for a student |
| GET | `/students/<student_id>/saved` | 1.2 | Return the student's saved-position shortlist |
| POST | `/students/<student_id>/saved` | 1.2 | Save a position to the shortlist |
| DELETE | `/students/<student_id>/saved/<position_id>` | 1.5 | Remove a saved position |
| PUT | `/students/<student_id>` | 3.1 | Suspend / reactivate a student (admin) |

## Blueprint 2 — positions

| Method | Path | Story | Action |
|---|---|---|---|
| GET | `/positions` | 1.1 / 1.6 | Search / list open positions (filter by role, location, skill, deadline) |
| GET | `/positions/<position_id>` | 1.1 / 2.4 | Return one position's details |
| GET | `/positions/<position_id>/applicants` | 2.2 | Applicants ranked by skill match |
| GET | `/positions/<position_id>/count` | 2.6 | Application count for a position |
| POST | `/positions` | 2.1 | Post a new position |
| PUT | `/positions/<position_id>` | 2.4 / 2.5 | Edit a posting / close it |
| DELETE | `/positions/<position_id>` | 3.2 | Remove a posting from public view (admin) |

## Blueprint 3 — applications

| Method | Path | Story | Action |
|---|---|---|---|
| GET | `/applications` | 3.1 | Return all applications for administrative review |
| GET | `/applications/<application_id>` | 1.4 / 2.3 | Return one application's details |
| POST | `/applications` | 1.3 | Submit a new application |
| PUT | `/applications/<application_id>` | 1.4 / 2.3 | Update application / pipeline status |
| DELETE | `/applications/<application_id>` | 1.4 | Withdraw an application |

## Blueprint 4 — skills

| Method | Path | Story | Action |
|---|---|---|---|
| GET | `/skills` | 3.6 | List all skills |
| GET | `/skills/<skill_id>` | 3.6 | Return one skill's details |
| GET | `/skills/demand` | 5.4 | Most in-demand skills (analytics) |
| POST | `/skills` | 3.6 | Add a skill to the master list |
| PUT | `/skills/<skill_id>` | 3.6 | Update a skill (rename / status) |
| DELETE | `/skills/<skill_id>` | 3.4 | Delete an unused duplicate skill |

## Blueprint 5 — admin

| Method | Path | Story | Action |
|---|---|---|---|
| GET | `/admin/reports` | 3.3 | Pending flagged / reported postings |
| GET | `/admin/employers` | 3.5 | List all employers (including pending) |
| GET | `/admin/placements` | 5.1 | Placement statistics (dashboard) |
| POST | `/admin/employers` | 3.5 | Register and verify a new employer |
| PUT | `/admin/reports/<report_id>` | 3.3 | Resolve / close a report |

---

## Streamlit page -> route mapping

**Sofia / Student pages**
- Position Search: `GET /positions`
- Saved Positions: `GET /students/<id>/saved`, `POST /students/<id>/saved`, `DELETE /students/<id>/saved/<pid>`
- Application Tracker: `GET /students/<id>/applications`, `POST /applications`, `PUT /applications/<id>`
- Upcoming Deadlines: `GET /positions` (filtered by deadline)

**Marcus / Employer pages**
- Create Position: `POST /positions`
- Edit / Close Position: `PUT /positions/<id>`
- Applicant Review: `GET /positions/<id>/applicants`
- Candidate Pipeline: `PUT /applications/<id>`
- Dashboard: `GET /positions/<id>/count`

**Nikki / Admin pages**
- Pending Reports: `GET /admin/reports`, `PUT /admin/reports/<id>`
- Employer Verification: `GET /admin/employers`, `POST /admin/employers`
- Student Management: `PUT /students/<id>` (suspend)
- Skill Management: `GET /skills`, `POST /skills`, `DELETE /skills/<id>`

`DELETE /positions/<id>`, `GET /skills/demand`, and `GET /admin/placements`
are used by the Admin moderation page and dashboard. Every listed API route has
at least one Streamlit consumer.
