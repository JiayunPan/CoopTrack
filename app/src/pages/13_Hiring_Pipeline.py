"""Employer hiring pipeline analytics and status management."""

from collections import Counter

import pandas as pd
import plotly.express as px
import streamlit as st

from modules.api_client import ApiError, get, put
from modules.nav import SideBarLinks, require_role


st.set_page_config(page_title="Hiring Pipeline · CoopTrack", page_icon="🚦", layout="wide")
require_role("employer")
SideBarLinks()

employer_id = st.session_state["employer_id"]
st.title("Hiring pipeline")

try:
    positions = get("/positions", params={"employer_id": employer_id})
    applicant_groups = [
        get(f"/positions/{position['position_id']}/applicants")
        for position in positions
    ]
except ApiError as error:
    st.error(str(error))
    st.stop()

applicants = [applicant for group in applicant_groups for applicant in group]
stage_order = ["SUBMITTED", "SCREENING", "INTERVIEW", "OFFER", "ACCEPTED", "REJECTED"]
counts = Counter(row["application_status"] for row in applicants)
pipeline = pd.DataFrame(
    [{"Stage": stage.title(), "Candidates": counts.get(stage, 0)} for stage in stage_order]
)
chart = px.bar(pipeline, x="Stage", y="Candidates", color="Candidates", color_continuous_scale="Teal")
chart.update_layout(coloraxis_showscale=False, margin=dict(l=10, r=10, t=20, b=10))
st.plotly_chart(chart, width="stretch")

if applicants:
    st.dataframe(pd.DataFrame(applicants), width="stretch", hide_index=True)
    labels = {
        f"#{row['application_id']} · {row['student_name']}": row["application_id"]
        for row in applicants
    }
    with st.container(border=True):
        selected = st.selectbox("Candidate", labels)
        stage = st.selectbox("Move to stage", stage_order[1:])
        if st.button("Update pipeline", type="primary"):
            try:
                put(f"/applications/{labels[selected]}", {"application_status": stage})
                st.success("Pipeline updated.")
                st.rerun()
            except ApiError as error:
                st.error(str(error))
else:
    st.info("No applicants are currently in this employer's pipeline.")
