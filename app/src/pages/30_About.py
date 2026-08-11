"""About page for CoopTrack."""

import streamlit as st

from modules.nav import SideBarLinks


st.set_page_config(page_title="About · CoopTrack", page_icon="ℹ️", layout="wide")
SideBarLinks(show_home=not st.session_state.get("authenticated", False))

st.title("About CoopTrack")
st.markdown(
    """
    **CoopTrack** is a data-driven web application that brings the co-op search
    lifecycle into one place. Students organize opportunities and applications,
    employers manage roles and candidate pipelines, and administrators protect
    the quality of the platform.

    ### Architecture

    - **Streamlit** provides the persona-specific user experience.
    - **Flask** exposes the REST API and application logic.
    - **MySQL** stores positions, applications, skills, reports, and account data.

    CoopTrack is a CS 3200 Summer B 2026 database-design project by **Team Thinking**.
    """
)

if st.button("Return to persona selection", type="primary"):
    st.switch_page("Home.py")
