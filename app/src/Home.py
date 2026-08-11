"""CoopTrack landing page and simulated persona sign-in."""

import logging

import streamlit as st

from modules.nav import SideBarLinks


logging.basicConfig(
    format="%(filename)s:%(lineno)s:%(levelname)s -- %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

st.set_page_config(
    page_title="CoopTrack",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Visiting the main page signs out the previous simulated persona.
for key in ("authenticated", "role", "first_name", "user_id", "employer_id", "admin_id"):
    st.session_state.pop(key, None)
st.session_state.authenticated = False

SideBarLinks(show_home=True)
logger.info("Loading the CoopTrack landing page")

logo_col, copy_col = st.columns([1, 2], vertical_alignment="center")
with logo_col:
    st.image("assets/logo.png", width=300)

with copy_col:
    st.title("Your co-op search, organized.")
    st.markdown(
        """
        CoopTrack brings job discovery, application progress, recruiting workflows,
        and platform administration into one reliable workspace. Choose a sample
        persona below to explore the experience—no account creation is required.
        """
    )
    st.caption("CS 3200 · Summer B 2026 · Team Thinking")

st.divider()
st.subheader("Choose a persona")

student_col, employer_col, admin_col = st.columns(3)

with student_col:
    with st.container(border=True):
        st.markdown("### 🎓 Sofia")
        st.caption("Student applicant")
        st.write("Search fitting roles, save opportunities, and keep every application deadline and status in one place.")
        if st.button("Continue as Sofia", type="primary", use_container_width=True):
            st.session_state.update(
                authenticated=True,
                role="student",
                first_name="Sofia",
                user_id=1,
            )
            st.switch_page("pages/00_Student_Home.py")

with employer_col:
    with st.container(border=True):
        st.markdown("### 💼 Marcus")
        st.caption("Employer / recruiter")
        st.write("Publish co-op roles, review skill-matched applicants, and move candidates through a clear hiring pipeline.")
        if st.button("Continue as Marcus", type="primary", use_container_width=True):
            st.session_state.update(
                authenticated=True,
                role="employer",
                first_name="Marcus",
                employer_id=1,
            )
            st.switch_page("pages/10_Employer_Home.py")

with admin_col:
    with st.container(border=True):
        st.markdown("### 🛡️ Nikki")
        st.caption("System administrator")
        st.write("Verify employers, review reported postings, manage students, and maintain a trustworthy skill taxonomy.")
        if st.button("Continue as Nikki", type="primary", use_container_width=True):
            st.session_state.update(
                authenticated=True,
                role="administrator",
                first_name="Nikki",
                admin_id=1,
            )
            st.switch_page("pages/20_Admin_Home.py")

st.divider()
metric_one, metric_two, metric_three, metric_four = st.columns(4)
metric_one.metric("Open roles", "11")
metric_two.metric("Partner employers", "35")
metric_three.metric("Student profiles", "40")
metric_four.metric("Tracked applications", "75")

st.info("These counts come from CoopTrack's current demonstration dataset. Live feature pages will connect through the Flask REST API.")
