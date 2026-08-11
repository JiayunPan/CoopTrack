"""Administrator shell for approving or rejecting employer registrations."""

import pandas as pd
import streamlit as st

from modules.mock_data import PENDING_EMPLOYERS
from modules.nav import SideBarLinks, require_role


st.set_page_config(page_title="Employer Verification · CoopTrack", page_icon="✅", layout="wide")
require_role("administrator")
SideBarLinks()

st.title("Employer verification")
st.caption("Administrator feature shell · REST API integration pending")

metric_one, metric_two = st.columns(2)
metric_one.metric("Awaiting review", len(PENDING_EMPLOYERS))
metric_two.metric("Oldest request", "5 days")
st.dataframe(pd.DataFrame(PENDING_EMPLOYERS), width="stretch", hide_index=True)

with st.container(border=True):
    employer = st.selectbox("Employer", [row["Company"] for row in PENDING_EMPLOYERS])
    selected = next(row for row in PENDING_EMPLOYERS if row["Company"] == employer)
    st.write(f"**Contact:** {selected['Email']}")
    approve_col, reject_col = st.columns(2)
    approve_col.button("Verify employer", type="primary", disabled=True, width="stretch")
    reject_col.button("Reject request", disabled=True, width="stretch")
    st.caption("The verification decision will use the employer PUT route.")
