"""Employer shell for monitoring candidates across hiring stages."""

import pandas as pd
import plotly.express as px
import streamlit as st

from modules.mock_data import APPLICANTS, PIPELINE
from modules.nav import SideBarLinks, require_role


st.set_page_config(page_title="Hiring Pipeline · CoopTrack", page_icon="🚦", layout="wide")
require_role("employer")
SideBarLinks()

st.title("Hiring pipeline")
st.caption("Employer feature shell · REST API integration pending")

pipeline = pd.DataFrame(PIPELINE)
chart = px.bar(pipeline, x="Stage", y="Candidates", color="Candidates", color_continuous_scale="Teal")
chart.update_layout(coloraxis_showscale=False, margin=dict(l=10, r=10, t=20, b=10))
st.plotly_chart(chart, width="stretch")

st.subheader("Candidates")
st.dataframe(pd.DataFrame(APPLICANTS), width="stretch", hide_index=True)

with st.container(border=True):
    st.selectbox("Candidate", [row["Applicant"] for row in APPLICANTS])
    st.selectbox("Move to stage", ["SCREENING", "INTERVIEW", "OFFER", "ACCEPTED", "CLOSED"])
    st.button("Update pipeline", type="primary", disabled=True)
    st.caption("This action will be enabled after the application-status PUT route is connected.")
