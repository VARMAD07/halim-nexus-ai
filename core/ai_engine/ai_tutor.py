import os
import sys
from pathlib import Path

# Ensure project root is mapped explicitly for config space resolution
root_path = Path(__file__).parent.parent.parent.parent
if str(root_path) not in sys.path:
    sys.path.append(str(root_path))

from google import genai
from config.settings import Settings

class AITutor:
    """
    AI Educational Assistant orchestration layer utilizing the modern Google GenAI SDK.
    """

    def __init__(self):
        # Read from config object class variable, fallback gracefully to system environment variable
        raw_key = getattr(Settings, "GEMINI_API_KEY", None) or os.getenv("GEMINI_API_KEY")
        
        if not raw_key or raw_key == "YOUR_API_KEY":
            self.client = None
            print("⚠️ WARNING: GEMINI_API_KEY is unconfigured. Engine will run using local mock fallbacks.")
        else:
            self.client = genai.Client(api_key=raw_key)
            
        self.model_name = "gemini-2.5-flash"

    def build_prompt(self, topic: str) -> str:
        """
        Assembles a highly tailored conceptual prompt structured for CBSE framework compliance.
        """
        prompt = f"""
        You are an elite academic educational AI tutor.
        Explain this topic in a beginner-friendly way.

        Topic: {topic}

        Requirements:
        - Simple explanations
        - CBSE-style teaching
        - Bullet points for key definitions
        - Concrete practical examples
        - Strategic study tips for examination revision
        - Short summary at the very end
        
        Ensure formatting uses clean Markdown headings.
        """
        return prompt

    def generate_topic_explanation(self, topic: str) -> str:
        """
        Generates a comprehensive structured lesson overview for a specific topic query.
        """
        if not self.client:
            return f"🎨 **[Mock Mode]** Detailed CBSE Explanation for **{topic}**:\n\nThis is a placeholder summary. Please update your real API token credentials within `config/settings.py` to process live Gemini responses."

        prompt = self.build_prompt(topic)

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            return response.text
        except Exception as e:
            return f"❌ GenAI SDK Operational Error: {str(e)}"

    def generate_weakness_coaching(self, weak_topic: str) -> str:
        """
        Generates a personalized pedagogical coaching strategy when a performance drop is logged.
        """
        if not self.client:
            return f"📊 **[Mock Mode]** Revision Guidance Blueprint for **{weak_topic}**:\n\nReview introductory foundational formulas and target 5 textbook sample exercises daily."

        prompt = f"""
        You are an empathetic, highly structured AI academic mentor.
        A student has performed poorly on a quiz assessment and is flagged as weak in: {weak_topic}

        Generate a practical and clear intervention framework covering:
        - Actionable Improvement Strategy
        - 3-Day Sequential Study Plan
        - Daily Practice Advice
        - Motivational Guidance
        - Long-term Revision Strategy

        Keep the tone encouraging, technical, and optimized for execution.
        """

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            return response.text
        except Exception as e:
            return f"❌ GenAI SDK Operational Error: {str(e)}"


if __name__ == "__main__":
    print("Initializing AITutor Component Run Test...")
    tutor = AITutor()
    result = tutor.generate_topic_explanation("Photosynthesis")
    print("\n--- Test Execution Result Output ---")
    print(result)