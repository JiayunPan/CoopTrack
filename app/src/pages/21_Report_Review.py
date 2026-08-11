"""Administrator shell for reviewing reports against positions."""

import pandas as pd
import streamlit as st

from modules.mock_data import REPORTS
from modules.nav import SideBarLinks, require_role


st.set_page_config(page_title="Report Review · CoopTrack", page_icon="🚩", layout="wide")
require_role("administrator")
SideBarLinks()

st.title("Report review")
st.caption("Administrator feature shell · REST API integration pending")

reports = pd.DataFrame(REPORTS)
status = st.radio("Queue", ["All", "PENDING", "IN_REVIEW"], horizontal=True)
if status != "All":
    reports = reports[reports["Status"] == status]
st.dataframe(reports, width="stretch", hide_index=True)

with st.container(border=True):
    st.subheader("Moderation decision")
    st.selectbox("Report", [f"#{row['Report ID']} · {row['Position']}" for row in REPORTS])
    st.text_area("Review notes")
    decision_col, remove_col = st.columns(2)
    decision_col.button("Dismiss report", disabled=True, width="stretch")
    remove_col.button("Remove position", type="primary", disabled=True, width="stretch")
    st.caption("Final actions will resolve the report and, when necessary, delete or remove the position.")
