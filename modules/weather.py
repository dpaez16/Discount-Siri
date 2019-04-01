import requests
import json
from datetime import datetime

WEATHER_API_KEY = '3f9eb0e727msh27f25e5c8b2bb69p113264jsna72367b8cebb'
WEATHER_URL = "https://community-open-weather-map.p.rapidapi.com/"


def current_weather(loc):
    """
    Gets the current weather at a particular location.

    :param loc: (City, Country)
    :return: Weather object that tells the current weather.
    """

    headers = {
        "X-RapidAPI-Key": WEATHER_API_KEY
    }
    response = requests.get(WEATHER_URL + 'weather',
                            headers=headers,
                            params={'q': loc,
                                    'units': 'imperial'})
    if response.status_code != 200:
        return None, "Bad Location: {}".format(loc)
    return json.loads(response.content.decode('utf-8')), ""


def five_day_weather(loc):
    """
    Gets the 5-day forecast at a particular location.

    :param loc: (City, Country)
    :return: Weather object that tells the current weather.
    """

    headers = {
        "X-RapidAPI-Key": WEATHER_API_KEY
    }
    response = requests.get(WEATHER_URL + 'forecast',
                            headers=headers,
                            params={'q': loc,
                                    'units': 'imperial'})
    if response.status_code != 200:
        return None, "Bad Location: {}".format(loc)
    return json.loads(response.content.decode('utf-8')), ""


def transform_current_weather(weather_json):
    """
    Transforms the raw current weather data into a reliable dictionary.

    :param weather_json: Raw JSON to be parsed through.
    :return: Transformed current weather dict.
    """
    transformed_weather = process_report(weather_json)

    transformed_weather["name"] = weather_json["name"]
    transformed_weather["country"] = weather_json["sys"]["country"]

    return transformed_weather


def transform_timestamp(raw_timestamp):
    """
    Transforms a raw timestamp from a

    :param raw_timestamp:
    :return:
    """
    raw_date = datetime.strptime(raw_timestamp, "%Y-%m-%d %H:%M:%S")
    date = raw_date.strftime("%m/%d")
    weekday = raw_date.strftime("%A")
    time = raw_date.strftime("%I:%M%p")
    if time[0] == '0':
        time = time[1:]
    return date, weekday, time


def transform_forecast_weather(weather_json):
    transformed_weather = {
        "name": weather_json["city"]["name"],
        "country": weather_json["city"]["country"]
    }

    raw_reports = weather_json["list"]
    transformed_reports = []
    n = weather_json["cnt"]

    for idx in range(n):
        raw_report = raw_reports[idx]
        raw_timestamp = raw_report["dt_txt"]
        date, weekday, time = transform_timestamp(raw_timestamp)

        transformed_report = process_report(raw_report)

        transformed_weather["date"] = date
        transformed_weather["weekday"] = weekday
        transformed_weather["time"] = time

        transformed_reports.append(transformed_report)

    transformed_weather["reports"] = transformed_reports
    return transformed_weather


def process_report(raw_report):
    words = raw_report["weather"][0]["description"].split()
    words[0] = words[0].capitalize()
    description = " ".join(words) + "."
    transformed_report = {
        "summary": raw_report["weather"][0]["main"],
        "description": description,
        "current_temp": round(raw_report["main"]["temp"]),
        "min_temp": round(raw_report["main"]["temp_min"]),
        "max_temp": round(raw_report["main"]["temp_max"]),
        "humidity": round(raw_report["main"]["humidity"]),
        "wind_speed": raw_report["wind"]["speed"]
    }
    return transformed_report
