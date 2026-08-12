# CoopTrack Phase 3 Pitch and Demo Plan

Target length: **7 minutes**. The allowed range is 6–8 minutes. Both team members
must remain on camera for the entire recording and contribute meaningfully.

## Before Recording

- Start Docker Desktop.
- Run `docker compose up -d --build`.
- Open Streamlit at <http://localhost:8501>.
- Open DataGrip on the `cooptrack` database at `localhost:3200`.
- Increase editor and browser font sizes so all content is readable in the video.
- Keep the API matrix and the five Blueprint folders ready in separate tabs.
- Confirm the final video-sharing setting is public to anyone with the link.

## 0:00–0:20 — Team Introduction

**Erica:**

> Hi, we are Erica Cheng and Jiayun Pan. Our CS 3200 project is CoopTrack, a
> three-tier database application for managing the co-op search and recruiting
> process.

## 0:20–1:00 — Elevator Pitch

**Jiayun:**

> Students often track positions, deadlines, and application statuses across
> disconnected tools. Employers need a clearer way to manage postings and candidate
> pipelines, while administrators need reliable moderation and reporting controls.
> CoopTrack brings those workflows into one application backed by a normalized MySQL
> database, a Flask REST API, and role-specific Streamlit interfaces.

## 1:00–2:25 — Architecture and REST API

**Erica:**

1. Show the top-level repository structure.
2. Briefly show the REST API matrix.
3. Show the five Blueprint folders:
   - `students` — 6 routes
   - `positions` — 7 routes
   - `applications` — 5 routes
   - `skills` — 6 routes
   - `admin` — 5 routes
4. State that the 29 routes use GET, POST, PUT, and DELETE.
5. Show `rest_entry.py` registering all five Blueprints.
6. Explain that Streamlit calls Flask through HTTP/JSON and never connects directly
   to MySQL.

Do not review routes line by line.

## 2:25–3:50 — Sofia / Student Demo

**Jiayun:**

1. Select **Continue as Sofia**.
2. Show live dashboard metrics.
3. Open **Find positions** and demonstrate role/location/skill filters.
4. Save a position.
5. Open **Application tracker** and submit an application to that position.
6. Update the application status to `INTERVIEW`.
7. Show **Upcoming deadlines**.

## 3:50–5:10 — Marcus / Employer Demo

**Erica:**

1. Log out and select **Continue as Marcus**.
2. Open **Position management**.
3. Create a clearly named demonstration position.
4. Update its title or close it to demonstrate PUT.
5. Open **Applicant review** and explain the calculated skill-match percentage.
6. Open **Hiring pipeline** and move a candidate to another stage.

## 5:10–6:20 — Nikki / Administrator Demo

**Jiayun:**

1. Log out and select **Continue as Nikki**.
2. Show placement-rate analytics on the dashboard.
3. Open **Report review** and dismiss or resolve one report.
4. Demonstrate removing a reported position from public view.
5. Open **Employer verification** and register one verified employer.
6. Open **Students & skills**, update a student status, and add/edit an unused skill.

## 6:20–6:50 — Verify Database Mutations

**Erica:**

In DataGrip, run focused queries showing the effects of the demonstrated writes:

```sql
SELECT * FROM application ORDER BY application_id DESC LIMIT 5;
SELECT * FROM position ORDER BY position_id DESC LIMIT 5;
SELECT * FROM employer ORDER BY employer_id DESC LIMIT 5;
SELECT * FROM skill ORDER BY skill_id DESC LIMIT 5;
SELECT * FROM report ORDER BY report_id LIMIT 5;
```

Point out the newly inserted records and changed statuses. Explicitly identify the
POST, PUT, and DELETE/soft-delete results.

## 6:50–7:00 — Closing

**Both:**

> CoopTrack demonstrates a complete database-backed workflow across students,
> employers, and administrators. Thank you for watching.

## After Recording

1. Confirm the video duration is between 6:00 and 8:00.
2. Confirm both members remain visible for the entire recording.
3. Upload without splicing separately recorded individual sections.
4. Test the public link in a private/incognito browser window.
5. Replace `Coming soon` in the root `README.md` with the public link.
6. Add the same public link to the Phase 3 Submission Google Doc.
