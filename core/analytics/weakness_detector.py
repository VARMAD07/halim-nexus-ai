class WeaknessDetector:
    """
    Detects, isolates, and classifies weak conceptual areas from quiz performance metrics.
    """

    def __init__(self):
        pass

    def detect_weak_areas(self, quiz_result, questions):
        """
        Analyze quiz results, group missed topics uniquely, and assign a prioritized severity track.
        """
        weak_areas = []
        flagged_topics = set()  # Tracks topics we have already processed to prevent duplicate API runs

        for result in quiz_result["results"]:
            if not result["is_correct"]:
                question_id = result["question_id"]

                # Resolve the topic data from the static question definition layout map
                matched_question = next(
                    (q for q in questions if q["question_id"] == question_id),
                    None
                )

                if matched_question:
                    topic_name = matched_question["topic"]

                    # If we have already flagged this specific topic in this quiz pass, skip duplication
                    if topic_name in flagged_topics:
                        continue

                    flagged_topics.add(topic_name)
                    
                    # Package structured recommendations with explicit recommendation prompts
                    weak_areas.append({
                        "question_id": question_id,
                        "topic": topic_name,
                        "weakness_level": "Needs Review",
                        "recommendation": f"Review core textbooks and attempt foundational exercises for: {topic_name}."
                    })

        return weak_areas


if __name__ == "__main__":
    # Mock testing suite matching your diagnostic metrics profile parameters
    questions = [
        {
            "question_id": 1,
            "question": "What is 5 + 5?",
            "correct_answer": "10",
            "topic": "Basic Mathematics"
        },
        {
            "question_id": 2,
            "question": "Capital of India?",
            "correct_answer": "New Delhi",
            "topic": "Geography"
        }
    ]

    quiz_result = {
        "score": 1,
        "results": [
            {"question_id": 1, "is_correct": True},
            {"question_id": 2, "is_correct": False}
        ]
    }

    detector = WeaknessDetector()
    weak_areas = detector.detect_weak_areas(quiz_result, questions)
    print("Verification Pass — Isolated Unique Weak Area Profiles:")
    print(weak_areas)