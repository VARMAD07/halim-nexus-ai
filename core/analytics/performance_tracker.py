class PerformanceTracker:
    """
    Tracks, calculates, and trends student performance scores over time.
    """

    def __init__(self):
        pass

    def analyze_progress(self, quiz_history):
        """
        Analyze percentage score metrics securely, guaranteeing proper chronological orientation.
        """
        # If the student hasn't taken any quizzes yet, return an informational fallback framework
        if not quiz_history or len(quiz_history) == 0:
            return {
                "status": "No historical evaluation records mapped to this profile.",
                "average_score": 0,
                "latest_score": 0
            }

        # Step 1: Ensure scores are chronological (Oldest to Newest)
        # We sort based on the quiz_date string field (index 6 in the quiz_results record row)
        chronological_history = sorted(quiz_history, key=lambda x: x[6])

        scores = []
        for result in chronological_history:
            score = result[4]
            total_marks = result[5]
            percentage = (score / total_marks) * 100
            scores.append(percentage)

        average_score = sum(scores) / len(scores)

        # Handle the edge case of exactly 1 quiz gracefully instead of throwing a generic error flag
        if len(scores) == 1:
            return {
                "trend": "Stable (Initial Baseline Established)",
                "average_score": round(average_score, 2),
                "latest_score": round(scores[0], 2)
            }

        # Step 2: Now that the array is sorted, our indices map perfectly to reality
        first_score = scores[0]
        latest_score = scores[-1]

        if latest_score > first_score:
            trend = "Improving"
        elif latest_score < first_score:
            trend = "Declining"
        else:
            trend = "Stable"

        return {
            "trend": trend,
            "average_score": round(average_score, 2),
            "latest_score": round(latest_score, 2)
        }


if __name__ == "__main__":
    # Rapid verification suite simulating an inverted date arrival timeline
    sample_history = [
        (3, 1, "Science", "Physics", 5, 5, "2026-04-22"),
        (2, 1, "Math", "Geometry", 4, 5, "2026-04-21"),
        (1, 1, "Math", "Algebra", 2, 5, "2026-04-20")
    ]

    tracker = PerformanceTracker()
    analysis = tracker.analyze_progress(sample_history)
    print("Verification Pass — Calculated Metrics Breakdown:")
    print(analysis)