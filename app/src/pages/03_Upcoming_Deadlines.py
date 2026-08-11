"""Student shell for reviewing upcoming co-op deadlines."""

import pandas as pd
import streamlit as st

from modules.mock_data import DEADLINES
from modules.nav import SideBarLinks, require_role


st.set_page_config(page_title="Upcoming Deadlines · CoopTrack", page_icon="📅", layout="wide")
require_role("student")
SideBarLinks()

st.title("Upcoming deadlines")
st.caption("Student feature shell · REST API integration pending")

window = st.slider("Show deadlines within", min_value=7, max_value=60, value=30, step=7, format="%d days")
deadlines = pd.DataFrame(DEADLINES)
visible = deadlines[deadlines["Days left"] <= window].sort_values("Days left")

urgent = len(visible[visible["Days left"] <= 7])
saved = len(visible[visible["Saved"] == "Yes"])
metric_one, metric_two, metric_three = st.columns(3)
metric_one.metric("Within selected window", len(visible))
metric_two.metric("Due within 7 days", urgent)
metric_three.metric("Saved opportunities", saved)

st.dataframe(visible, width="stretch", hide_index=True)
st.info("The final page will load open positions ordered by application deadline from the REST API.")
