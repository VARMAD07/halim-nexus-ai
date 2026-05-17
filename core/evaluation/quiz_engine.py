# Rebuild core/evaluation/quiz_engine.py cleanly with the correct class definition
class QuizEngine:
    """
    Handles student quiz input validation and evaluation metrics processing.
    """

    def __init__(self):
        pass

    def evaluate_quiz(self, questions, student_answers):
        """
        Evaluate student responses against correct answers with string normalization.
        """
        score = 0
        results = []

        for question in questions:
            question_id = question["question_id"]
            correct_answer = str(question["correct_answer"]).strip().lower()

            raw_student_answer = student_answers.get(question_id)
            student_answer = str(raw_student_answer).strip().lower() if raw_student_answer is not None else ""

            is_correct = student_answer == correct_answer

            if is_correct:
                score += 1

            results.append({
                "question_id": question_id,
                "student_answer": raw_student_answer,
                "correct_answer": question["correct_answer"],
                "is_correct": is_correct
            })

        return {
            "score": score,
            "total_questions": len(questions),
            "results": results
        }


if __name__ == "__main__":
    questions = [
        {
            "question_id": 1,
            "question": "What is 2 + 2?",
            "correct_answer": "4"
        },
        {
            "question_id": 2,
            "question": "Capital of India?",
            "correct_answer": "New Delhi"
        }
    ]

    student_answers = {
        1: "4 ",
        2: "new delhi"
    }

    engine = QuizEngine()
    result = engine.evaluate_quiz(questions, student_answers)
    print("Verification Pass — Normalized Evaluation Results Output:")
    print(result)