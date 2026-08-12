"""Landing page for Marcus, the employer/recruiter persona."""

import streamlit as st

from modules.api_client import ApiError, get
from modules.nav import SideBarLinks, require_role


st.set_page_config(page_title="Employer Dashboard · CoopTrack", page_icon="💼", layout="wide")
require_role("employer")
SideBarLinks()

employer_id = st.session_state["employer_id"]
st.title(f"Welcome back, {st.session_state['first_name']}")
st.write("Manage your co-op opportunities and move strong candidates forward.")

try:
    positions = get("/positions", params={"employer_id": employer_id})
    counts = [get(f"/positions/{row['position_id']}/count") for row in positions]
except ApiError as error:
    st.error(str(error))
    st.stop()

open_positions = [row for row in positions if row["position_status"] == "OPEN"]
total_applicants = sum(row["application_count"] for row in counts)
metric_one, metric_two, metric_three = st.columns(3)
metric_one.metric("Open postings", len(open_positions))
metric_two.metric("All postings", len(positions))
metric_three.metric("Total applications", total_applicants)

st.subheader("Recruiting workspace")
posting_col, applicant_col, pipeline_col = st.columns(3)

with posting_col:
    with st.container(border=True):
        st.markdown("### ✍️ Manage postings")
        st.write("Create positions, update role details and deadlines, and close positions when filled.")
        if st.button("Open position management", type="primary", width="stretch"):
            st.switch_page("pages/11_Position_Management.py")

with applicant_col:
    with st.container(border=True):
        st.markdown("### 🧩 Review skill fit")
        st.write("Compare applicants using the overlap between student and position skills.")
        if st.button("Open applicant review", type="primary", width="stretch"):
            st.switch_page("pages/12_Applicant_Review.py")

with pipeline_col:
    with st.container(border=True):
        st.markdown("### 🚦 Manage the pipeline")
        st.write("Update candidate stages and monitor application volume across every posting.")
        if st.button("Open hiring pipeline", type="primary", width="stretch"):
            st.switch_page("pages/13_Hiring_Pipeline.py")
