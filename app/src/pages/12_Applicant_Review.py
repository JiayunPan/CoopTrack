"""Employer shell for comparing applicants and their skill fit."""

import pandas as pd
import streamlit as st

from modules.mock_data import APPLICANTS
from modules.nav import SideBarLinks, require_role


st.set_page_config(page_title="Applicant Review · CoopTrack", page_icon="🧩", layout="wide")
require_role("employer")
SideBarLinks()

st.title("Applicant review")
st.caption("Employer feature shell · REST API integration pending")

positions = sorted({row["Position"] for row in APPLICANTS})
selected = st.selectbox("Position", ["All positions", *positions])
applicants = pd.DataFrame(APPLICANTS)
if selected != "All positions":
    applicants = applicants[applicants["Position"] == selected]

st.dataframe(applicants, width="stretch", hide_index=True)

with st.container(border=True):
    st.subheader("Candidate detail")
    candidate = st.selectbox("Applicant", [row["Applicant"] for row in APPLICANTS])
    detail = next(row for row in APPLICANTS if row["Applicant"] == candidate)
    st.write(f"**Skill match:** {detail['Skill match']}")
    st.write(f"**Matched skills:** {detail['Matched skills']}")
    st.button("Advance candidate", type="primary", disabled=True)
    st.caption("The final action will update the application through a PUT route.")
