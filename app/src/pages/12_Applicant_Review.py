"""Employer applicant and skill-match review."""

import pandas as pd
import streamlit as st

from modules.api_client import ApiError, get, put
from modules.nav import SideBarLinks, require_role


st.set_page_config(page_title="Applicant Review · CoopTrack", page_icon="🧩", layout="wide")
require_role("employer")
SideBarLinks()

employer_id = st.session_state["employer_id"]
st.title("Applicant review")

try:
    positions = get("/positions", params={"employer_id": employer_id})
except ApiError as error:
    st.error(str(error))
    st.stop()

if not positions:
    st.info("Create a position before reviewing applicants.")
    st.stop()

labels = {f"{row['position_title']} · #{row['position_id']}": row["position_id"] for row in positions}
selected_label = st.selectbox("Position", labels)

try:
    applicants = get(f"/positions/{labels[selected_label]}/applicants")
except ApiError as error:
    st.error(str(error))
    st.stop()

if applicants:
    for applicant in applicants:
        required = applicant["required_skill_count"]
        applicant["skill_match_percent"] = round(
            100 * applicant["matched_skill_count"] / required
        ) if required else 0
    st.dataframe(pd.DataFrame(applicants), width="stretch", hide_index=True)

    candidate_labels = {
        f"{row['student_name']} · {row['skill_match_percent']}% match": row
        for row in applicants
    }
    with st.container(border=True):
        candidate_label = st.selectbox("Candidate", candidate_labels)
        candidate = candidate_labels[candidate_label]
        new_status = st.selectbox("Move candidate to", ["SCREENING", "INTERVIEW", "OFFER", "ACCEPTED", "REJECTED"])
        if st.button("Update candidate", type="primary"):
            try:
                put(
                    f"/applications/{candidate['application_id']}",
                    {"application_status": new_status},
                )
                st.success("Candidate status updated.")
                st.rerun()
            except ApiError as error:
                st.error(str(error))
else:
    st.info("No students have applied to this position yet.")
