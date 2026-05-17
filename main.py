import streamlit as st
import sys
import importlib
from pathlib import Path

# ✅ STEP 1 — ALWAYS FIRST: set up sys.path before ANY custom imports
project_root = Path(__file__).resolve().parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# ✅ STEP 2 — Now safe to import custom modules
from database.storage.db_manager import DatabaseManager

# ✅ STEP 3 — Auto-initialize database on every cold start
_db = DatabaseManager()
_db.create_tables()

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

if workspace == "Student Workspace":
    import app.dashboards.student_dashboard as sd
    sd.show_student_dashboard()

elif workspace == "Teacher Workspace":
    import app.dashboards.teacher_dashboard as td
    td.show_teacher_dashboard()

elif workspace == "Guardian Workspace":
    import app.dashboards.parent_dashboard as pd
    pd.show_parent_dashboard()