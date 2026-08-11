"""Administrator shell for managing student access and skill taxonomy."""

import pandas as pd
import streamlit as st

from modules.mock_data import SKILLS, STUDENTS
from modules.nav import SideBarLinks, require_role


st.set_page_config(page_title="Student & Skill Management · CoopTrack", page_icon="🧹", layout="wide")
require_role("administrator")
SideBarLinks()

st.title("Student and skill management")
st.caption("Administrator feature shell · REST API integration pending")

student_tab, skill_tab = st.tabs(["Student accounts", "Skill taxonomy"])
with student_tab:
    st.dataframe(pd.DataFrame(STUDENTS), width="stretch", hide_index=True)
    st.selectbox("Student", [row["Student"] for row in STUDENTS])
    st.selectbox("Account status", ["ACTIVE", "SUSPENDED"])
    st.button("Update student", type="primary", disabled=True)
    st.caption("This action will use the student PUT route.")

with skill_tab:
    st.dataframe(pd.DataFrame(SKILLS), width="stretch", hide_index=True)
    action = st.selectbox("Action", ["Add a skill", "Rename a skill", "Merge duplicate skills", "Retire a skill"])
    st.text_input("Skill name", placeholder="Enter the canonical skill name")
    st.button("Apply skill change", type="primary", disabled=True)
    st.caption(f"Selected shell action: {action}. Final behavior will use the skill POST, PUT, or DELETE route.")
