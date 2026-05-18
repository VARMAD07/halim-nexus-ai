import os
from pathlib import Path

# Load .env for local development only
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).resolve().parent.parent / ".env"
    load_dotenv(dotenv_path=str(env_path))
except Exception:
    pass

# Streamlit Cloud automatically injects secrets as environment variables
# so os.getenv works on both local (.env) and cloud (Streamlit secrets)
class Settings:
    GEMINI_API_KEY        = os.getenv("AIzaSyBnFQ4DijqgmQ1IehAf0k_CDVSjOqdE1WY", "")
    TWILIO_ACCOUNT_SID    = os.getenv("TWILIO_ACCOUNT_SID", "")
    TWILIO_AUTH_TOKEN     = os.getenv("TWILIO_AUTH_TOKEN", "")
    TWILIO_FROM_NUMBER    = os.getenv("TWILIO_FROM_NUMBER", "")
    SYSTEM_EMAIL_PASSWORD = os.getenv("SYSTEM_EMAIL_PASSWORD", "")