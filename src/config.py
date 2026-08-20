import os
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

if os.getenv("GITHUB_ACTIONS") != "true":
    load_dotenv(Path(r"C:\Secrets\daily-notifier.env"))

logger.info("環境変数を読み込みます")
try:
    MAIL_ADDRESS = os.environ["MAIL_ADDRESS"]
    MAIL_PASSWORD = os.environ["MAIL_PASSWORD"]
    MAIL_TO = os.environ["MAIL_TO"]
    logger.info("環境変数を読み込みました")
except KeyError:
    logger.exception("環境変数の読み込みに失敗しました")
    raise

