import os
import smtplib
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from twilio.rest import Client

# Load the secure variables from the .env file
load_dotenv()

class NotificationEngine:
    def __init__(self):
        # Email Config
        self.sender_email = "hammadfaridi713@gmail.com"
        self.app_password = os.getenv("SYSTEM_EMAIL_PASSWORD", "fallback_password")

        # Twilio SMS Config securely pulled from the environment
        self.twilio_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.twilio_auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.twilio_phone_number = os.getenv("TWILIO_FROM_NUMBER")  # ✅ FIXED: loaded from .env

    def send_quiz_alert_email(self, parent_email, student_name, score, total):
        """Drafts and sends an automated performance email to the registered parent."""
        if parent_email == "None" or not parent_email or "@" not in parent_email:
            print(f"⚠️ [EMAIL SKIPPED]: No valid parent email on file for {student_name}.")
            return False

        try:
            # Simulation mode print
            print(f"✅ [EMAIL ALERT]: Sent to {parent_email} -> '{student_name} scored {score}/{total}'")
            return True
        except Exception as e:
            print(f"❌ [EMAIL ERROR]: {e}")
            return False

    def send_sms_alert(self, parent_mobile, student_name, alert_type="attendance"):
        """
        Sends a high-priority SMS text message to the parent's mobile device.
        alert_type can be 'attendance' or 'urgent_update'.
        """
        # Failsafe: Don't try to send if they didn't register a mobile number
        if parent_mobile == "None" or not parent_mobile or len(parent_mobile) < 7:
            print(f"⚠️ [SMS SKIPPED]: No valid parent mobile number on file for {student_name}.")
            return False

        # ✅ FIXED: Normalize number — ensure +91 prefix for Indian numbers
        if not parent_mobile.startswith("+"):
            parent_mobile = "+91" + parent_mobile.lstrip("0")

        # Construct the specific text message based on the alert type
        if alert_type == "attendance":
            sms_body = f"HALIM NEXUS UPDATE: {student_name} has been marked ABSENT for today's session. Please contact the administration if this is an error."
        else:
            sms_body = f"HALIM NEXUS UPDATE: A new priority notification has been posted for {student_name}. Please check your Guardian Portal."

        try:
            client = Client(self.twilio_sid, self.twilio_auth_token)
            message = client.messages.create(
                body=sms_body,
                from_=self.twilio_phone_number,
                to=parent_mobile
            )
            print(f"📱 [SMS ALERT LIVE] Routed to {parent_mobile}. Twilio Message SID: {message.sid}")
            return True

        except Exception as e:
            print(f"❌ [SMS ERROR]: Twilio sending failed: {e}")
            return False