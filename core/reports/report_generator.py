class ReportGenerator:
    """
    Generates structured, print-ready student academic performance reports.
    """

    def __init__(self):
        pass

    def generate_student_report(self, student_name, performance_data, weak_areas, quiz_history):
        """
        Compiles analytical data aggregates into a structured dictionary layout report.
        """
        total_quizzes = len(quiz_history)

        report = {
            "student_name": student_name,
            "total_quizzes": total_quizzes,
            "performance_trend": performance_data.get("trend", "Unknown"),
            "average_score": performance_data.get("average_score", 0),
            "latest_score": performance_data.get("latest_score", 0),
            "weak_areas": weak_areas if weak_areas else []
        }

        return report

    def export_markdown_summary(self, report):
        """
        Transforms a raw data report dictionary into a clean, human-readable markdown format sheet.
        """
        markdown_str = f"""
# 📋 HALIM NEXUS AI ACADEMIC REPORT
## Student Profile: {report['student_name']}
---
### 📈 Performance Metrics Summary
* **Total Evaluated Quizzes Logged:** {report['total_quizzes']}
* **Analytical Growth Trend:** {report['performance_trend']}
* **Cumulative Average Score:** {report['average_score']}%
* **Last Logged Assessment Score:** {report['latest_score']}%

### ⚠️ Flagged Weak Topics & Recommendations
"""
        if report["weak_areas"]:
            for area in report["weak_areas"]:
                # Handles both raw tuple database rows and dictionary structures safely
                if isinstance(area, dict):
                    markdown_str += f"* **Topic:** {area.get('topic')} \n  * **Recommendation:** {area.get('recommendation')}\n"
                elif isinstance(area, tuple) and len(area) >= 3:
                    markdown_str += f"* **Topic:** {area[2]} \n  * **Recommendation:** Focus on targeted conceptual revision practice via adaptive coaching history logs.\n"
        else:
            markdown_str += "* ✨ *No outstanding micro-concept weaknesses logged for this active profile tracker sequence.*\n"

        return markdown_str


if __name__ == "__main__":
    # Isolated module validation check matching your exact data parameters
    performance_data = {
        "trend": "Improving",
        "average_score": 75.0,
        "latest_score": 90.0
    }

    weak_areas = [
        {
            "topic": "Geometry",
            "recommendation": "Practice geometry diagrams and theorem structures."
        }
    ]

    quiz_history = [
        (1, 1, "Math", "Geometry", 3, 5, "2026-04-23")
    ]

    generator = ReportGenerator()
    report = generator.generate_student_report(
        student_name="Hammad",
        performance_data=performance_data,
        weak_areas=weak_areas,
        quiz_history=quiz_history
    )
    
    print("--- Compiled Report Dictionary ---")
    print(report)
    
    print("\n--- Exported Human-Readable Markdown Document ---")
    print(generator.export_markdown_summary(report))