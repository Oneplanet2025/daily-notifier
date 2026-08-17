import smtplib
from email.message import EmailMessage

from src.config import MAIL_ADDRESS, MAIL_PASSWORD, MAIL_TO


def send_mail(subject: str, body: str) -> None:
    """メールを送信する"""

    message = EmailMessage()

    message["Subject"] = subject
    message["From"] = MAIL_ADDRESS
    message["To"] = MAIL_TO

    message.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(MAIL_ADDRESS, MAIL_PASSWORD)
        smtp.send_message(message)
