"""Administrator report review and position moderation."""

import pandas as pd
import streamlit as st

from modules.api_client import ApiError, delete, get, put
from modules.nav import SideBarLinks, require_role


st.set_page_config(page_title="Report Review · CoopTrack", page_icon="🚩", layout="wide")
require_role("administrator")
SideBarLinks()

admin_id = st.session_state["admin_id"]
st.title("Report review")

try:
    reports = get("/admin/reports")
except ApiError as error:
    st.error(str(error))
    st.stop()

if not reports:
    st.success("There are no pending reports.")
    st.stop()

st.dataframe(pd.DataFrame(reports), width="stretch", hide_index=True)
labels = {
    f"#{row['report_id']} · {row['position_title']} · {row['reason']}": row
    for row in reports
}

with st.container(border=True):
    selected_label = st.selectbox("Report", labels)
    report = labels[selected_label]
    st.write(f"**Employer:** {report['company_name']}")
    st.write(f"**Reported by:** {report['reported_by']}")
    decision = st.radio(
        "Decision",
        ["Dismiss report", "Resolve report", "Remove position and resolve"],
    )
    confirm = st.checkbox("I have reviewed the report details.")
    if st.button("Apply moderation decision", type="primary", disabled=not confirm):
        try:
            if decision == "Remove position and resolve":
                delete(f"/positions/{report['position_id']}")
                review_status = "RESOLVED"
            elif decision == "Resolve report":
                review_status = "RESOLVED"
            else:
                review_status = "DISMISSED"
            put(
                f"/admin/reports/{report['report_id']}",
                {"review_status": review_status, "admin_id": admin_id},
            )
            st.success("Moderation decision saved.")
            st.rerun()
        except ApiError as error:
            st.error(str(error))
