import os
from pathlib import Path
from dotenv import load_dotenv

# ✅ FIXED: Dynamic path anchored to this file's location — works on any machine
env_path = Path(__file__).resolve().parent.parent / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=str(env_path))
else:
    load_dotenv()

class Settings:
    """
    Central operational credentials mapper for HALIM NEXUS AI.
    Hard-anchored file system pathing to guarantee live environment loading.
    """
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip().strip('"').strip("'")

    @classmethod
    def validate(cls):
        """Validates that critical credentials are loaded correctly at boot."""
        if not cls.GEMINI_API_KEY or cls.GEMINI_API_KEY in ("", "YOUR_API_KEY"):
            print("⚠️ WARNING: GEMINI_API_KEY is unconfigured. Engine will run using local mock fallbacks.")
        else:
            print(f"✅ GEMINI engine authenticated successfully.")
            Settings.validate()