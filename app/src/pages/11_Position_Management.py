"""Employer position creation and maintenance."""

from datetime import date

import pandas as pd
import streamlit as st

from modules.api_client import ApiError, get, post, put
from modules.nav import SideBarLinks, require_role


st.set_page_config(page_title="Position Management · CoopTrack", page_icon="✍️", layout="wide")
require_role("employer")
SideBarLinks()

employer_id = st.session_state["employer_id"]
st.title("Position management")

try:
    positions = get("/positions", params={"employer_id": employer_id})
except ApiError as error:
    st.error(str(error))
    st.stop()

if positions:
    st.dataframe(pd.DataFrame(positions), width="stretch", hide_index=True)
else:
    st.info("This employer has no position listings yet.")

create_tab, update_tab = st.tabs(["Create position", "Update or close position"])
with create_tab:
    with st.form("create_position_form"):
        left, right = st.columns(2)
        title = left.text_input("Position title")
        location = left.text_input("Location")
        work_mode = left.selectbox("Work mode", ["ON_SITE", "HYBRID", "REMOTE"])
        term_id = right.number_input("Recruiting term ID", min_value=1, step=1, value=1)
        deadline = right.date_input("Application deadline", min_value=date.today())
        employment_type = right.selectbox("Employment type", ["COOP", "INTERNSHIP", "PART_TIME"])
        description = st.text_area("Description")
        submitted = st.form_submit_button("Create position", type="primary")
    if submitted:
        if not title.strip():
            st.error("Position title is required.")
        else:
            try:
                post(
                    "/positions",
                    {
                        "employer_id": employer_id,
                        "term_id": int(term_id),
                        "position_title": title.strip(),
                        "description": description.strip() or None,
                        "location": location.strip() or None,
                        "work_mode": work_mode,
                        "employment_type": employment_type,
                        "application_deadline": deadline.isoformat(),
                    },
                )
                st.success("Position created.")
                st.rerun()
            except ApiError as error:
                st.error(str(error))

with update_tab:
    if positions:
        labels = {
            f"#{row['position_id']} · {row['position_title']}": row
            for row in positions
        }
        selected_label = st.selectbox("Position", labels)
        selected = labels[selected_label]
        new_title = st.text_input("Position title", value=selected["position_title"])
        new_status = st.selectbox(
            "Status",
            ["OPEN", "CLOSED"],
            index=0 if selected["position_status"] == "OPEN" else 1,
        )
        if st.button("Save changes", type="primary"):
            try:
                put(
                    f"/positions/{selected['position_id']}",
                    {"position_title": new_title.strip(), "position_status": new_status},
                )
                st.success("Position updated.")
                st.rerun()
            except ApiError as error:
                st.error(str(error))
    else:
        st.caption("Create a position before attempting an update.")
