from logging import getLogger, basicConfig, INFO

basicConfig(
    level=INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)

from src.providers import weather_json
from src.formatters import weather_formatter, message
from src.mailer import send_mail

logger = getLogger(__name__)


def main() -> None:
    logger.info("daily-notifierを開始します")

    forecast_json = weather_json.fetch_forecast_json()

    weather_info = weather_json.extract_weather_info(forecast_json)

    weather_section = weather_formatter.format_weather_section(weather_info)

    send_mail("daily-notifier", message.create_message(weather_section))

    logger.info("daily-notifierが正常終了しました")


if __name__ == "__main__":
    main()
