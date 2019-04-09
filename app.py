import os
from flask import Flask, request, render_template, redirect, url_for, send_from_directory
from modules.weather import current_weather, transform_current_weather, \
    five_day_weather, transform_forecast_weather, aggregate_forecast, get_current_location
from modules.skyline import get_skyline_link
from modules.definition import get_definition
from modules.random_fact import get_random_fact
from modules.random_shower_thought import get_random_shower_thought
from modules.front_page_preview import get_front_page_preview
from modules.image_converter import convert_image_file
from modules.audio_converter import convert_audio_file

UPLOAD_FOLDER = os.getcwd()
PREVIOUS_FILE = None
ALLOWED_EXTENSIONS = {
    'IMAGES': set(['png', 'jpeg', 'jpg', 'bmp', 'gif']),
    'AUDIO': set(['ogg', 'wav', 'mp3', 'm4a', 'flac'])
}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def try_remove_previous_file():
    global PREVIOUS_FILE
    if PREVIOUS_FILE is not None:
        os.remove(PREVIOUS_FILE)
    return


def allowed_image_file(file):
    return '.' in file \
            and file.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS['IMAGES']


def allowed_audio_file(file):
    return '.' in file \
            and file.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS['AUDIO']


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
        skyline_link = get_skyline_link(city, country)
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
        skyline_link = get_skyline_link(city, country)
        return render_template('weather/forecast.html',
                               forecast=transformed_weather,
                               skyline=skyline_link)
    else:
        return render_template('error.html', msg=msg)


@app.route("/definition", methods=["GET", "POST"])
def definition_page():
    word = None
    if request.method == "POST":
        word = request.form['word']

    definition, msg = None, None
    if word is not None:
        definition, msg = get_definition(word)
    if definition is None and word is not None:
        return render_template('error.html', msg=msg)
    else:
        print(definition)
        return render_template('serious/definition.html', word=word, definitions=definition)


@app.route("/random_fact")
def random_fact_page():
    random_fact = get_random_fact()
    return render_template('serious/random_fact.html', fact=random_fact)


@app.route("/random_shower_thought")
def random_shower_thought_page():
    random_shower_thought = get_random_shower_thought()
    return render_template('serious/random_shower_thought.html',
                           shower_thought=random_shower_thought)


@app.route("/front_page_reddit")
def front_page_reddit_preview():
    front_page_preview = get_front_page_preview()
    print(front_page_preview)
    return render_template('serious/front_page_preview.html',
                           front_page=front_page_preview)


@app.route('/image_converter', methods=['GET', 'POST'])
def image_converter_page():
    global PREVIOUS_FILE
    try_remove_previous_file()
    if request.method == "POST":
        if request.files:
            file = request.files['file']
            if file and allowed_image_file(file.filename):
                file.save(file.filename)
                output_format = request.form['image_format']
                converted_file, msg = convert_image_file(file.filename, output_format)
                if converted_file is None:
                    return render_template('error.html', msg=msg)
                os.remove(file.filename)
                PREVIOUS_FILE = converted_file
                return send_from_directory(UPLOAD_FOLDER, converted_file, as_attachment=True)
            else:
                msg = "File is not an image!"
                return render_template('error.html', msg=msg)
        else:
            msg = "You did not upload a file at all!"
            return render_template('error.html', msg=msg)
    else:
        return render_template('serious/image_converter.html')


@app.route('/audio_converter', methods=['GET', 'POST'])
def audio_converter_page():
    global PREVIOUS_FILE
    try_remove_previous_file()
    if request.method == "POST":
        if request.files:
            file = request.files['file']
            if file and allowed_audio_file(file.filename):
                file.save(file.filename)
                output_format = request.form['audio_format']
                converted_file, msg = convert_audio_file(file.filename, output_format)
                if converted_file is None:
                    return render_template('error.html', msg=msg)
                os.remove(file.filename)
                PREVIOUS_FILE = converted_file
                return send_from_directory(UPLOAD_FOLDER, converted_file, as_attachment=True)
            else:
                msg = "File is not an audio file!"
                return render_template('error.html', msg=msg)
        else:
            msg = "You did not upload a file at all!"
            return render_template('error.html', msg=msg)
    else:
        return render_template('serious/audio_converter.html')


if __name__ == "__main__":
    app.run(debug=True)
