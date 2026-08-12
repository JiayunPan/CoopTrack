"""Landing page for Sofia, the student applicant persona."""

import streamlit as st

from modules.api_client import ApiError, get
from modules.nav import SideBarLinks, require_role


st.set_page_config(page_title="Student Dashboard · CoopTrack", page_icon="🎓", layout="wide")
require_role("student")
SideBarLinks()

student_id = st.session_state["user_id"]
st.title(f"Welcome back, {st.session_state['first_name']}")
st.write("Keep your co-op search focused and every next step visible.")

try:
    profile = get(f"/students/{student_id}")
    applications = get(f"/students/{student_id}/applications")
    open_positions = get("/positions", params={"status": "OPEN"})
except ApiError as error:
    st.error(str(error))
    st.stop()

active = [row for row in applications if row["application_status"] not in {"REJECTED"}]
interviews = [row for row in applications if row["application_status"] == "INTERVIEW"]
metric_one, metric_two, metric_three, metric_four = st.columns(4)
metric_one.metric("Major", profile.get("major") or "Not set")
metric_two.metric("Active applications", len(active))
metric_three.metric("Interviews", len(interviews))
metric_four.metric("Open positions", len(open_positions))

st.subheader("Student workspace")
search_col, tracker_col, deadline_col = st.columns(3)

with search_col:
    with st.container(border=True):
        st.markdown("### 🔎 Find opportunities")
        st.write("Search open co-op positions by role, location, and required skills, then save the best matches.")
        if st.button("Open position search", type="primary", width="stretch"):
            st.switch_page("pages/01_Position_Search.py")

with tracker_col:
    with st.container(border=True):
        st.markdown("### 📋 Track applications")
        st.write("Submit applications and keep screening, interview, offer, and decision statuses current.")
        if st.button("Open application tracker", type="primary", width="stretch"):
            st.switch_page("pages/02_Application_Tracker.py")

with deadline_col:
    with st.container(border=True):
        st.markdown("### 📅 Watch deadlines")
        st.write("Review upcoming application deadlines in date order so promising opportunities never slip by.")
        if st.button("Open upcoming deadlines", type="primary", width="stretch"):
            st.switch_page("pages/03_Upcoming_Deadlines.py")
