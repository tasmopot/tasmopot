import os

from flask import Flask, render_template, send_from_directory, request, make_response, flash, redirect, url_for
import datetime

from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000

toggle_state = True


def toggle():
    global toggle_state
    toggle_state = not toggle_state


def restart():
    return render_template('restart.html')


@app.route('/cn')
@app.route('/md')
@app.route('/wi')
@app.route('/mq')
@app.route('/dm')
@app.route('/tm')
@app.route('/lg')
@app.route('/co')
@app.route('/tp')
@app.route('/rt')
@app.route('/dl')
@app.route('/rs')
def configuration():
    return render_template('configuration.html')


@app.route('/')
def home():
    if request.args.get('o') is not None:       # toggle command
        toggle()
        return home_stats()
    if request.args.get('m') is not None:       # stats command
        return home_stats()
    if request.args.get('rst') is not None:     # resa
        return restart()


    return render_template('home.html')


def home_stats():
    r = make_response(render_template('stats/home_stats', value='ON' if toggle_state else 'OFF'))
    r.headers['Server'] = 'Tasmota/12.1.1 (ESP8266EX)'
    return r


@app.route('/in')
def info():
    r = make_response(render_template('info.html', uptime=uptime(), percentage='88', dbm='-56'))
    r.headers['Server'] = 'Tasmota/12.1.1 (ESP8266EX)'
    return r


@app.route('/up')
def up():
    r = make_response(render_template('update.html'))
    r.headers['Server'] = 'Tasmota/12.1.1 (ESP8266EX)'
    return r


def allowed_file(filename):
    return True


@app.route('/u2', methods=['POST'])
def u2():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'u2' not in request.files:
            return render_template('update_no_file_selected.html')
        file = request.files['u2']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            return render_template('update_no_file_selected.html')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join('uploaded_files/', filename))
            return render_template('upload_success.html')


@app.errorhandler(413)
def too_large(e):
    return render_template('update_too_large.html')


def uptime():
    start_date = datetime.datetime(2022, 9, 19, 14, 37, 3)
    duration = datetime.datetime.now() - start_date
    days = duration.days
    hours = int(duration.total_seconds() / 60 / 60) % 24
    minutes = int(duration.total_seconds() / 60) % 60
    seconds = int(duration.total_seconds() % 60)
    string = f'{days}T{hours}:{minutes}:{seconds}'  # TODO leading zero

    return string


if __name__ == '__main__':
    app.run()
