"""Temporary end-to-end verification for every planned CoopTrack API route."""

from __future__ import annotations

import json
import os
from uuid import uuid4
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


BASE = os.getenv("COOPTRACK_API_URL", "http://127.0.0.1:4000").rstrip("/")
RUN_ID = uuid4().hex[:10]


def call(method: str, path: str, payload=None, expected=(200,)):
    body = None if payload is None else json.dumps(payload).encode()
    request = Request(
        BASE + path,
        data=body,
        method=method,
        headers={"Content-Type": "application/json"},
    )
    try:
        with urlopen(request, timeout=10) as response:
            status = response.status
            data = json.loads(response.read() or b"null")
    except HTTPError as error:
        status = error.code
        data = json.loads(error.read() or b"null")
    assert status in expected, f"{method} {path}: expected {expected}, got {status}: {data}"
    print(f"PASS {method:6} {path:45} {status}")
    return data


# students: 6 routes
students = call("GET", "/students")
student_id = students[0]["student_id"]
student = call("GET", f"/students/{student_id}")
call("GET", f"/students/{student_id}/applications")
call("PUT", f"/students/{student_id}", {"active_status": False, "admin_id": 1})
updated_student = call("GET", f"/students/{student_id}")
assert not updated_student["active_status"]
call(
    "PUT",
    f"/students/{student_id}",
    {"active_status": bool(student["active_status"]), "admin_id": None},
)

# admin: 5 routes; create a test employer used by position tests
reports = call("GET", "/admin/reports")
call("GET", "/admin/employers")
call("GET", "/admin/placements")
employer = call(
    "POST",
    "/admin/employers",
    {
        "company_name": "CoopTrack Integration Test Employer",
        "email": f"integration-{RUN_ID}@cooptrack.invalid",
        "admin_id": 1,
    },
    expected=(201,),
)
employer_id = employer["employer_id"]
if reports:
    report_id = reports[0]["report_id"]
    call("PUT", f"/admin/reports/{report_id}", {"review_status": "RESOLVED", "admin_id": 1})
    call("PUT", f"/admin/reports/{report_id}", {"review_status": "PENDING", "admin_id": None})

# positions: 7 routes
query = urlencode({"status": "OPEN", "location": "Boston"})
call("GET", f"/positions?{query}")
position = call(
    "POST",
    "/positions",
    {
        "employer_id": employer_id,
        "term_id": 1,
        "position_title": "Integration Test Co-op",
        "description": "Temporary position used by the automated API test.",
        "location": "Boston, MA",
        "work_mode": "HYBRID",
        "employment_type": "COOP",
        "application_deadline": "2026-12-15",
    },
    expected=(201,),
)
position_id = position["position_id"]
call("GET", f"/positions/{position_id}")
call("GET", f"/positions/{position_id}/applicants")
count = call("GET", f"/positions/{position_id}/count")
assert count["application_count"] == 0
call("PUT", f"/positions/{position_id}", {"position_title": "Updated Integration Test Co-op"})

# saved-position POST and DELETE complete the student blueprint
call("POST", f"/students/{student_id}/saved", {"position_id": position_id}, expected=(201,))
call("DELETE", f"/students/{student_id}/saved/{position_id}")

# applications: 5 routes
call("GET", "/applications")
application = call(
    "POST",
    "/applications",
    {"student_id": student_id, "position_id": position_id},
    expected=(201,),
)
application_id = application["application_id"]
call("GET", f"/applications/{application_id}")
call("PUT", f"/applications/{application_id}", {"application_status": "INTERVIEW"})
interview = call("GET", f"/applications/{application_id}")
assert interview["application_status"] == "INTERVIEW"
assert interview["interview_date"] is not None
call("DELETE", f"/applications/{application_id}")
call("GET", f"/applications/{application_id}", expected=(404,))

# skills: 6 routes
call("GET", "/skills")
call("GET", "/skills/demand")
skill = call(
    "POST",
    "/skills",
    {"skill_name": f"CoopTrack Integration Test Skill {RUN_ID}", "admin_id": 1},
    expected=(201,),
)
skill_id = skill["skill_id"]
call("GET", f"/skills/{skill_id}")
call("PUT", f"/skills/{skill_id}", {"skill_name": "Updated Integration Test Skill"})
call("DELETE", f"/skills/{skill_id}")
call("GET", f"/skills/{skill_id}", expected=(404,))

# position DELETE is a soft removal; verify the state afterward
call("DELETE", f"/positions/{position_id}")
removed = call("GET", f"/positions/{position_id}")
assert removed["position_status"] == "REMOVED"

# representative validation/error behavior
call("GET", "/students/999999", expected=(404,))
call("POST", "/applications", {}, expected=(400,))
call("PUT", "/applications/999999", {"application_status": "NOT_A_STATUS"}, expected=(400,))
call("DELETE", "/skills/999999", expected=(404,))

print("\nAll 29 planned CoopTrack routes and representative errors passed.")
