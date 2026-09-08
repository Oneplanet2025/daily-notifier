#Ruffエラーを起こすためのimport CIの確認のため
import os


import pytest

from src.config import Settings


def test_settings_from_environment(monkeypatch):
    monkeypatch.setenv("MAIL_ADDRESS", "test@example.com")
    monkeypatch.setenv("MAIL_PASSWORD", "password")
    monkeypatch.setenv("MAIL_TO", "to@example.com")

    result = Settings.from_environment()

    assert result.mail_address == "test@example.com"
    assert result.mail_password == "password"
    assert result.mail_to == "to@example.com"


def test_settings_from_environment_missing_mail_address(monkeypatch):
    monkeypatch.delenv("MAIL_ADDRESS", raising=False)
    monkeypatch.delenv("MAIL_PASSWORD", raising=False)
    monkeypatch.delenv("MAIL_TO", raising=False)

    with pytest.raises(KeyError):
        Settings.from_environment()


def test_settings_from_environment_empty_value(monkeypatch):
    monkeypatch.setenv("MAIL_ADDRESS", "")
    monkeypatch.setenv("MAIL_PASSWORD", "")
    monkeypatch.setenv("MAIL_TO", "")

    with pytest.raises(ValueError, match="メール関連の環境変数は空にできません"):
        Settings.from_environment()
