"""Role-aware sidebar navigation for the CoopTrack Streamlit application."""

import streamlit as st


ROLE_HOME_PAGES = {
    "student": "pages/00_Student_Home.py",
    "employer": "pages/10_Employer_Home.py",
    "administrator": "pages/20_Admin_Home.py",
}


def require_role(expected_role: str) -> None:
    """Redirect unauthenticated or mismatched personas to a safe page."""
    if not st.session_state.get("authenticated", False):
        st.switch_page("Home.py")
    if st.session_state.get("role") != expected_role:
        st.error("This page is not available for the selected persona.")
        destination = ROLE_HOME_PAGES.get(st.session_state.get("role"), "Home.py")
        if st.button("Return to my dashboard", type="primary"):
            st.switch_page(destination)
        st.stop()


def _logout() -> None:
    for key in ("authenticated", "role", "first_name", "user_id", "employer_id", "admin_id"):
        st.session_state.pop(key, None)
    st.switch_page("Home.py")


def SideBarLinks(show_home: bool = False) -> None:
    """Render navigation links appropriate for the active simulated persona."""
    st.sidebar.image("assets/logo.png", width=170)

    if show_home:
        st.sidebar.page_link("Home.py", label="Choose a persona", icon="🏠")

    authenticated = st.session_state.get("authenticated", False)
    if not authenticated and not show_home:
        st.switch_page("Home.py")

    role = st.session_state.get("role")
    if authenticated and role in ROLE_HOME_PAGES:
        st.sidebar.caption(f"Signed in as {st.session_state.get('first_name', 'Guest')}")
        labels = {
            "student": ("Student dashboard", "🎓"),
            "employer": ("Employer dashboard", "💼"),
            "administrator": ("Admin dashboard", "🛡️"),
        }
        label, icon = labels[role]
        st.sidebar.page_link(ROLE_HOME_PAGES[role], label=label, icon=icon)

    st.sidebar.page_link("pages/30_About.py", label="About CoopTrack", icon="ℹ️")

    if authenticated:
        st.sidebar.divider()
        if st.sidebar.button("Log out", use_container_width=True):
            _logout()
