from src.providers import weather_json
from src.formatters import weather_format, message
from src.mailer import send_mail

def main():
    weather_json_data = weather_json.fetch_forecast_json()

    weather_info = weather_json.get_weather(weather_json_data)

    weather_section = weather_format.format_weather_section(weather_info)

    send_mail(
    "daily-notifier",
    message.create_message(weather_section)
    )


if __name__ == "__main__":
    main()