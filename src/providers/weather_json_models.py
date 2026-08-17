from dataclasses import dataclass


@dataclass(frozen=True)
class RainForecast:
    """時間帯ごとの降水確率"""

    time: str
    probability: str


@dataclass(frozen=True)
class TemperatureInfo:
    """最高・最低気温"""

    minimum_temperature: str
    maximum_temperature: str


@dataclass(frozen=True)
class WeatherInfo:
    """メール通知に必要な天気情報"""

    report_datetime: str
    forecast_date: str
    weather: str
    rain_forecasts: tuple[RainForecast, ...]
    temperature: TemperatureInfo
