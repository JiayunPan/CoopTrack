"""Administrator employer review and verified registration."""

import pandas as pd
import streamlit as st

from modules.api_client import ApiError, get, post
from modules.nav import SideBarLinks, require_role


st.set_page_config(page_title="Employer Verification · CoopTrack", page_icon="✅", layout="wide")
require_role("administrator")
SideBarLinks()

admin_id = st.session_state["admin_id"]
st.title("Employer verification")

try:
    employers = get("/admin/employers")
except ApiError as error:
    st.error(str(error))
    st.stop()

pending = [row for row in employers if row["verification_status"] == "PENDING"]
verified = [row for row in employers if row["verification_status"] == "VERIFIED"]
metric_one, metric_two, metric_three = st.columns(3)
metric_one.metric("All employers", len(employers))
metric_two.metric("Pending", len(pending))
metric_three.metric("Verified", len(verified))
st.dataframe(pd.DataFrame(employers), width="stretch", hide_index=True)

with st.form("register_verified_employer"):
    st.subheader("Register a verified employer")
    company_name = st.text_input("Company name")
    email = st.text_input("Recruiting email")
    confirmed = st.checkbox("I verified this organization's information.")
    submitted = st.form_submit_button(
        "Register and verify employer",
        type="primary",
    )
if submitted:
    if not confirmed:
        st.error("Confirm that the organization's information has been verified.")
    elif not company_name.strip() or not email.strip():
        st.error("Company name and email are required.")
    else:
        try:
            post(
                "/admin/employers",
                {
                    "company_name": company_name.strip(),
                    "email": email.strip(),
                    "admin_id": admin_id,
                },
            )
            st.success("Employer registered and verified.")
            st.rerun()
        except ApiError as error:
            st.error(str(error))
