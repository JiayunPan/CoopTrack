"""Landing page for Marcus, the employer/recruiter persona."""

import streamlit as st

from modules.nav import SideBarLinks, require_role


st.set_page_config(page_title="Employer Dashboard · CoopTrack", page_icon="💼", layout="wide")
require_role("employer")
SideBarLinks()

st.title(f"Welcome back, {st.session_state['first_name']}")
st.write("Manage Northstar Robotics opportunities and move strong candidates forward.")

metric_one, metric_two, metric_three, metric_four = st.columns(4)
metric_one.metric("Open postings", "2")
metric_two.metric("Total applicants", "6")
metric_three.metric("In interview", "2")
metric_four.metric("Offers", "1")

st.subheader("Recruiting workspace")
posting_col, applicant_col, pipeline_col = st.columns(3)

with posting_col:
    with st.container(border=True):
        st.markdown("### ✍️ Manage postings")
        st.write("Create co-op positions, update role details and deadlines, and close positions when they are filled.")
        st.caption("Planned feature: Position Management")

with applicant_col:
    with st.container(border=True):
        st.markdown("### 🧩 Review skill fit")
        st.write("Compare applicants using the overlap between student skills and each position's required skills.")
        st.caption("Planned feature: Applicant Review")

with pipeline_col:
    with st.container(border=True):
        st.markdown("### 🚦 Manage the pipeline")
        st.write("Update candidate stages and monitor application volume across every employer posting.")
        st.caption("Planned feature: Candidate Pipeline")

st.info("Feature pages will be connected after the Flask API contract is finalized.")
