import streamlit as st
import sys
from pathlib import Path
from datetime import datetime

# Set up system paths for modular resolution absolute to the project root
root_path = Path(__file__).parent.parent.parent.parent
if str(root_path) not in sys.path:
    sys.path.append(str(root_path))

from database.storage.db_manager import DatabaseManager
from core.evaluation.quiz_engine import QuizEngine
from core.analytics.weakness_detector import WeaknessDetector
from core.analytics.performance_tracker import PerformanceTracker
from core.reports.report_generator import ReportGenerator
from core.ai_engine.ai_tutor import AITutor
from app.dashboards.notifier import NotificationEngine

# Initialize it with your other engines (around line 26)
notifier = NotificationEngine()

# =====================================
# INITIALIZATION (OUTSIDE FUNCTION)
# =====================================
db = DatabaseManager()
quiz_engine = QuizEngine()
weakness_detector = WeaknessDetector()
performance_tracker = PerformanceTracker()
report_generator = ReportGenerator()
ai_tutor = AITutor()

# =====================================
# SCHEMA SELF-HEALING MIGRATIONS
# (add missing columns if they don't exist yet)
# =====================================
try:
    conn = db.connect()
    cursor = conn.cursor()
    cursor.execute("ALTER TABLE students ADD COLUMN student_email TEXT DEFAULT 'None'")
    cursor.execute("ALTER TABLE students ADD COLUMN parent_email TEXT DEFAULT 'None'")
    cursor.execute("ALTER TABLE students ADD COLUMN parent_mobile TEXT DEFAULT 'None'")
    conn.commit()
except Exception:
    pass
finally:
    db.close_connection()

def show_student_dashboard():
    # Initialize Session State tracking parameters safely
    if "active_student_id" not in st.session_state:
        st.session_state.active_student_id = None
    if "active_student_name" not in st.session_state:
        st.session_state.active_student_name = ""

    # =====================================
    # PREMIUM MAIN HEADER
    # =====================================
    st.markdown("<h1 style='text-align: center; color: #00E676; letter-spacing: 2px;'>🎓 HALIM NEXUS AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #8892B0; font-size: 1.2rem; margin-bottom: 2rem;'>Student Performance & Analytics Command Center</p>", unsafe_allow_html=True)
    st.write("---")
    
    # =====================================
    # PREMIUM SIDEBAR CONTROL MATRIX
    # =====================================
    with st.sidebar:
        st.markdown("### ⚙️ System Control")
        st.caption("AI-Powered Navigation Matrix")
        st.write("---")
        
        # Global Dynamic Profile Selector
        st.markdown("#### 👤 Active Profile")
        students_list = db.fetch_all_students()
        
        if st.session_state.active_student_id is None:
            st.warning("No profile activated.")
            if students_list:
                # Dropdown choice to switch profiles dynamically
                student_options = {f"{s[1]} (ID: {s[0]})": s for s in students_list}
                selected_option = st.selectbox("Select Student:", ["-- Select --"] + list(student_options.keys()))
                
                if selected_option != "-- Select --":
                    matched_student = student_options[selected_option]
                    st.session_state.active_student_id = matched_student[0]
                    st.session_state.active_student_name = matched_student[1]
                    st.rerun()
            else:
                st.info("Go to 'Student Registration' to initialize.")
        else:
            st.success(f"**{st.session_state.active_student_name}**")
            st.caption(f"Database ID Trace: `{st.session_state.active_student_id}`")
            if st.button("🔄 Swap Profile", use_container_width=True):
                st.session_state.active_student_id = None
                st.session_state.active_student_name = ""
                st.rerun()

        st.write("---")
        st.markdown("#### 🧭 Core Modules")
        section = st.radio(
            "Select Destination",
            [
                "Student Registration",
                "Quiz System",
                "Performance Analytics",
                "Reports",
                "AI Learning Assistant",
                "AI Coaching History"
            ],
            label_visibility="collapsed"
        )

    # Extract active session references
    active_id = st.session_state.active_student_id
    active_name = st.session_state.active_student_name

    # =====================================
    # STUDENT REGISTRATION
    # =====================================
    if section == "Student Registration":
        st.header("Student Registration")

        with st.form("student_form"):
            full_name = st.text_input("Student Full Name")
            class_name = st.text_input("Class")
            section_name = st.text_input("Section")
            
            # --- UPGRADED INPUTS ---
            parent_mobile = st.text_input("Parent Mobile Number (e.g., +919876543210)")
            parent_email = st.text_input("Parent Email Address (Optional)")
            
            submit_button = st.form_submit_button("Register Student")

        if submit_button:
            if full_name.strip() and class_name.strip() and parent_mobile.strip():
                # Make sure your db.add_student call passes these new variables!
                db.add_student(
                    full_name=full_name.strip(), 
                    class_name=class_name.strip(), 
                    section=section_name.strip(), 
                    parent_mobile=parent_mobile.strip(),
                    parent_email=parent_email.strip()
                )
                st.success(f"Profile securely mapped to mobile ID: '{parent_mobile.strip()}'!")
            else:
                st.error("Please fill in all required fields (Name, Class, Mobile) before submitting.")

        st.divider()
        st.subheader("Registered Students Ecosystem")
        
        # Fetch fresh list of students
        updated_students_list = db.fetch_all_students()
        if updated_students_list:
            for student in updated_students_list:
                st.info(f"**ID:** {student[0]} | **Name:** {student[1]} | **Class:** {student[2]} | **Section:** {student[3]}")
        else:
            st.warning("No student records found in local SQLite engine repository.")

    # =====================================
    # QUIZ SYSTEM
    # =====================================
    elif section == "Quiz System":
        st.header("Quiz Evaluation System")

        if active_id is None:
            st.warning("⚠️ Action Required: Please select an active student profile from the sidebar panel before attempting quizzes.")
        else:
            questions = [
                {
                    "question_id": 1,
                    "question": "What is 5 + 5?",
                    "correct_answer": "10",
                    "topic": "Basic Mathematics"
                },
                {
                    "question_id": 2,
                    "question": "What is the capital of India?",
                    "correct_answer": "New Delhi",
                    "topic": "Geography"
                }
            ]

            with st.form("quiz_form"):
                answer_1 = st.text_input("1. What is 5 + 5?")
                answer_2 = st.text_input("2. What is the capital of India?")
                submit_quiz = st.form_submit_button("Submit Quiz")

                if submit_quiz:
                    student_answers = {
                        1: answer_1.strip(),
                        2: answer_2.strip()
                    }

                    result = quiz_engine.evaluate_quiz(questions, student_answers)
                    
                    # Automated execution date timestamping
                    current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    db.save_quiz_result(
                        student_id=active_id,
                        subject="General Knowledge",
                        topic="Mixed Topics",
                        score=result["score"],
                        total_marks=result["total_questions"],
                        quiz_date=current_timestamp
                    )
                    db.save_quiz_result(
                        student_id=active_id,
                        subject="General Knowledge",
                        topic="Mixed Topics",
                        score=result["score"],
                        total_marks=result["total_questions"],
                        quiz_date=current_timestamp
                    )

                    # --- NEW: FIRE THE NOTIFICATION ENGINE ---
                    # Fetch the student's profile to get the parent's email
                    student_data = db.fetch_students_by_parent(st.session_state.active_student_name) # simplified fetch
                    # For testing, we will just use a hardcoded test email to prove it works!
                    test_parent_email = "test_parent@gmail.com" 
                    
                    notifier.send_quiz_alert_email(
                        parent_email=test_parent_email, 
                        student_name=active_name, 
                        score=result["score"], 
                        total=result["total_questions"]
                    )
                    # -----------------------------------------

                    st.success(f"🎉 Quiz Evaluated! Final Score: {result['score']} / {result['total_questions']}")

                    st.subheader("Detailed Evaluation Breakdown")
                    for item in result["results"]:
                        if item["is_correct"]:
                            st.success(f"🟢 Question {item['question_id']}: Correct")
                        else:
                            st.error(f"🔴 Question {item['question_id']}: Incorrect\n* Your Answer: {item['student_answer']}\n* Correct Answer: {item['correct_answer']}")

                    st.subheader("Weak Area Analysis")
                    weak_areas = weakness_detector.detect_weak_areas(result, questions)

                    if weak_areas:
                        for area in weak_areas:
                            st.warning(f"**Weak Topic Detected:** {area['topic']}\n\n**Recommendation Optimization:** {area['recommendation']}")

                            with st.spinner(f"Initiating Google GenAI SDK interface orchestration for {area['topic']}..."):
                                coaching = ai_tutor.generate_weakness_coaching(area['topic'])
                                
                                db.save_ai_coaching(
                                    student_id=active_id,
                                    weak_topic=area['topic'],
                                    ai_feedback=coaching,
                                    created_date=current_timestamp
                                )

                            st.markdown("### 🤖 AI Improvement Coach Guidance")
                            st.info(coaching)
                    else:
                        st.success("Excellent performance. No explicit structural weak areas detected from this test run sequence.")

# =====================================
    # PERFORMANCE ANALYTICS (PREMIUM UI)
    # =====================================
    elif section == "Performance Analytics":
        st.markdown("## 📊 Performance Analytics Command Center")
        st.markdown("<p style='color: #8892B0; font-size: 1.1rem;'>Real-time telemetry and historical growth vectors.</p>", unsafe_allow_html=True)
        st.write("---")

        if active_id is None:
            st.info("💡 **Pro Tip:** Select a student profile from the sidebar to populate this dashboard.")
        else:
            quiz_results = db.fetch_quiz_results(active_id)
            performance_data = performance_tracker.analyze_progress(quiz_results)

            if "trend" in performance_data:
                # 🏆 Premium Top Metric Row
                st.markdown("#### 🎯 Core Vitality Metrics")
                st.markdown("<br>", unsafe_allow_html=True) # Spacer
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric(label="📈 Growth Trend", value=performance_data["trend"])
                with col2:
                    st.metric(label="🎯 Cumulative Average", value=f"{performance_data['average_score']}%")
                with col3:
                    # Calculate a simulated 'delta' (change) for visual effect if we have more than 1 quiz
                    delta_val = None
                    if len(quiz_results) > 1:
                        sorted_scores = sorted(quiz_results, key=lambda x: x[6])
                        last_score = (sorted_scores[-1][4] / sorted_scores[-1][5]) * 100
                        prev_score = (sorted_scores[-2][4] / sorted_scores[-2][5]) * 100
                        delta_val = f"{last_score - prev_score:.1f}%"

                    st.metric(label="⚡ Latest Score", value=f"{performance_data['latest_score']}%", delta=delta_val)
                with col4:
                    st.metric(label="📝 Total Evaluations", value=len(quiz_results))
                
                st.write("---")
                
                # 📈 Premium Chart Layout
                col_chart, col_details = st.columns([2, 1]) # 2/3 width for chart, 1/3 for details
                
                with col_chart:
                    st.subheader("📉 Score Progression Timeline")
                    st.caption("Visual tracking mapping score percentage trends.")
                    
                    chronological_history = sorted(quiz_results, key=lambda x: x[6])
                    chart_data = []
                    
                    for row in chronological_history:
                        score = row[4]
                        total_marks = row[5]
                        percentage = (score / total_marks) * 100
                        chart_data.append(percentage)
                    
                    st.line_chart(data=chart_data, use_container_width=True)
                
                with col_details:
                    st.subheader("Recent Activity")
                    st.caption("Last 3 evaluations")
                    # Show only the last 3 quizzes in a clean list
                    recent_history = chronological_history[-3:]
                    for row in reversed(recent_history):
                        percentage = (row[4] / row[5]) * 100
                        st.info(f"**{row[3]}**\n\nScore: {percentage:.0f}%")
                        
            else:
                st.warning("No performance metrics present yet. Complete a quiz to generate data.")

    # =====================================
    # REPORTS
    # =====================================
    elif section == "Reports":
        st.header("Student Performance Comprehensive Summarizer Reports")

        if active_id is None:
            st.warning("⚠️ Please choose an active student context frame profile row to build automated report summary cards.")
        else:
            quiz_results = db.fetch_quiz_results(active_id)
            ai_coaching_logs = db.fetch_ai_coaching(active_id)
            performance_data = performance_tracker.analyze_progress(quiz_results)

            report = report_generator.generate_student_report(
                student_name=active_name,
                performance_data=performance_data,
                weak_areas=ai_coaching_logs,
                quiz_history=quiz_results
            )

            st.success("Adaptive Performance Report Compiling Block Finalized.")
            
            col_r1, col_r2 = st.columns(2)
            with col_r1:
                st.metric("Total Quizzes Logged", f"{report['total_quizzes']} Submissions")
                st.metric("Analytical Growth Trend", report['performance_trend'])
            with col_r2:
                st.metric("Average Score Grade", f"{report['average_score']}%")
                st.metric("Last Active Score Logged", f"{report['latest_score']}%")
                
            st.write("---")
            st.subheader("📄 Generated Academic Sheet Document")
            
            markdown_document = report_generator.export_markdown_summary(report)
            st.markdown(markdown_document)

    # =====================================
    # AI LEARNING ASSISTANT
    # =====================================
    elif section == "AI Learning Assistant":
        st.header("AI Learning Assistant Hub")

        topic = st.text_input("Enter Topic Name (e.g., Quantum Mechanics, Organic Reactions)")

        if st.button("Generate Explanation", use_container_width=True):
            if topic.strip():
                with st.spinner("Contacting Live Google GenAI SDK Endpoint Matrix via gemini-2.5-flash..."):
                    response = ai_tutor.generate_topic_explanation(topic.strip())
                st.success("AI Content Module Compilation Successful.")
                st.markdown("## 📖 Detailed Structural AI Lesson Output")
                st.write(response)
            else:
                st.error("Please enter a valid topic phrase constraint target.")

    # =====================================
    # AI COACHING HISTORY
    # =====================================
    elif section == "AI Coaching History":
        st.header("AI Coaching Adaptive Interventions Log Matrix")

        if active_id is None:
            st.warning("⚠️ Access Restriction: Activate an account profile from the left-hand rail to load persistent coaching memory logs.")
        else:
            coaching_history = db.fetch_ai_coaching(active_id)

            if coaching_history:
                st.write(f"Displaying historical records tracked for student session user: **{active_name}**")
                for coaching in coaching_history:
                    st.markdown("---")
                    st.subheader(f"🔍 Evaluated Weak Topic Target: {coaching[2]}")
                    st.caption(f"📅 Logging Timestamp Marker: {coaching[4]}")
                    st.markdown("#### Retained Tutor Context Response Frame:")
                    st.info(coaching[3])
            else:
                st.warning("No persistent intervention coaching memory sequences have been recorded for this specific profile row instance yet.")

if __name__ == "__main__":
    show_student_dashboard()