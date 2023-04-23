from fastapi import APIRouter, Request, Body
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

import smtplib
from decouple import config
import typing as T
import os
import base64


router = APIRouter()
# define email credentials
gmail_user = config("GMAIL_USER")
gmail_password = config("GMAIL_PASSWORD")


# define function to send email
def send_email(to: str, message: MIMEMultipart):
    smtp_server = smtplib.SMTP("smtp.gmail.com", 587)
    smtp_server.starttls()
    smtp_server.login(gmail_user, gmail_password)
    text = message.as_string()
    smtp_server.sendmail(gmail_user, to, text)
    smtp_server.quit()


@router.post("/send-pdf")
async def send_pdf_route(
    request: Request, email: str = Body(...), files: T.List[str] = Body(...)
):
    message = MIMEMultipart()
    message["From"] = gmail_user
    message["To"] = email
    message["Subject"] = "Question Papers Delivery!"
    message.attach(
        MIMEText(
            "Please find attached the PDF files of Question Papers you requested.\n\nAll the Best!",
            "plain",
        )
    )
    # txts = []
    for file in files:
        filepath = os.path.join("app", "resources", file)
        if os.path.isfile(filepath):
            with open(filepath, "rb") as f:
                file_data = f.read()

            filename = os.path.basename(filepath)
            encoded_file = base64.b64encode(file_data).decode()
            attachment = MIMEApplication(base64.b64decode(encoded_file))
            attachment.add_header(
                "Content-Disposition", "attachment", filename=filename
            )
            message.attach(attachment)

            # exampdf = ExamPDF(filepath)
            # await exampdf.pdf_to_image()
            # text = await exampdf.image_to_text()
            # txts.append(text)

    # print("analysing cos")
    # await ExamPDF.analyse_cos(txts)

    send_email(email, message)
    return {"message": "Email sent successfully"}
