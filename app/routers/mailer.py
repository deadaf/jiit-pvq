from fastapi import APIRouter
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from decouple import config

router = APIRouter()
# define email credentials
gmail_user = config("GMAIL_USER")
gmail_password = config("GMAIL_PASSWORD")


# define function to send email
def send_email(to, subject, body):
    message = MIMEMultipart()
    message["From"] = gmail_user
    message["To"] = to
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    smtp_server = smtplib.SMTP("smtp.gmail.com", 587)
    smtp_server.starttls()
    smtp_server.login(gmail_user, gmail_password)
    text = message.as_string()
    smtp_server.sendmail(gmail_user, to, text)
    smtp_server.quit()


# define route to send email
@router.get("/send-email")
async def send_email_route(email: str, text: str):
    send_email(email, "Test Email", text)
    return {"message": "Email sent successfully"}
