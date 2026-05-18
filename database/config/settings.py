import os
class Settings:

    GEMINI_API_KEY = os.getenv("AIzaSyBnFQ4DijqgmQ1IehAf0k_CDVSjOqdE1WY", "fallback_value")

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "fallback_value")