"""Student shell for discovering and saving co-op positions."""

import pandas as pd
import streamlit as st

from modules.mock_data import OPEN_POSITIONS
from modules.nav import SideBarLinks, require_role


st.set_page_config(page_title="Find Positions · CoopTrack", page_icon="🔎", layout="wide")
require_role("student")
SideBarLinks()

st.title("Find and save positions")
st.caption("Student feature shell · REST API integration pending")

query_col, location_col, mode_col = st.columns([2, 1, 1])
query = query_col.text_input("Keywords", placeholder="SQL, data analyst, Python…")
location = location_col.selectbox("Location", ["All locations", "Boston, MA", "Cambridge, MA", "Somerville, MA", "Remote"])
mode = mode_col.selectbox("Work mode", ["All modes", "On-site", "Hybrid", "Remote"])

positions = pd.DataFrame(OPEN_POSITIONS)
if query:
    mask = positions.astype(str).apply(lambda column: column.str.contains(query, case=False)).any(axis=1)
    positions = positions[mask]
if location != "All locations":
    positions = positions[positions["Location"] == location]
if mode != "All modes":
    positions = positions[positions["Mode"] == mode]

st.metric("Matching open positions", len(positions))
st.dataframe(positions, width="stretch", hide_index=True)

with st.container(border=True):
    st.subheader("Save an opportunity")
    st.selectbox("Position", [row["Position"] for row in OPEN_POSITIONS])
    st.button("Save position", type="primary", disabled=True)
    st.caption("This action will be enabled when the save-position POST route is connected.")
