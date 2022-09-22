import os

from flask import Flask, render_template, send_from_directory, request, make_response, flash, redirect, url_for
import datetime

from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000


def restart():
    return render_template('restart.html')


@app.route('/')
def home():
    if request.args.get('m') is not None:
        return home_stats()
    if request.args.get('rst') is not None:
        return restart()

    return render_template('home.html')


def home_stats():
    r = make_response(render_template('stats/home_stats'))
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
    hours = int(duration.total_seconds() / 60 / 60)
    minutes = int(duration.total_seconds() / 60) - hours * 60
    seconds = int(duration.total_seconds() % 60)
    string = f'{duration.days}T{hours}:{minutes}:{seconds}'  # TODO leading zero

    return string


if __name__ == '__main__':
    app.run()
