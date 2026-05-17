import os
class Settings:

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "fallback_value")

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "fallback_value")