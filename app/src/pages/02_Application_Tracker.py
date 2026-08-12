"""Student application submission and status tracking."""

import pandas as pd
import streamlit as st

from modules.api_client import ApiError, delete, get, post, put
from modules.nav import SideBarLinks, require_role


st.set_page_config(page_title="Application Tracker · CoopTrack", page_icon="📋", layout="wide")
require_role("student")
SideBarLinks()

student_id = st.session_state["user_id"]
st.title("Application tracker")


def load_data():
    return (
        get(f"/students/{student_id}/applications"),
        get("/positions", params={"status": "OPEN"}),
    )


try:
    applications, positions = load_data()
except ApiError as error:
    st.error(str(error))
    st.stop()

statuses = sorted({row["application_status"] for row in applications})
selected_statuses = st.multiselect("Filter by status", statuses, default=statuses)
filtered = [row for row in applications if row["application_status"] in selected_statuses]
if filtered:
    st.dataframe(pd.DataFrame(filtered), width="stretch", hide_index=True)
else:
    st.info("No applications match the current filter.")

with st.expander("Submit a new application", expanded=True):
    if positions:
        position_labels = {
            f"{row['position_title']} — {row['company_name']}": row["position_id"]
            for row in positions
        }
        selected_position = st.selectbox("Open position", position_labels)
        if st.button("Submit application", type="primary"):
            try:
                post(
                    "/applications",
                    {"student_id": student_id, "position_id": position_labels[selected_position]},
                )
                st.success("Application submitted.")
                st.rerun()
            except ApiError as error:
                st.error(str(error))
    else:
        st.info("There are currently no open positions.")

if applications:
    application_labels = {
        f"#{row['application_id']} · {row['position_title']}": row["application_id"]
        for row in applications
    }
    with st.expander("Update an application status"):
        selected_application = st.selectbox("Application", application_labels, key="update_application")
        new_status = st.selectbox(
            "New status",
            ["SUBMITTED", "SCREENING", "INTERVIEW", "OFFER", "ACCEPTED", "REJECTED"],
        )
        if st.button("Update status"):
            try:
                put(
                    f"/applications/{application_labels[selected_application]}",
                    {"application_status": new_status},
                )
                st.success("Application status updated.")
                st.rerun()
            except ApiError as error:
                st.error(str(error))

    with st.expander("Withdraw an application"):
        selected_withdrawal = st.selectbox("Application", application_labels, key="delete_application")
        confirm = st.checkbox("I understand this permanently withdraws the application.")
        if st.button("Withdraw application", disabled=not confirm):
            try:
                delete(f"/applications/{application_labels[selected_withdrawal]}")
                st.success("Application withdrawn.")
                st.rerun()
            except ApiError as error:
                st.error(str(error))
