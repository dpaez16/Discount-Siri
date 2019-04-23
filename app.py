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
from modules.trash_meme import gen_trash_meme
from modules.facts_meme import gen_facts_meme
from modules.random_memes import get_random_memes
from modules.deep_fry import gen_deep_fry
from modules.alternating_emoji import gen_alternating_emoji
from modules.spongebob_mock import gen_spongebob_mock
from modules.explosion_meme import append_explosion_clip
from modules.youtube_videos import video_search_query

UPLOAD_FOLDER = os.getcwd()
ALLOWED_EXTENSIONS = {
    'IMAGES': set(['png', 'jpeg', 'jpg', 'bmp', 'gif']),
    'AUDIO': set(['ogg', 'wav', 'mp3', 'm4a', 'flac']),
    'VIDEO': set(['mp4', 'ogv', 'mpeg', 'avi', 'mov'])
}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_image_file(file):
    return '.' in file \
           and file.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS['IMAGES']


def allowed_audio_file(file):
    return '.' in file \
           and file.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS['AUDIO']


def allowed_video_file(file):
    return '.' in file \
           and file.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS['VIDEO']


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
    if request.method == "POST":
        if request.files:
            file = request.files['file']
            if file and allowed_image_file(file.filename):
                file.save(file.filename)
                output_format = request.form['image_format']
                converted_file, msg = convert_image_file(file.filename, output_format)
                if converted_file is None:
                    return render_template('error.html', msg=msg)
                sent_file = send_from_directory(UPLOAD_FOLDER, converted_file, as_attachment=True)
                os.remove(file.filename)
                os.remove(converted_file)
                return sent_file
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
    if request.method == "POST":
        if request.files:
            file = request.files['file']
            if file and allowed_audio_file(file.filename):
                file.save(file.filename)
                output_format = request.form['audio_format']
                converted_file, msg = convert_audio_file(file.filename, output_format)
                if converted_file is None:
                    return render_template('error.html', msg=msg)
                sent_file = send_from_directory(UPLOAD_FOLDER, converted_file, as_attachment=True)
                os.remove(file.filename)
                os.remove(converted_file)
                return sent_file
            else:
                msg = "File is not an audio file!"
                return render_template('error.html', msg=msg)
        else:
            msg = "You did not upload a file at all!"
            return render_template('error.html', msg=msg)
    else:
        return render_template('serious/audio_converter.html')


@app.route("/trash_vision", methods=['GET', 'POST'])
def trash_vision():
    if request.method == "POST":
        if request.files:
            file = request.files['file']
            if file and allowed_image_file(file.filename):
                file.save(file.filename)
                trash_meme, msg = gen_trash_meme(file.filename)
                if trash_meme is None:
                    return render_template('error.html', msg=msg)
                sent_file = send_from_directory(UPLOAD_FOLDER, trash_meme, as_attachment=True)
                os.remove(file.filename)
                os.remove(trash_meme)
                return sent_file
            else:
                msg = "File is not an image!"
                return render_template('error.html', msg=msg)
        else:
            msg = "You did not upload a file at all!"
            return render_template('error.html', msg=msg)
    else:
        return render_template('memes/trash_vision.html')


@app.route("/facts_meme", methods=['GET', 'POST'])
def facts_meme_page():
    if request.method == 'POST':
        text_input = request.form['text_input']
        facts_meme, msg = gen_facts_meme(text_input)
        if facts_meme is None:
            return render_template('error.html', msg=msg)
        sent_file = send_from_directory(UPLOAD_FOLDER, facts_meme, as_attachment=True)
        os.remove(facts_meme)
        return sent_file
    else:
        return render_template("memes/facts_meme.html")


@app.route("/random_memes")
def random_meme_page():
    random_memes, msg = get_random_memes()
    return render_template('memes/random_meme.html', memes=random_memes)


@app.route('/deep_fry', methods=['GET', 'POST'])
def deep_fry_page():
    if request.method == "POST":
        if request.files:
            file = request.files['file']
            if file and allowed_image_file(file.filename):
                file.save(file.filename)
                deep_fried_meme, msg = gen_deep_fry(file.filename)
                if deep_fried_meme is None:
                    return render_template('error.html', msg=msg)
                sent_file = send_from_directory(UPLOAD_FOLDER, deep_fried_meme, as_attachment=True)
                os.remove(file.filename)
                os.remove(deep_fried_meme)
                return sent_file
            else:
                msg = "File is not an image!"
                return render_template('error.html', msg=msg)
        else:
            msg = "You did not upload a file at all!"
            return render_template('error.html', msg=msg)
    else:
        return render_template('memes/deep_fry.html')


@app.route("/alternating_text_emoji", methods=['GET', 'POST'])
def alternating_text_emoji_page():
    generated_meme = ""
    if request.method == 'POST':
        text_input = request.form['text_input']
        generated_meme = gen_alternating_emoji(text_input)
    return render_template('memes/alternating_text_emoji.html',
                           output=generated_meme)


@app.route("/sponge_mock", methods=['GET', 'POST'])
def spongemock_page():
    generated_meme = ""
    if request.method == 'POST':
        text_input = request.form['user_input']
        generated_meme = gen_spongebob_mock(text_input)
    return render_template('memes/spongemock.html',
                           output=generated_meme)


@app.route('/add_explosion_clip', methods=['GET', 'POST'])
def explosion_clip_meme_page():
    if request.method == "POST":
        if request.files:
            file = request.files['file']
            if file and allowed_video_file(file.filename):
                file.save(file.filename)
                video, msg = append_explosion_clip(file.filename)
                if video is None:
                    return render_template('error.html', msg=msg)
                sent_file = send_from_directory(UPLOAD_FOLDER, video, as_attachment=True)
                os.remove(file.filename)
                os.remove(video)
                return sent_file
            else:
                msg = "File is not a video!"
                return render_template('error.html', msg=msg)
        else:
            msg = "You did not upload a file at all!"
            return render_template('error.html', msg=msg)
    else:
        return render_template('memes/explosion_clip.html')


@app.route('/youtube_audio', methods=['GET', 'POST'])
def youtube_audio_page():
    results, msg = None, None
    query = None
    results_range = []
    if request.method == 'POST':
        query = request.form['query']
        results, msg = video_search_query(query)
        if results is None:
            return render_template('error.html', msg=msg)
        results_range = range(len(results))

    return render_template('serious/youtube_audio.html',
                           query=query,
                           results=results,
                           results_range=results_range,
                           zip=zip)


if __name__ == "__main__":
    app.run(debug=True)
