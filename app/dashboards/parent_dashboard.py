import streamlit as st
import sys
from pathlib import Path

# Set up absolute pathing for seamless imports
current_file = Path(__file__).resolve()
project_root = current_file.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

from database.storage.db_manager import DatabaseManager
from core.analytics.performance_tracker import PerformanceTracker
from core.reports.report_generator import ReportGenerator

# Instantiate the backend managers
db = DatabaseManager()
performance_tracker = PerformanceTracker()
report_generator = ReportGenerator()

def show_parent_dashboard():
    # Auto-patch the database schema if the column is missing
    try:
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT parent_binding FROM students LIMIT 1")
        db.close_connection()
    except Exception:
        try:
            conn = db.connect()
            cursor = conn.cursor()
            cursor.execute("ALTER TABLE students ADD COLUMN parent_binding TEXT DEFAULT 'Unlinked'")
            conn.commit()
        except Exception:
            pass
        finally:
            db.close_connection()

    # =====================================
    # PREMIUM MAIN HEADER
    # =====================================
    st.markdown("<h1 style='text-align: center; color: #00E676; letter-spacing: 2px;'>👪 HALIM NEXUS AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #8892B0; font-size: 1.2rem; margin-bottom: 2rem;'>Guardian Oversight & Analytics Portal</p>", unsafe_allow_html=True)
    st.write("---")

    # 🔐 Premium Mobile Authentication Layer
    col_login1, col_login2, col_login3 = st.columns([1, 2, 1])
    with col_login2:
        with st.form("guardian_login_form"):
            st.markdown("### 🔐 Secure Mobile Access")
            # Ask for the phone number instead of the name token
            parent_mobile_auth = st.text_input("Enter Registered Mobile Number:", placeholder="+919876543210")
            submit_search = st.form_submit_button("Authenticate & Load Dashboard", use_container_width=True)
        
    st.write("---")

    # Use the brand new database method we just created!
    all_students = db.fetch_students_by_mobile(parent_mobile_auth)

    if not all_students:
        st.info("ℹ️ **Awaiting Authentication:** Please enter your registered mobile number above to view your linked children's academic profiles.")
    else:
        # Build dropdown mapping for active linked child profiles
        st.markdown("### 👤 Select Profile")
        student_options = {f"{student[1]} (Class {student[2]}-{student[3]})": student for student in all_students}
        selected_profile = st.selectbox("Active Roster:", list(student_options.keys()), label_visibility="collapsed")
        
        target_student = student_options[selected_profile]
        child_id = target_student[0]
        child_name = target_student[1]
        
        st.write("---")
        
        quiz_history = db.fetch_quiz_results(child_id)
        ai_coaching_logs = db.fetch_ai_coaching(child_id)
        
        if quiz_history:
            performance_data = performance_tracker.analyze_progress(quiz_history)
        else:
            performance_data = {
                "trend": "Initial Baseline Established",
                "average_score": 0,
                "latest_score": 0
            }
        
        tab_overview, tab_coaching, tab_report = st.tabs([
            "📈 Learning Growth Tracking",
            "🤖 AI Coaching History",
            "📄 Official Progress Report"
        ])
        
        # -----------------------------------------
        # TAB 1: OVERVIEW
        # -----------------------------------------
        with tab_overview:
            st.markdown("#### 🎯 Core Vitality Metrics")
            st.markdown("<br>", unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(label="📈 Growth Trend", value=performance_data.get("trend", "Stable"))
            with col2:
                st.metric(label="🎯 Cumulative Average", value=f"{performance_data.get('average_score', 0)}%")
            with col3:
                # Calculate Delta for visual flair if multiple quizzes exist
                delta_val = None
                if quiz_history and len(quiz_history) > 1:
                    sorted_scores = sorted(quiz_history, key=lambda x: x[6])
                    last_score = (sorted_scores[-1][4] / sorted_scores[-1][5]) * 100
                    prev_score = (sorted_scores[-2][4] / sorted_scores[-2][5]) * 100
                    delta_val = f"{last_score - prev_score:.1f}%"
                    
                st.metric(label="⚡ Latest Score", value=f"{performance_data.get('latest_score', 0)}%", delta=delta_val)
            
            st.write("---")
            
            col_chart, col_details = st.columns([2, 1])
            with col_chart:
                st.subheader("📉 Score Progression Timeline")
                st.caption("Visual tracking of your child's academic velocity.")
                
                if quiz_history:
                    chronological_history = sorted(quiz_history, key=lambda x: x[6])
                    chart_data = [(row[4] / row[5]) * 100 for row in chronological_history]
                    st.line_chart(data=chart_data, use_container_width=True)
                else:
                    st.warning(f"✨ {child_name} hasn't completed any tracked quiz evaluations yet.")

            with col_details:
                st.subheader("Recent Activity")
                st.caption("Latest evaluation logs")
                if quiz_history:
                    recent_history = sorted(quiz_history, key=lambda x: x[6])[-3:]
                    for row in reversed(recent_history):
                        percentage = (row[4] / row[5]) * 100
                        st.info(f"**{row[3]}**\n\nScore: {percentage:.0f}%")
                else:
                    st.info("Awaiting initial baseline data.")

        # -----------------------------------------
        # TAB 2: AI COACHING
        # -----------------------------------------
        with tab_coaching:
            st.markdown("#### 🧠 Persistent AI Assistant Memory")
            st.markdown("<p style='color: #8892B0;'>Automated interventions deployed to correct foundational misunderstandings.</p>", unsafe_allow_html=True)
            
            if ai_coaching_logs:
                for log in ai_coaching_logs:
                    with st.expander(f"🔍 Flagged Weakness: {log[2]} | 📅 {log[4]}"):
                        st.markdown("##### AI Tutor Feedback:")
                        st.info(log[3])
            else:
                st.success(f"✨ Clear Slate: No conceptual friction points currently flagged for {child_name}.")

        # -----------------------------------------
        # TAB 3: REPORTS
        # -----------------------------------------
        with tab_report:
            st.markdown("#### 📋 Official Term Summary Document")
            st.caption("Auto-generated, printable progress sheet.")
            report = report_generator.generate_student_report(
                student_name=child_name,
                performance_data=performance_data,
                weak_areas=ai_coaching_logs,
                quiz_history=quiz_history
            )
            st.markdown(report_generator.export_markdown_summary(report))

if __name__ == "__main__":
    show_parent_dashboard()