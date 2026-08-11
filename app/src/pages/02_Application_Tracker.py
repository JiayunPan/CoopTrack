"""Student shell for recording and tracking applications."""

import pandas as pd
import streamlit as st

from modules.mock_data import APPLICATIONS
from modules.nav import SideBarLinks, require_role


st.set_page_config(page_title="Application Tracker · CoopTrack", page_icon="📋", layout="wide")
require_role("student")
SideBarLinks()

st.title("Application tracker")
st.caption("Student feature shell · REST API integration pending")

status = st.multiselect(
    "Filter by status",
    ["SUBMITTED", "SCREENING", "INTERVIEW", "OFFER", "ACCEPTED", "CLOSED"],
    default=["SUBMITTED", "SCREENING", "INTERVIEW", "OFFER"],
)
applications = pd.DataFrame(APPLICATIONS)
filtered = applications[applications["Status"].isin(status)] if status else applications.iloc[0:0]
st.dataframe(filtered, width="stretch", hide_index=True)

with st.expander("Record a new application", expanded=True):
    st.text_input("Position or posting ID", placeholder="Select from an API-powered position list")
    st.date_input("Submitted date")
    st.button("Add application", type="primary", disabled=True)
    st.caption("This action will use the application POST route.")

with st.expander("Update an application status"):
    st.selectbox("Application", [f"{row['Position']} — {row['Employer']}" for row in APPLICATIONS])
    st.selectbox("New status", ["SUBMITTED", "SCREENING", "INTERVIEW", "OFFER", "ACCEPTED", "CLOSED"])
    st.button("Update status", disabled=True)
    st.caption("This action will use the application PUT route.")
