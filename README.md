# 🧠 Halim Nexus AI

> *educational command center — built for speed, built for scale.*

Halim Nexus AI is a Python-based institutional management system that unifies role-based administrative workflows, automated parent notifications, and generative AI-powered academic monitoring into a single relational backend core.

It completely isolates viewing environments across Student, Instructor, and Guardian workspaces — eliminating cross-contamination while keeping every data point linked through a single SQLite3 persistence layer.

**The goal is simple:** eliminate friction in institutional tracking and deliver students custom-tailored cognitive evaluation pipelines.

---

## ✨ Features

- 📡 **Real-time attendance tracking** with exception-based flagging matrices
- 📱 **Automated SMS alerts** routed directly through the Twilio Gateway
- 🤖 **Generative AI evaluations** powered by the Google GenAI SDK
- 🗺️ **Persistent weakness mapping** across tracked student learning sessions
- 🔐 **Role-based workspace isolation** — Student, Instructor, and Guardian views
- 🗄️ **Clean local data persistence** via a structured SQLite3 relational layout

---

## 🏗️ Architecture

```text
DatabaseManager → Roster Engine → Dashboard Matrix → Notifier Core → Twilio Gateway
                                         ↓
                                  GenAI Evaluator
                                         ↓
                               Weakness Analytics Map
```

---

## 📂 Project Structure

```text
halim_nexus_ai/
├── main.py                          # Central navigation matrix and state routing engine
├── requirements.txt                 # System dependency specification configuration
├── .env                             # Private system variables (ignored by Git)
├── .gitignore                       # Tracking exclusion register
│
├── app/
│   ├── components/                  # Reusable UI widgets
│   └── dashboards/
│       ├── notifier.py              # Outbound Twilio and SMTP engines
│       ├── parent_dashboard.py      # Guardian analytics viewport
│       ├── student_dashboard.py     # Learning ecosystem and evaluation framework
│       └── teacher_dashboard.py     # Instructor administration panel
│
├── config/
│   ├── settings.py                  # Global credentials and constant configurations
│   └── .streamlit/
│       └── config.toml              # Streamlit interface configuration parameters
│
├── core/
│   ├── ai_engine/
│   │   └── ai_tutor.py              # Google GenAI SDK orchestration layer
│   ├── analytics/
│   │   └── performance_tracker.py   # Telemetry and weakness analysis metrics
│   └── reports/
│       └── document_generator.py    # Summary compilation and export script
│
└── database/
    ├── data/
    │   └── halim_nexus.db           # SQLite3 binary database storage
    └── storage/
        └── db_manager.py            # SQL transactional abstraction layer
```

---

## ⚙️ Setup & Deployment

### 1 — Initialize the Environment Matrix

Create a `.env` file in your project root and populate it with your live credentials:

```env
GEMINI_API_KEY="YOUR_ACTUAL_GEMINI_API_KEY"
TWILIO_ACCOUNT_SID="YOUR_ACTUAL_TWILIO_ACCOUNT_SID"
TWILIO_AUTH_TOKEN="YOUR_ACTUAL_TWILIO_AUTH_TOKEN"
TWILIO_FROM_NUMBER="+1XXXXXXXXXX"
SYSTEM_EMAIL_PASSWORD="your_google_app_password"
```

> ⚠️ **Never commit this file to GitHub.** All production credentials must remain private.

---

### 2 — Isolate Dependencies

Install all required libraries from the package configuration module:

```bash
pip install -r requirements.txt
```

---

### 3 — Bootstrap Relational Layouts

Execute the database manager to generate a clean, initialized schema:

```bash
python database/storage/db_manager.py
```

---

### 4 — Activate the Infrastructure Engine

Launch the central application interface via Streamlit:

```bash
python -m streamlit run main.py
```

---

## 🚀 Deployment

To deploy on **Streamlit Community Cloud** (free):

1. Push this repository to GitHub *(ensure `.env` is in `.gitignore`)*
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New App**
3. Connect your GitHub repo and set the main file to `main.py`
4. Under **Advanced Settings → Secrets**, add your credentials in TOML format:

```toml
GEMINI_API_KEY = "your_key_here"
TWILIO_ACCOUNT_SID = "your_sid_here"
TWILIO_AUTH_TOKEN = "your_token_here"
TWILIO_FROM_NUMBER = "+1XXXXXXXXXX"
SYSTEM_EMAIL_PASSWORD = "your_password_here"
```

---

## 🛡️ Security Notes

- The `.env` file is listed in `.gitignore` and must **never** be pushed to any public repository
- Twilio Auth Tokens should be **regenerated immediately** if accidentally exposed
- All SMS alerts are restricted to Twilio-verified numbers while on a trial account

---

*Built with Python · Streamlit · SQLite3 · Twilio · Google GenAI*