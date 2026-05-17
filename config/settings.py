import os
from pathlib import Path

# Load .env for local development
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).resolve().parent.parent / ".env"
    if env_path.exists():
        load_dotenv(dotenv_path=str(env_path))
    else:
        load_dotenv()
except Exception:
    pass

# ✅ Read from Streamlit secrets on cloud, fall back to .env locally
def _get(key, default=""):
    try:
        import streamlit as st
        return st.secrets.get(key, os.getenv(key, default))
    except Exception:
        return os.getenv(key, default)

class Settings:
    GEMINI_API_KEY      = _get("GEMINI_API_KEY")
    TWILIO_ACCOUNT_SID  = _get("TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN   = _get("TWILIO_AUTH_TOKEN")
    TWILIO_FROM_NUMBER  = _get("TWILIO_FROM_NUMBER")
    SYSTEM_EMAIL_PASSWORD = _get("SYSTEM_EMAIL_PASSWORD")

    @classmethod
    def validate(cls):
        if not cls.GEMINI_API_KEY:
            print("⚠️ WARNING: GEMINI_API_KEY is unconfigured.")
        else:
            print("✅ GEMINI engine authenticated.")