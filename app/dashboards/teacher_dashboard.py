import streamlit as st
import sys
from pathlib import Path

# Set up system paths for modular resolution absolute to the project root
current_file = Path(__file__).resolve()
project_root = current_file.parent.parent.parent

# ✅ FIXED: insert(0) ensures project root takes priority over conflicting pip packages
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from database.storage.db_manager import DatabaseManager
from .notifier import NotifieryEngine

# Initialize backend engines
db = DatabaseManager()
notifier = NotifieryEngine()

def show_teacher_dashboard():
    # =====================================
    # PREMIUM MAIN HEADER
    # =====================================
    st.markdown("<h1 style='text-align: center; color: #00E676; letter-spacing: 2px;'>👨‍🏫 HALIM NEXUS AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #8892B0; font-size: 1.2rem; margin-bottom: 2rem;'>Educator Control & Broadcast Matrix</p>", unsafe_allow_html=True)
    st.write("---")

    # =====================================
    # SIDEBAR CONTROL MATRIX
    # =====================================
    with st.sidebar:
        st.markdown("### ⚙️ Command Console")
        st.caption("Instructor Navigation")
        st.write("---")

        st.markdown("#### 🧭 Core Modules")
        section = st.radio(
            "Select Destination",
            [
                "Class Roster Overview",
                "Smart Attendance & SMS",
                "System Broadcasts"
            ],
            label_visibility="collapsed"
        )

    all_students = db.fetch_all_students()

    # =====================================
    # MODULE: CLASS ROSTER
    # =====================================
    if section == "Class Roster Overview":
        st.markdown("## 📋 Active Cohort Overview")
        st.markdown("<p style='color: #8892B0;'>High-level view of all registered student profiles.</p>", unsafe_allow_html=True)

        if not all_students:
            st.warning("No students registered in the database.")
        else:
            for student in all_students:
                with st.container():
                    col1, col2, col3 = st.columns([1, 2, 2])
                    with col1:
                        st.caption("System ID")
                        st.write(f"`{student[0]}`")
                    with col2:
                        st.caption("Student Name")
                        st.write(f"**{student[1]}**")
                    with col3:
                        st.caption("Placement")
                        st.write(f"Class {student[2]} - Sec {student[3]}")
                    st.write("---")

    # =====================================
    # MODULE: SMART ATTENDANCE
    # =====================================
    elif section == "Smart Attendance & SMS":
        st.markdown("## 📡 Exception-Based Attendance")
        st.markdown("<p style='color: #8892B0;'>All students default to Present. Only flag absentees to trigger automated parent SMS alerts.</p>", unsafe_allow_html=True)
        st.write("---")

        if not all_students:
            st.warning("No students available for attendance tracking.")
        else:
            with st.form("attendance_form"):
                st.subheader("Today's Roster")

                absent_flags = {}
                for student in all_students:
                    student_id = student[0]
                    student_name = student[1]
                    absent_flags[student_id] = st.checkbox(f"Flag **{student_name}** as ABSENT", key=f"abs_{student_id}")

                st.write("---")
                submit_attendance = st.form_submit_button("Submit Attendance & Fire Alerts", type="primary")

                if submit_attendance:
                    absent_count = 0
                    with st.spinner("Processing attendance matrix and waking SMS engine..."):
                        for student in all_students:
                            s_id = student[0]
                            s_name = student[1]

                            if absent_flags[s_id]:
                                absent_count += 1

                                # ✅ FIXED: Use the dedicated db method (correct column name, clean & safe)
                                real_parent_mobile = db.fetch_student_parent_mobile(s_id)

                                # FIRE THE SMS ENGINE!
                                notifier.send_sms_alert(real_parent_mobile, s_name, alert_type="attendance")
                                st.error(f"🔴 Marked Absent: {s_name} (SMS Alert Dispatched)")

                    if absent_count == 0:
                        st.success("✅ 100% Attendance recorded. No SMS alerts required.")
                    else:
                        st.success(f"✅ Attendance logged. {absent_count} absentee SMS alerts successfully routed.")

    # =====================================
    # MODULE: SYSTEM BROADCASTS
    # =====================================
    elif section == "System Broadcasts":
        st.markdown("## 📢 Urgent Mass Broadcast")
        st.info("Coming soon: Type one message here to instantly SMS every parent in the selected class section.")

if __name__ == "__main__":
    show_teacher_dashboard()