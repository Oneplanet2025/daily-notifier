from src import weather
from src import format
# from src.mailer import send_mail

def main():
    weather_json_data = weather.fetch_forecast_json()

    weather_info = weather.get_weather(weather_json_data)

    print(format.format_weather(weather_info))

    # send_mail(
    # "daily-notifier テスト",
    # format.format_weather(weather_info)


if __name__ == "__main__":
    main()