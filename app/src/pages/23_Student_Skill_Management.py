"""Administrator student-access and skill-taxonomy management."""

import pandas as pd
import streamlit as st

from modules.api_client import ApiError, delete, get, post, put
from modules.nav import SideBarLinks, require_role


st.set_page_config(page_title="Student & Skill Management · CoopTrack", page_icon="🧹", layout="wide")
require_role("administrator")
SideBarLinks()

admin_id = st.session_state["admin_id"]
st.title("Student and skill management")

try:
    students = get("/students")
    skills = get("/skills")
    demand = get("/skills/demand")
except ApiError as error:
    st.error(str(error))
    st.stop()

student_tab, skill_tab, demand_tab = st.tabs(
    ["Student accounts", "Skill taxonomy", "Skill demand"]
)
with student_tab:
    st.dataframe(pd.DataFrame(students), width="stretch", hide_index=True)
    labels = {f"#{row['student_id']} · {row['name']}": row for row in students}
    selected_label = st.selectbox("Student", labels)
    selected = labels[selected_label]
    status = st.selectbox(
        "Account status",
        ["ACTIVE", "SUSPENDED"],
        index=0 if selected["active_status"] else 1,
    )
    if st.button("Update student", type="primary"):
        try:
            put(
                f"/students/{selected['student_id']}",
                {
                    "active_status": status == "ACTIVE",
                    "admin_id": None if status == "ACTIVE" else admin_id,
                },
            )
            st.success("Student account updated.")
            st.rerun()
        except ApiError as error:
            st.error(str(error))

with skill_tab:
    st.dataframe(pd.DataFrame(skills), width="stretch", hide_index=True)
    create_col, edit_col = st.columns(2)
    with create_col:
        with st.form("create_skill"):
            st.subheader("Add a skill")
            new_skill = st.text_input("New skill name")
            create_submitted = st.form_submit_button("Add skill", type="primary")
        if create_submitted:
            if not new_skill.strip():
                st.error("Skill name is required.")
            else:
                try:
                    post("/skills", {"skill_name": new_skill.strip(), "admin_id": admin_id})
                    st.success("Skill added.")
                    st.rerun()
                except ApiError as error:
                    st.error(str(error))
    with edit_col:
        st.subheader("Edit or delete a skill")
        skill_labels = {f"#{row['skill_id']} · {row['skill_name']}": row for row in skills}
        skill_label = st.selectbox("Skill", skill_labels)
        selected_skill = skill_labels[skill_label]
        renamed = st.text_input("Canonical name", value=selected_skill["skill_name"])
        skill_status = st.selectbox(
            "Skill status",
            ["ACTIVE", "REVIEW", "RETIRED"],
            index=["ACTIVE", "REVIEW", "RETIRED"].index(selected_skill["skill_status"])
            if selected_skill["skill_status"] in {"ACTIVE", "REVIEW", "RETIRED"}
            else 0,
        )
        if st.button("Save skill changes"):
            try:
                put(
                    f"/skills/{selected_skill['skill_id']}",
                    {"skill_name": renamed.strip(), "skill_status": skill_status},
                )
                st.success("Skill updated.")
                st.rerun()
            except ApiError as error:
                st.error(str(error))
        confirm_delete = st.checkbox("Delete this skill if it is unused.")
        if st.button("Delete unused skill", disabled=not confirm_delete):
            try:
                delete(f"/skills/{selected_skill['skill_id']}")
                st.success("Unused skill deleted.")
                st.rerun()
            except ApiError as error:
                st.error(str(error))

with demand_tab:
    st.write("Skills ranked by the number of position postings that require them.")
    st.dataframe(pd.DataFrame(demand), width="stretch", hide_index=True)
