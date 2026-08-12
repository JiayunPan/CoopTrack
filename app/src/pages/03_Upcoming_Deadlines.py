"""Student view of upcoming open-position deadlines."""

from datetime import date, datetime

import pandas as pd
import streamlit as st

from modules.api_client import ApiError, get
from modules.nav import SideBarLinks, require_role


st.set_page_config(page_title="Upcoming Deadlines · CoopTrack", page_icon="📅", layout="wide")
require_role("student")
SideBarLinks()

st.title("Upcoming deadlines")
window = st.slider("Show deadlines within", min_value=7, max_value=120, value=30, step=7, format="%d days")

try:
    positions = get("/positions", params={"status": "OPEN"})
except ApiError as error:
    st.error(str(error))
    st.stop()

today = date.today()
deadlines = []
for position in positions:
    raw_deadline = position.get("application_deadline")
    if not raw_deadline:
        continue
    deadline = datetime.strptime(raw_deadline, "%a, %d %b %Y %H:%M:%S %Z").date()
    days_left = (deadline - today).days
    if 0 <= days_left <= window:
        deadlines.append(
            {
                "Deadline": deadline.isoformat(),
                "Position": position["position_title"],
                "Employer": position["company_name"],
                "Location": position.get("location"),
                "Days left": days_left,
            }
        )

deadlines.sort(key=lambda row: row["Days left"])
urgent = len([row for row in deadlines if row["Days left"] <= 7])
metric_one, metric_two, metric_three = st.columns(3)
metric_one.metric("Within selected window", len(deadlines))
metric_two.metric("Due within 7 days", urgent)
metric_three.metric("All open positions", len(positions))

if deadlines:
    st.dataframe(pd.DataFrame(deadlines), width="stretch", hide_index=True)
else:
    st.info("No open-position deadlines fall within the selected window.")
