from src.providers import weather_json
from src.formatters import weather_formatter, message
from src.mailer import send_mail


def main() -> None:
    forecast_json = weather_json.fetch_forecast_json()

    weather_info = weather_json.extract_weather_info(forecast_json)

    weather_section = weather_formatter.format_weather_section(weather_info)

    send_mail("daily-notifier", message.create_message(weather_section))


if __name__ == "__main__":
    main()
