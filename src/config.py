import os
from dataclasses import dataclass
from logging import getLogger
from pathlib import Path

from dotenv import load_dotenv


logger = getLogger(__name__)

# 気象庁の予報JSON URL
JMA_FORECAST_URL = "http://www.jma.go.jp/bosai/forecast/data/forecast/230000.json"

# 天気予報を取得する地域
JMA_FORECAST_AREA_NAME = "東部"

# 気温を取得する地点
JMA_TEMPERATURE_AREA_NAME = "名古屋"

# 機密情報ファイルのローカル上のパス
ENV_PATH = Path(r"C:\Secrets\daily-notifier.env")

if os.getenv("GITHUB_ACTIONS") != "true":
    load_dotenv(ENV_PATH)

@dataclass(frozen=True)
class Settings:
    mail_address: str
    mail_password: str
    mail_to: str

    @classmethod
    def from_environment(cls):
        logger.info("環境変数を読み込みます")

        try:
            mail_address = os.environ["MAIL_ADDRESS"]
            mail_password = os.environ["MAIL_PASSWORD"]
            mail_to = os.environ["MAIL_TO"]
        except KeyError:
            logger.exception("環境変数の読み込みに失敗しました")
            raise

        if not mail_address or not mail_password or not mail_to:
            logger.error("メール関連の環境変数に空の値があります")
            raise ValueError("メール関連の環境変数は空にできません")

        logger.info("環境変数を読み込みました")

        return cls(
            mail_address=mail_address,
            mail_password=mail_password,
            mail_to=mail_to,
        )


settings = Settings.from_environment()
