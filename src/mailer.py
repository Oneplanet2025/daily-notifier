from logging import getLogger
import smtplib
from email.message import EmailMessage

from src.config import Settings


logger = getLogger(__name__)


def send_mail(subject: str, body: str, settings: Settings) -> None:
    """メールを送信する"""

    message = EmailMessage()

    message["Subject"] = subject
    message["From"] = settings.mail_address
    message["To"] = settings.mail_to

    message.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        logger.info("メールサービスにログインします")

        try:
            smtp.login(settings.mail_address, settings.mail_password)
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
