"""Student position discovery and shortlist management."""

import pandas as pd
import streamlit as st

from modules.api_client import ApiError, delete, get, post
from modules.nav import SideBarLinks, require_role


st.set_page_config(page_title="Find Positions · CoopTrack", page_icon="🔎", layout="wide")
require_role("student")
SideBarLinks()

student_id = st.session_state["user_id"]
st.title("Find and save positions")

# --- Search filters ---
query_col, location_col, skill_col = st.columns([2, 1, 1])
role = query_col.text_input("Role keywords", placeholder="Data analyst, software…")
location = location_col.text_input("Location", placeholder="Boston")
skill = skill_col.text_input("Required skill", placeholder="Python")

params = {"status": "OPEN"}
if role:
    params["role"] = role
if location:
    params["location"] = location
if skill:
    params["skill"] = skill

try:
    with st.spinner("Loading open positions…"):
        positions = get("/positions", params=params)
except ApiError as error:
    st.error(str(error))
    st.stop()

st.metric("Matching open positions", len(positions))
if positions:
    st.dataframe(pd.DataFrame(positions), width="stretch", hide_index=True)
else:
    st.info("No open positions match these filters.")

# --- Shortlist actions ---
saved_positions = st.session_state.setdefault("saved_position_ids", set())
with st.container(border=True):
    st.subheader("Shortlist actions")
    if not positions:
        st.caption("A matching position is required before it can be saved.")
    else:
        labels = {
            f"{row['position_title']} — {row['company_name']}": row["position_id"]
            for row in positions
        }
        selected_label = st.selectbox("Position", labels)
        position_id = labels[selected_label]
        try:
            position_detail = get(f"/positions/{position_id}")
        except ApiError as error:
            st.error(str(error))
            position_detail = None
        if position_detail:
            st.write(position_detail.get("description") or "No description provided.")
            st.caption(
                f"{position_detail.get('work_mode') or 'Mode not set'} · "
                f"{position_detail.get('employment_type') or 'Type not set'}"
            )
        save_col, remove_col = st.columns(2)
        if save_col.button("Save position", type="primary", width="stretch"):
            try:
                post(f"/students/{student_id}/saved", {"position_id": position_id})
                saved_positions.add(position_id)
                st.success("Position saved to your shortlist.")
            except ApiError as error:
                st.error(str(error))
        if remove_col.button("Remove saved position", width="stretch"):
            try:
                delete(f"/students/{student_id}/saved/{position_id}")
                saved_positions.discard(position_id)
                st.success("Position removed from your shortlist.")
            except ApiError as error:
                st.error(str(error))

# --- My saved positions (NEW: reads the student's saved shortlist from the API) ---
with st.container(border=True):
    st.subheader("📌 My saved positions")
    try:
        saved = get(f"/students/{student_id}/saved")
    except ApiError as error:
        st.error(str(error))
        saved = []
    if saved:
        st.dataframe(pd.DataFrame(saved), width="stretch", hide_index=True)
    else:
        st.caption("You have not saved any positions yet.")