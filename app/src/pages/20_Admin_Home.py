"""Landing page for Nikki, the system-administrator persona."""

import streamlit as st

from modules.nav import SideBarLinks, require_role


st.set_page_config(page_title="Admin Dashboard · CoopTrack", page_icon="🛡️", layout="wide")
require_role("administrator")
SideBarLinks()

st.title(f"Welcome back, {st.session_state['first_name']}")
st.write("Keep CoopTrack verified, consistent, and safe for the whole co-op community.")

metric_one, metric_two, metric_three, metric_four = st.columns(4)
metric_one.metric("Pending reports", "27")
metric_two.metric("Employers to verify", "4")
metric_three.metric("Moderation queue", "8")
metric_four.metric("Duplicate skills", "2")

st.subheader("Administration workspace")
reports_col, verification_col, governance_col = st.columns(3)

with reports_col:
    with st.container(border=True):
        st.markdown("### 🚩 Review reports")
        st.write("Investigate misleading or policy-violating postings and remove them from public view when necessary.")
        st.caption("Planned feature: Report Review")

with verification_col:
    with st.container(border=True):
        st.markdown("### ✅ Verify employers")
        st.write("Review pending organizations and register verified employers before they can publish opportunities.")
        st.caption("Planned feature: Employer Verification")

with governance_col:
    with st.container(border=True):
        st.markdown("### 🧹 Govern the platform")
        st.write("Suspend abusive student accounts and maintain a clean, shared vocabulary of skill tags.")
        st.caption("Planned feature: Student & Skill Management")

st.info("Feature pages will be connected after the Flask API contract is finalized.")
