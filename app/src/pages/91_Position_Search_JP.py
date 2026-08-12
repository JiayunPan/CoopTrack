"""
Position Search — live page backed by the CoopTrack REST API.
Author: Jiayun Pan
Calls GET /positions on the Flask API and shows real data.
"""

import streamlit as st
import requests
import pandas as pd

# Inside Docker, the Streamlit container reaches the API by its
# service name "web-api" on port 4000 (not localhost).
API_BASE = "http://web-api:4000"

st.set_page_config(page_title="Position Search · CoopTrack", page_icon="🔎")

st.title("🔎 Position Search")
st.caption("Live data from the CoopTrack REST API (GET /positions)")

# --- Search filters ---
query_col, status_col = st.columns([2, 1])
keyword = query_col.text_input("Search by title", placeholder="e.g. Software Engineer")
status = status_col.selectbox("Status", ["All", "OPEN", "CLOSED"])

# --- Call the API ---
try:
    params = {}
    if keyword:
        params["role"] = keyword
    if status != "All":
        params["status"] = status

    response = requests.get(f"{API_BASE}/positions", params=params, timeout=5)

    if response.status_code == 200:
        positions = response.json()
        st.metric("Matching positions", len(positions))

        if positions:
            df = pd.DataFrame(positions)
            st.dataframe(df, width="stretch", hide_index=True)
        else:
            st.info("No positions match your search. Try different filters.")
    else:
        st.error(f"API returned status {response.status_code}")

except requests.exceptions.RequestException as e:
    st.error(f"Could not reach the API: {e}")