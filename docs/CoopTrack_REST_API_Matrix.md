# CoopTrack — REST API Matrix

Phase 3 Requirement 1. Personas: **Sofia (Student)**, **Marcus (Employer)**,
**Nikki (Admin)**. Each cell gives a short synopsis of the route's action and
the user story that uses it.

| Resource | GET | POST | PUT | DELETE |
|---|---|---|---|---|
| `/students` | List all students (Nikki) | — | — | — |
| `/students/<id>` | One student's profile (Sofia, Nikki) | — | Suspend/reactivate a student — 3.1 (Nikki) | — |
| `/students/<id>/applications` | A student's applications — 1.x (Sofia) | — | — | — |
| `/students/<id>/saved` | — | Save a position to shortlist — 1.2 (Sofia) | — | — |
| `/students/<id>/saved/<pid>` | — | — | — | Remove a saved position — 1.5 (Sofia) |
| `/positions` | Search/list open positions — 1.1, 1.6 (Sofia) | Post a new position — 2.1 (Marcus) | — | — |
| `/positions/<id>` | Position details (Sofia, Marcus) | — | Edit/close a position — 2.4, 2.5 (Marcus) | Remove a posting — 3.2 (Nikki) |
| `/positions/<id>/applicants` | Applicants ranked by skill match — 2.2 (Marcus) | — | — | — |
| `/positions/<id>/count` | Application count for a posting — 2.6 (Marcus) | — | — | — |
| `/applications` | List all applications (Nikki) | Submit an application — 1.3 (Sofia) | — | — |
| `/applications/<id>` | Application details (Sofia, Marcus) | — | Update application/pipeline status — 1.4, 2.3 (Sofia, Marcus) | Withdraw an application (Sofia) |
| `/skills` | List all skills — 3.6 (Sofia, Nikki) | Add a skill to the master list — 3.6 (Nikki) | — | — |
| `/skills/<id>` | Skill details (Nikki) | — | Update a skill (Nikki) | Delete an unused duplicate skill — 3.4 (Nikki) |
| `/skills/demand` | Most in-demand skills — 5.4 (Marcus, Nikki) | — | — | — |
| `/admin/reports` | Pending flagged postings — 3.3 (Nikki) | — | — | — |
| `/admin/reports/<id>` | — | — | Resolve/close a report — 3.3 (Nikki) | — |
| `/admin/employers` | List employers incl. pending (Nikki) | Register & verify an employer — 3.5 (Nikki) | — | — |
| `/admin/placements` | Placement rate by term — 5.1 (Nikki) | — | — | — |

## Summary

- **5 Flask Blueprints:** `students`, `positions`, `applications`, `skills`, `admin`
- **29 routes total** — GET 15, POST 5, PUT 5, DELETE 4
- Every Blueprint has ≥5 routes and at most one of each write verb (POST/PUT/DELETE)
- Meets: ≥4 Blueprints, ≥2 POST, ≥2 PUT, ≥2 DELETE, ~20+ routes target
