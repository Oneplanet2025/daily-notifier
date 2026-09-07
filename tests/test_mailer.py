from unittest.mock import patch

import pytest

from src.config import Settings
from src.mailer import send_mail


def test_send_mail():
    settings = Settings(
        mail_address="test@example.com",
        mail_password="password",
        mail_to="to@example.com",
    )

    with patch("src.mailer.smtplib.SMTP_SSL") as mock_smtp_ssl:
        mock_smtp = mock_smtp_ssl.return_value.__enter__.return_value

        send_mail(
            subject="テスト件名",
            body="テスト本文",
            settings=settings,
        )

    mock_smtp_ssl.assert_called_once_with(
        "smtp.gmail.com",
        465,
    )

    mock_smtp.login.assert_called_once_with(
        "test@example.com",
        "password",
    )

    mock_smtp.send_message.assert_called_once()

    message = mock_smtp.send_message.call_args.args[0]

    assert message["Subject"] == "テスト件名"
    assert message["From"] == "test@example.com"
    assert message["To"] == "to@example.com"
    assert message.get_content() == "テスト本文\n"


def test_send_mail_login_error():
    settings = Settings(
        mail_address="test@example.com",
        mail_password="password",
        mail_to="to@example.com",
    )

    with patch("src.mailer.smtplib.SMTP_SSL") as mock_smtp_ssl:
        mock_smtp = mock_smtp_ssl.return_value.__enter__.return_value
        mock_smtp.login.side_effect = RuntimeError("login failed")

        with pytest.raises(RuntimeError, match="login failed"):
            send_mail(
                subject="テスト件名",
                body="テスト本文",
                settings=settings,
            )

    mock_smtp.login.assert_called_once_with(
        "test@example.com",
        "password",
    )

    mock_smtp.send_message.assert_not_called()


def test_send_mail_send_error():
    settings = Settings(
        mail_address="test@example.com",
        mail_password="password",
        mail_to="to@example.com",
    )

    with patch("src.mailer.smtplib.SMTP_SSL") as mock_smtp_ssl:
        mock_smtp = mock_smtp_ssl.return_value.__enter__.return_value
        mock_smtp.send_message.side_effect = RuntimeError("send failed")

        with pytest.raises(RuntimeError, match="send failed"):
            send_mail(
                subject="テスト件名",
                body="テスト本文",
                settings=settings,
            )

    mock_smtp.login.assert_called_once_with(
        "test@example.com",
        "password",
    )

    mock_smtp_ssl.assert_called_once_with(
        "smtp.gmail.com",
        465,
    )

    mock_smtp.login.assert_called_once_with(
        "test@example.com",
        "password",
    )

    mock_smtp.send_message.assert_called_once()

    message = mock_smtp.send_message.call_args.args[0]

    assert message["Subject"] == "テスト件名"
    assert message["From"] == "test@example.com"
    assert message["To"] == "to@example.com"
    assert message.get_content() == "テスト本文\n"


def test_send_mail_login_error():
    settings = Settings(
        mail_address="test@example.com",
        mail_password="password",
        mail_to="to@example.com",
    )

    with patch("src.mailer.smtplib.SMTP_SSL") as mock_smtp_ssl:
        mock_smtp = mock_smtp_ssl.return_value.__enter__.return_value
        mock_smtp.login.side_effect = RuntimeError("login failed")

        with pytest.raises(RuntimeError, match="login failed"):
            send_mail(
                subject="テスト件名",
                body="テスト本文",
                settings=settings,
            )

    mock_smtp.login.assert_called_once_with(
        "test@example.com",
        "password",
    )

    mock_smtp.send_message.assert_not_called()


def test_send_mail_send_error():
    settings = Settings(
        mail_address="test@example.com",
        mail_password="password",
        mail_to="to@example.com",
    )

    with patch("src.mailer.smtplib.SMTP_SSL") as mock_smtp_ssl:
        mock_smtp = mock_smtp_ssl.return_value.__enter__.return_value
        mock_smtp.send_message.side_effect = RuntimeError("send failed")

        with pytest.raises(RuntimeError, match="send failed"):
            send_mail(
                subject="テスト件名",
                body="テスト本文",
                settings=settings,
            )

    mock_smtp.login.assert_called_once_with(
        "test@example.com",
        "password",
    )

    mock_smtp.send_message.assert_called_once()