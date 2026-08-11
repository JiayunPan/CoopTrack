"""Landing page for Sofia, the student applicant persona."""

import streamlit as st

from modules.nav import SideBarLinks, require_role


st.set_page_config(page_title="Student Dashboard · CoopTrack", page_icon="🎓", layout="wide")
require_role("student")
SideBarLinks()

st.title(f"Welcome back, {st.session_state['first_name']}")
st.write("Keep your co-op search focused and every next step visible.")

metric_one, metric_two, metric_three, metric_four = st.columns(4)
metric_one.metric("Saved roles", "4")
metric_two.metric("Active applications", "3")
metric_three.metric("Interviews", "1")
metric_four.metric("Next deadline", "6 days")

st.subheader("Student workspace")
search_col, tracker_col, deadline_col = st.columns(3)

with search_col:
    with st.container(border=True):
        st.markdown("### 🔎 Find opportunities")
        st.write("Search open co-op positions by role, location, and required skills, then save the best matches.")
        st.caption("Planned feature: Position Search & Save")

with tracker_col:
    with st.container(border=True):
        st.markdown("### 📋 Track applications")
        st.write("Record submitted applications and keep screening, interview, offer, and decision statuses current.")
        st.caption("Planned feature: Application Tracker")

with deadline_col:
    with st.container(border=True):
        st.markdown("### 📅 Watch deadlines")
        st.write("Review upcoming application deadlines in date order so promising opportunities never slip by.")
        st.caption("Planned feature: Upcoming Deadlines")

st.info("Feature pages will be connected after the Flask API contract is finalized.")
