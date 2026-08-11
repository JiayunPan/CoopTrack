"""Employer shell for creating and maintaining position listings."""

import pandas as pd
import streamlit as st

from modules.mock_data import EMPLOYER_POSITIONS
from modules.nav import SideBarLinks, require_role


st.set_page_config(page_title="Position Management · CoopTrack", page_icon="✍️", layout="wide")
require_role("employer")
SideBarLinks()

st.title("Position management")
st.caption("Employer feature shell · REST API integration pending")
st.dataframe(pd.DataFrame(EMPLOYER_POSITIONS), width="stretch", hide_index=True)

create_tab, update_tab = st.tabs(["Create position", "Update or close position"])
with create_tab:
    left, right = st.columns(2)
    left.text_input("Position title")
    left.text_input("Location")
    left.selectbox("Work mode", ["ON_SITE", "HYBRID", "REMOTE"])
    right.selectbox("Recruiting term", ["Fall 2026", "Spring 2027"])
    right.date_input("Application deadline")
    right.multiselect("Required skills", ["Python", "SQL", "Java", "Tableau", "Communication"])
    st.text_area("Description")
    st.button("Create position", type="primary", disabled=True)
    st.caption("This action will use the position POST route.")

with update_tab:
    st.selectbox("Position", [row["Position"] for row in EMPLOYER_POSITIONS])
    st.selectbox("New status", ["OPEN", "CLOSED", "REMOVED"])
    st.button("Save changes", disabled=True)
    st.caption("This action will use the position PUT route.")
