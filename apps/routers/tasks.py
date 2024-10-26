import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv
from fastapi import APIRouter, BackgroundTasks

from celery_config import celery_app

load_dotenv()
send_email = APIRouter()

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = os.getenv('EMAIL')
SMTP_PASSWORD = os.getenv('EMAIL_PASSWORD')


@celery_app.task()
def send_email_smtp(recipient_email: str, subject: str, message: str):
    msg = MIMEMultipart()
    msg["From"] = SMTP_USERNAME
    msg["To"] = recipient_email
    msg["Subject"] = subject

    msg.attach(MIMEText(message, "plain"))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(SMTP_USERNAME, recipient_email, msg.as_string())


@send_email.get("/send-email/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(send_email_smtp.delay, email, "Notification", "Hello")

    return {"message": "Notification sent in the background"}
