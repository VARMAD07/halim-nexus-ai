import sqlite3
from pathlib import Path

DATABASE_PATH = Path(__file__).parent.parent.parent / "data" / "halim_nexus.db"

class DatabaseManager:
    def __init__(self):
        self.connection = None
        DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    def connect(self):
        self.connection = sqlite3.connect(str(DATABASE_PATH))
        return self.connection

    def close_connection(self):
        if self.connection:
            self.connection.close()

    def create_tables(self):
        connection = self.connect()
        cursor = connection.cursor()

        # FIXED SCHEMA: Injected parent_mobile and parent_email directly into the initialization layer
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            class_name TEXT NOT NULL,
            section TEXT NOT NULL,
            parent_mobile TEXT DEFAULT 'None',
            parent_email TEXT DEFAULT 'None',
            parent_binding TEXT DEFAULT 'Unlinked'
        )""")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS quiz_results (
            result_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            subject TEXT NOT NULL,
            topic TEXT NOT NULL,
            score INTEGER NOT NULL,
            total_marks INTEGER NOT NULL,
            quiz_date TEXT NOT NULL,
            FOREIGN KEY(student_id) REFERENCES students (student_id)
        )""")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS weak_areas (
            weak_area_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            topic TEXT NOT NULL,
            weakness_level TEXT NOT NULL,
            recommendation TEXT,
            FOREIGN KEY(student_id) REFERENCES students (student_id)
        )""")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS ai_coaching (
            coaching_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            weak_topic TEXT NOT NULL,
            ai_feedback TEXT NOT NULL,
            created_date TEXT NOT NULL,
            FOREIGN KEY(student_id) REFERENCES students (student_id)
        )""")

        connection.commit()
        self.close_connection()

    def add_student(self, full_name, class_name, section, parent_mobile="None", parent_email="None"):
        """Registers a new student and securely binds their parent contact info."""
        connection = self.connect()
        cursor = connection.cursor()
        
        cursor.execute(
            """
            INSERT INTO students (full_name, class_name, section, parent_mobile, parent_email) 
            VALUES (?, ?, ?, ?, ?)
            """, 
            (full_name, class_name, section, parent_mobile, parent_email)
        )
        
        connection.commit()
        self.close_connection()

    def fetch_students_by_parent(self, parent_token):
        connection = self.connect()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM students WHERE parent_binding = ?", (parent_token,))
        res = cursor.fetchall()
        self.close_connection()
        return res

    def fetch_all_students(self):
        connection = self.connect()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM students")
        res = cursor.fetchall()
        self.close_connection()
        return res

    def fetch_student_by_id(self, student_id):
        """Fetches the complete profile array for a specific student_id."""
        connection = self.connect()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM students WHERE student_id = ?", (student_id,))
        res = cursor.fetchone()
        self.close_connection()
        return res

    def fetch_student_parent_mobile(self, student_id):
        """Fetches the parent mobile number for a specific student_id."""
        connection = self.connect()
        cursor = connection.cursor()
        cursor.execute("SELECT parent_mobile FROM students WHERE student_id = ?", (student_id,))
        result = cursor.fetchone()
        self.close_connection()
        return result[0] if result else None
    def save_quiz_result(self, student_id, subject, topic, score, total_marks, quiz_date):
        connection = self.connect()
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO quiz_results (student_id, subject, topic, score, total_marks, quiz_date) 
            VALUES (?, ?, ?, ?, ?, ?)
        """, (student_id, subject, topic, score, total_marks, quiz_date))
        connection.commit()
        self.close_connection()
        return True

    def fetch_quiz_results(self, student_id):
        """Fetches historical records filtered cleanly by student_id."""
        connection = self.connect()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM quiz_results WHERE student_id = ? ORDER BY quiz_date DESC", (student_id,))
        res = cursor.fetchall()
        self.close_connection()
        return res

    def save_ai_coaching(self, student_id, weak_topic, ai_feedback, created_date):
        connection = self.connect()
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO ai_coaching (student_id, weak_topic, ai_feedback, created_date) 
            VALUES (?, ?, ?, ?)
        """, (student_id, weak_topic, ai_feedback, created_date))
        connection.commit()
        self.close_connection()
        return True

    def fetch_ai_coaching(self, student_id):
        """Fetches persistent coaching logs filtered cleanly by student_id."""
        connection = self.connect()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM ai_coaching WHERE student_id = ? ORDER BY created_date DESC", (student_id,))
        res = cursor.fetchall()
        self.close_connection()
        return res

    def fetch_weak_topics_summary(self):
        connection = self.connect()
        cursor = connection.cursor()
        cursor.execute("""
            SELECT weak_topic, COUNT(*) 
            FROM ai_coaching 
            GROUP BY weak_topic 
            ORDER BY COUNT(*) DESC
        """)
        data = cursor.fetchall()
        self.close_connection()
        return data

    def fetch_students_by_mobile(self, mobile_number):
        """Fetches students matching a specific parent mobile number."""
        connection = self.connect()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM students WHERE parent_mobile = ?", (mobile_number,))
        res = cursor.fetchall()
        self.close_connection()
        return res

if __name__ == "__main__":
    db = DatabaseManager()
    db.create_tables()
    print("Database manager updated and verified successfully.")