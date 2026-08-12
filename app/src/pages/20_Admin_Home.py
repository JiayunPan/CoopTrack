"""Landing page for Nikki, the system-administrator persona."""

import pandas as pd
import plotly.express as px
import streamlit as st

from modules.api_client import ApiError, get
from modules.nav import SideBarLinks, require_role


st.set_page_config(page_title="Admin Dashboard · CoopTrack", page_icon="🛡️", layout="wide")
require_role("administrator")
SideBarLinks()

st.title(f"Welcome back, {st.session_state['first_name']}")
st.write("Keep CoopTrack verified, consistent, and safe for the whole co-op community.")

try:
    reports = get("/admin/reports")
    employers = get("/admin/employers")
    placements = get("/admin/placements")
    skill_demand = get("/skills/demand")
except ApiError as error:
    st.error(str(error))
    st.stop()

pending_employers = [row for row in employers if row["verification_status"] == "PENDING"]
metric_one, metric_two, metric_three, metric_four = st.columns(4)
metric_one.metric("Pending reports", len(reports))
metric_two.metric("Employers to verify", len(pending_employers))
metric_three.metric("Recruiting terms", len(placements))
metric_four.metric("Tracked skills", len(skill_demand))

st.subheader("Placement analytics")
placement_frame = pd.DataFrame(placements)
if not placement_frame.empty:
    chart = px.bar(
        placement_frame,
        x="season",
        y="placement_rate",
        labels={"season": "Recruiting term", "placement_rate": "Placement rate (%)"},
    )
    st.plotly_chart(chart, width="stretch")
else:
    st.info("No placement data is available.")

st.subheader("Administration workspace")
reports_col, verification_col, governance_col = st.columns(3)
with reports_col:
    with st.container(border=True):
        st.markdown("### 🚩 Review reports")
        st.write("Investigate reported postings and remove them from public view when necessary.")
        if st.button("Open report review", type="primary", width="stretch"):
            st.switch_page("pages/21_Report_Review.py")
with verification_col:
    with st.container(border=True):
        st.markdown("### ✅ Verify employers")
        st.write("Review employer records and register verified organizations.")
        if st.button("Open employer verification", type="primary", width="stretch"):
            st.switch_page("pages/22_Employer_Verification.py")
with governance_col:
    with st.container(border=True):
        st.markdown("### 🧹 Govern the platform")
        st.write("Manage student access and maintain the shared skill taxonomy.")
        if st.button("Open students and skills", type="primary", width="stretch"):
            st.switch_page("pages/23_Student_Skill_Management.py")
