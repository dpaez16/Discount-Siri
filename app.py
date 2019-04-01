from flask import Flask, jsonify, request, render_template, redirect, url_for
from modules.weather import current_weather, transform_current_weather, \
    five_day_weather, transform_forecast_weather, aggregate_forecast, get_current_location
from modules.skyline import get_skyline_link

app = Flask(__name__)


@app.route("/")
def home_page():
    return render_template('home.html')


@app.route("/current_weather")
def pre_current_weather_page():
    city, country, msg = get_current_location()
    if city is not None:
        return redirect(url_for('current_weather_page', city=city, country=country))
    else:
        return render_template('error.html', msg=msg)


@app.route("/current_weather/city=<string:city>,country=<string:country>",
           methods=['GET', 'POST'])
def current_weather_page(city, country):
    if request.method == "POST":
        city, country = request.form["city"], request.form["country"]
    else:
        pass

    location = "{},{}".format(city, country)
    weather_json, msg = current_weather(location)

    if weather_json is not None:
        transformed_json = transform_current_weather(weather_json)
        skyline_link = get_skyline_link(city)
        return render_template('weather/current.html',
                               current_weather=transformed_json,
                               skyline=skyline_link)
    else:
        return render_template('error.html', msg=msg)


@app.route("/forecast_weather")
def pre_forecast_weather_page():
    city, country, msg = get_current_location()
    if city is not None:
        return redirect(url_for('forecast_weather_page', city=city, country=country))
    else:
        return render_template('error.html', msg=msg)


@app.route("/forecast_weather/city=<string:city>,country=<string:country>",
           methods=['GET', 'POST'])
def forecast_weather_page(city, country):
    if request.method == 'POST':
        city, country = request.form['city'], request.form['country']
    else:
        pass

    location = "{},{}".format(city, country)
    weather_json, msg = five_day_weather(location)

    if weather_json is not None:
        transformed_weather = transform_forecast_weather(weather_json)
        aggregate_forecast(transformed_weather)
        skyline_link = get_skyline_link(city)
        return render_template('weather/forecast.html',
                               forecast=transformed_weather,
                               skyline=skyline_link)
    else:
        return render_template('error.html', msg=msg)


if __name__ == "__main__":
    app.run(debug=True)
