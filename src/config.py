import os
from dotenv import load_dotenv

# 気象庁の予報JSON URL
JMA_FORECAST_URL = "http://www.jma.go.jp/bosai/forecast/data/forecast/230000.json"

# 天気予報を取得する地域
JMA_FORECAST_AREA_NAME = "東部"

# 気温を取得する地点
JMA_TEMPERATURE_AREA_NAME = "名古屋"

load_dotenv()

#送信元メールアドレス
MAIL_ADDRESS = os.getenv("MAIL_ADDRESS")

#送信元メールアドレスのアプリパスワード
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")

#送信先メールアドレス
MAIL_TO = os.getenv("MAIL_TO")