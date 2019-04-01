from flask import Flask, jsonify, request
from modules.weather import current_weather, transform_current_weather, \
    five_day_weather, transform_forecast_weather

app = Flask(__name__)


@app.route("/")
def home_page():
    return "Hello World!"


@app.route("/current_weather/<string:city>/<string:country>")
def current_weather_page(city, country):
    location = "{},{}".format(city, country)
    weather_json, msg = current_weather(location)

    if weather_json is not None:
        transformed_json = transform_current_weather(weather_json)
        return jsonify(transformed_json)
    else:
        return msg


@app.route("/forecast_weather/<string:city>/<string:country>")
def forecast_weather_page(city, country):
    location = "{},{}".format(city, country)
    weather_json, msg = five_day_weather(location)

    if weather_json is not None:
        transformed_weather = transform_forecast_weather(weather_json)
        return jsonify(transformed_weather)
    else:
        return msg


if __name__ == "__main__":
    app.run(debug=True)
