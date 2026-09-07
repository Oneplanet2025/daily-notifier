import pytest
import requests
from unittest.mock import Mock, patch

from src.config import (
    JMA_FORECAST_URL,
)
from src.providers.weather_json import (
    fetch_forecast_json,
    extract_weather_info,
    find_area,
)


def test_fetch_forecast_json():
    mock_response = Mock()
    mock_response.json.return_value = {"test": "data"}

    with patch(
        "src.providers.weather_json.requests.get",
        return_value=mock_response,
    ) as mock_get:
        result = fetch_forecast_json()

    assert result == {"test": "data"}

    mock_get.assert_called_once_with(
        JMA_FORECAST_URL,
        timeout=20,
    )
    mock_response.raise_for_status.assert_called_once()
    mock_response.json.assert_called_once()


def test_fetch_forecast_json_json_decode_error():
    mock_response = Mock()
    mock_response.json.side_effect = requests.exceptions.JSONDecodeError(
        "Invalid JSON",
        "invalid json",
        0,
    )

    with patch(
        "src.providers.weather_json.requests.get",
        return_value=mock_response,
    ):
        with pytest.raises(requests.exceptions.JSONDecodeError):
            fetch_forecast_json()


def test_fetch_forecast_json_timeout():
    with patch(
        "src.providers.weather_json.requests.get",
        side_effect=requests.Timeout(),
    ):
        with pytest.raises(requests.Timeout):
            fetch_forecast_json()


def test_fetch_forecast_json_request_exception():
    with patch(
        "src.providers.weather_json.requests.get",
        side_effect=requests.RequestException(),
    ):
        with pytest.raises(requests.RequestException):
            fetch_forecast_json()


def test_fetch_forecast_json_other_exception():
    with patch(
        "src.providers.weather_json.requests.get",
        side_effect=Exception(),
    ):
        with pytest.raises(Exception):
            fetch_forecast_json()


def test_extract_weather_info():
    weather_json_data = [
        {
            "reportDatetime": "2026-09-03T17:00:00+09:00",
            "timeSeries": [
                {
                    "timeDefines": [
                        "2026-09-03T17:00:00+09:00",
                        "2026-09-04T00:00:00+09:00",
                    ],
                    "areas": [
                        {
                            "area": {"name": "東部"},
                            "weathers": ["晴れ", "晴れ時々曇り"],
                        }
                    ],
                },
                {
                    "timeDefines": [
                        "2026-09-04T00:00:00+09:00",
                        "2026-09-04T06:00:00+09:00",
                        "2026-09-04T12:00:00+09:00",
                        "2026-09-04T18:00:00+09:00",
                    ],
                    "areas": [
                        {
                            "area": {"name": "東部"},
                            "pops": ["10", "20", "30", "40"],
                        }
                    ],
                },
                {
                    "areas": [
                        {
                            "area": {"name": "名古屋"},
                            "temps": ["22", "30"],
                        }
                    ],
                },
            ],
        }
    ]

    result = extract_weather_info(weather_json_data)

    assert result.report_datetime == "2026-09-03T17:00:00+09:00"
    assert result.forecast_date == "2026-09-04T00:00:00+09:00"
    assert result.weather == "晴れ時々曇り"

    assert len(result.rain_forecasts) == 4
    assert result.rain_forecasts[0].time == "2026-09-04T00:00:00+09:00"
    assert result.rain_forecasts[0].probability == "10"
    assert result.rain_forecasts[3].time == "2026-09-04T18:00:00+09:00"
    assert result.rain_forecasts[3].probability == "40"

    assert result.temperature.minimum_temperature == "22"
    assert result.temperature.maximum_temperature == "30"


def test_extract_weather_info_key_error():
    weather_json_data = [
        {
            "reportDatetime": "2026-09-03T17:00:00+09:00",
            "time_series": [],  # "timeSeries" → "time_series" に変更
        }
    ]

    with pytest.raises(KeyError):
        extract_weather_info(weather_json_data)


def test_extract_weather_info_index_error():
    weather_json_data = [
        {
            "reportDatetime": "2026-09-03T17:00:00+09:00",
            "timeSeries": [
                {},
                {},
            ],
        }
    ]

    with pytest.raises(IndexError):
        extract_weather_info(weather_json_data)


def test_extract_weather_info_other_exception():
    weather_json_data = [
        {
            "reportDatetime": "2026-09-03T17:00:00+09:00",
            "timeSeries": [
                {
                    "timeDefines": [
                        "2026-09-03T17:00:00+09:00",
                        "2026-09-04T00:00:00+09:00",
                    ],
                    "areas": [
                        {
                            "area": {"name": "東部"},
                            "weathers": ["晴れ", "晴れ時々曇り"],
                        }
                    ],
                },
                {
                    "timeDefines": [
                        "2026-09-04T00:00:00+09:00",
                        "2026-09-04T06:00:00+09:00",
                        "2026-09-04T12:00:00+09:00",
                        "2026-09-04T18:00:00+09:00",
                    ],
                    "areas": [
                        {
                            "area": {"name": "東部"},
                            "pops": ["10", "20", "30", "40"],
                        }
                    ],
                },
                {
                    "areas": [
                        {
                            "area": {"name": "名古屋"},
                            "temps": ["22", "30"],
                        }
                    ],
                },
            ],
        }
    ]

    with patch(
        "src.providers.weather_json.find_area",
        side_effect=RuntimeError("unexpected error"),
    ):
        with pytest.raises(RuntimeError, match="unexpected error"):
            extract_weather_info(weather_json_data)


def test_find_area():
    areas = [
        {"area": {"name": "西部"}, "weathers": ["晴れ"]},
        {"area": {"name": "東部"}, "weathers": ["曇り"]},
    ]

    result = find_area(areas, "東部", "天気予報")

    assert result == {
        "area": {"name": "東部"},
        "weathers": ["曇り"],
    }


def test_find_area_not_found():
    areas = [
        {"area": {"name": "西部"}, "weathers": ["晴れ"]},
        {"area": {"name": "東部"}, "weathers": ["曇り"]},
    ]

    with pytest.raises(ValueError, match="南部 の天気予報が見つかりません。"):
        find_area(areas, "南部", "天気予報")
