"""Temporary presentation data for Streamlit shells awaiting REST API integration."""

OPEN_POSITIONS = [
    {"Position": "Data Analyst Co-op", "Employer": "Northstar Robotics", "Location": "Boston, MA", "Mode": "Hybrid", "Deadline": "2026-08-24", "Skills": "SQL, Python"},
    {"Position": "Software Engineer Co-op", "Employer": "Harbor Health", "Location": "Cambridge, MA", "Mode": "On-site", "Deadline": "2026-08-28", "Skills": "Python, Flask"},
    {"Position": "Product Operations Co-op", "Employer": "BrightGrid Energy", "Location": "Somerville, MA", "Mode": "Hybrid", "Deadline": "2026-09-02", "Skills": "Excel, Analytics"},
    {"Position": "UX Research Co-op", "Employer": "CivicWorks Lab", "Location": "Remote", "Mode": "Remote", "Deadline": "2026-09-05", "Skills": "Research, Figma"},
]

APPLICATIONS = [
    {"Position": "Data Analyst Co-op", "Employer": "Northstar Robotics", "Submitted": "2026-08-03", "Status": "INTERVIEW", "Next step": "Interview · Aug 18"},
    {"Position": "Backend Developer Co-op", "Employer": "Atlas Learning", "Submitted": "2026-08-05", "Status": "SCREENING", "Next step": "Await recruiter review"},
    {"Position": "Business Intelligence Co-op", "Employer": "BrightGrid Energy", "Submitted": "2026-08-08", "Status": "SUBMITTED", "Next step": "Application received"},
    {"Position": "Cloud Engineering Co-op", "Employer": "Juniper Systems", "Submitted": "2026-07-26", "Status": "CLOSED", "Next step": "No further action"},
]

DEADLINES = [
    {"Deadline": "2026-08-17", "Position": "QA Automation Co-op", "Employer": "Vertex Labs", "Days left": 6, "Saved": "Yes"},
    {"Deadline": "2026-08-20", "Position": "Data Engineering Co-op", "Employer": "Harbor Health", "Days left": 9, "Saved": "Yes"},
    {"Deadline": "2026-08-24", "Position": "Data Analyst Co-op", "Employer": "Northstar Robotics", "Days left": 13, "Saved": "No"},
    {"Deadline": "2026-09-02", "Position": "Product Operations Co-op", "Employer": "BrightGrid Energy", "Days left": 22, "Saved": "Yes"},
]

EMPLOYER_POSITIONS = [
    {"ID": 1, "Position": "Data Analyst Co-op", "Status": "OPEN", "Deadline": "2026-08-24", "Applicants": 4},
    {"ID": 2, "Position": "Robotics Software Co-op", "Status": "OPEN", "Deadline": "2026-09-01", "Applicants": 2},
    {"ID": 3, "Position": "Operations Co-op", "Status": "CLOSED", "Deadline": "2026-07-30", "Applicants": 7},
]

APPLICANTS = [
    {"Applicant": "Sofia Martinez", "Position": "Data Analyst Co-op", "Status": "INTERVIEW", "Skill match": "88%", "Matched skills": "SQL, Python, Tableau"},
    {"Applicant": "Noah Williams", "Position": "Data Analyst Co-op", "Status": "SCREENING", "Skill match": "75%", "Matched skills": "SQL, Excel"},
    {"Applicant": "Ava Thompson", "Position": "Robotics Software Co-op", "Status": "SUBMITTED", "Skill match": "82%", "Matched skills": "Python, C++"},
    {"Applicant": "Liam Chen", "Position": "Robotics Software Co-op", "Status": "OFFER", "Skill match": "93%", "Matched skills": "Python, C++, ROS"},
]

PIPELINE = [
    {"Stage": "Submitted", "Candidates": 6},
    {"Stage": "Screening", "Candidates": 3},
    {"Stage": "Interview", "Candidates": 2},
    {"Stage": "Offer", "Candidates": 1},
    {"Stage": "Accepted", "Candidates": 0},
]

REPORTS = [
    {"Report ID": 101, "Position": "Marketing Co-op", "Employer": "Example Dynamics", "Reason": "Misleading description", "Status": "PENDING", "Reported": "2026-08-09"},
    {"Report ID": 102, "Position": "Software Intern", "Employer": "Nova Consulting", "Reason": "Duplicate posting", "Status": "PENDING", "Reported": "2026-08-10"},
    {"Report ID": 103, "Position": "Research Assistant", "Employer": "Metro Analytics", "Reason": "Expired opportunity", "Status": "IN_REVIEW", "Reported": "2026-08-10"},
]

PENDING_EMPLOYERS = [
    {"Employer ID": 31, "Company": "Beacon BioTech", "Email": "recruiting@beacon.example", "Submitted": "2026-08-06", "Status": "PENDING"},
    {"Employer ID": 32, "Company": "Commonwealth AI", "Email": "careers@commonwealth.example", "Submitted": "2026-08-07", "Status": "PENDING"},
    {"Employer ID": 33, "Company": "Seaport Mobility", "Email": "talent@seaport.example", "Submitted": "2026-08-09", "Status": "PENDING"},
    {"Employer ID": 34, "Company": "Evergreen Finance", "Email": "jobs@evergreen.example", "Submitted": "2026-08-10", "Status": "PENDING"},
]

STUDENTS = [
    {"Student ID": 1, "Student": "Sofia Martinez", "Major": "Data Science", "Status": "ACTIVE", "Skills": 6},
    {"Student ID": 2, "Student": "Noah Williams", "Major": "Computer Science", "Status": "ACTIVE", "Skills": 5},
    {"Student ID": 3, "Student": "Ava Thompson", "Major": "Information Systems", "Status": "SUSPENDED", "Skills": 4},
]

SKILLS = [
    {"Skill ID": 1, "Skill": "Python", "Status": "ACTIVE", "Profiles": 26},
    {"Skill ID": 2, "Skill": "SQL", "Status": "ACTIVE", "Profiles": 23},
    {"Skill ID": 3, "Skill": "Java Script", "Status": "REVIEW", "Profiles": 2},
    {"Skill ID": 4, "Skill": "JavaScript", "Status": "ACTIVE", "Profiles": 18},
]
