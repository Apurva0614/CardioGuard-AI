"""ECG multi-agent triage: Streamlit frontend. A thin client of the API service.

Run (with the API running):  streamlit run frontend/app.py      env: API_URL (default http://127.0.0.1:8000)

How Streamlit works, in one paragraph: the script runs top to bottom on every interaction (a click, a typed
question) and redraws the page. Anything that must survive a rerun lives in ``st.session_state``. A
``@st.fragment(run_every=...)`` re-runs just one part of the page on a timer, which is how the live agent trace
updates without redrawing everything else.
"""
from pathlib import Path

import streamlit as st

import api
import ui

st.set_page_config(page_title="CARDIOGUARD", layout="wide")

# Hide Streamlit header, footer, and 'Hosted on Streamlit' branding
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.viewerBadge_container__1QSob {display: none !important;}
[data-testid="stStatusWidget"] {display: none !important;}
footer {display: none !important;}
div[class*="viewerBadge"] {display: none !important;}
</style>
""", unsafe_allow_html=True)

# Page files are located from this file, not from the entry script
VIEWS = Path(__file__).resolve().parent / "views"
ui.PAGES = {
    "worklist": st.Page(VIEWS / "worklist.py", title="Worklist", default=True),
    "run": st.Page(VIEWS / "run.py", title="Recording", url_path="run"),
}
pages = st.navigation(list(ui.PAGES.values()))

with st.sidebar:
    st.markdown("### CARDIOGUARD")
    st.caption(ui.DISCLAIMER)
    try:
        st.session_state["status"] = api.status()
    except api.ApiError:
        st.session_state["status"] = None
    s = st.session_state["status"]
    if s:
        st.caption(f"Receiver: **{s['receiver']}** · planner: {s['planner']} · questions: {s['classifier']}"
                   f" · uploads: {'on' if s['uploads'] else 'off'}")

pages.run()

