from logging import getLogger
import smtplib
from email.message import EmailMessage

from src.config import MAIL_ADDRESS, MAIL_PASSWORD, MAIL_TO

logger = getLogger(__name__)

def send_mail(subject: str, body: str) -> None:
    """メールを送信する"""

    message = EmailMessage()

    message["Subject"] = subject
    message["From"] = MAIL_ADDRESS
    message["To"] = MAIL_TO

    message.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        logger.info("メールサービスにログインします")

        try:
            smtp.login(MAIL_ADDRESS, MAIL_PASSWORD)
            logger.info("メールサービスにログインしました")
        except Exception:
            logger.exception("メールサービスへのログインに失敗しました")
            raise

        logger.info("メールを送信します")

        try:
            smtp.send_message(message)
            logger.info("メールを送信しました")
        except Exception:
            logger.exception("メールの送信に失敗しました")
            raise
