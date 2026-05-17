import streamlit as st
import sys
import importlib
from pathlib import Path

# Enforce absolute path anchors for deep nested imports
# ✅ FIXED: insert(0) ensures YOUR app package loads before any pip-installed 'app' conflict
project_root = Path(__file__).resolve().parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from config.settings import Settings

st.set_page_config(
    page_title="HALIM NEXUS AI",
    layout="wide"
)

st.sidebar.title("🎮 Central Infrastructure Matrix")
st.sidebar.caption("Navigation router link bypass layer")

workspace = st.sidebar.radio(
    "Select Active Portal Environment:",
    ["Student Workspace", "Teacher Workspace", "Guardian Workspace"]
)

st.sidebar.write("---")

# Route code threads seamlessly without breaking the system runtime state
if workspace == "Student Workspace":
    import app.dashboards.student_dashboard as sd
    sd.show_student_dashboard()

elif workspace == "Teacher Workspace":
    import app.dashboards.teacher_dashboard as td
    td.show_teacher_dashboard()

elif workspace == "Guardian Workspace":
    import app.dashboards.parent_dashboard as pd
    pd.show_parent_dashboard()