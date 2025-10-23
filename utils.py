import smtplib
from email.message import EmailMessage
from datetime import datetime
from . import config

def log(*args):
    print(datetime.now().strftime("[%Y-%m-%d %H:%M:%S]"), *args, flush=True)

def send_email(subject: str, body: str):
    if not (config.SMTP_HOST and config.SMTP_USERNAME and config.SMTP_PASSWORD and config.EMAIL_FROM and config.EMAIL_TO):
        log("Email not configured; skipping notification.")
        return
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = config.EMAIL_FROM
    msg["To"] = config.EMAIL_TO
    msg.set_content(body)
    try:
        with smtplib.SMTP(config.SMTP_HOST, config.SMTP_PORT, timeout=20) as s:
            s.starttls()
            s.login(config.SMTP_USERNAME, config.SMTP_PASSWORD)
            s.send_message(msg)
        log("Email sent.")
    except Exception as e:
        log("Email failed:", e)
