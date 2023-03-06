import os
from urllib.parse import unquote

from flask import Flask, render_template, request, make_response
import datetime

from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000

toggle_state = True


def toggle():
    """
    Toggles the power button
    :return:
    """
    global toggle_state
    toggle_state = not toggle_state


def restart():
    """
    Restart page
    :return:
    """
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
    """
    Configuration route, returns main configuration page for all sub config pages
    :return:
    """
    return render_template('configuration.html')


def console_stats():
    """
    Console stats route
    :return:
    """
    r = make_response(render_template('stats/console_stats', uptime=uptime(),
                                      timestamp=datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')))
    return r


@app.route('/cs')
def console():
    """
    Console route, logs executed commands with timestamp
    :return:
    """
    if request.args.get('c1') is not None:  # console command
        directory = 'logging/commands/'
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(os.path.join(directory, 'commands.txt'), "a+", encoding="utf-8") as file_object:
            file_object.write(
                f'{datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")}: {unquote(request.args.get("c1"))}{os.linesep}')
    if request.args.get('c2') is not None:  # console stats
        if request.args.get('c2') == '0':
            return console_stats()
        else:
            return '53}11}1}1'
    return render_template('console.html')


@app.route('/')
def home():
    """
    Home route, implementing dynamic toggle button
    :return:
    """
    if request.args.get('o') is not None:  # toggle command
        toggle()
        return home_stats()
    if request.args.get('m') is not None:  # stats command
        return home_stats()
    if request.args.get('rst') is not None:  # restart command
        return restart()

    return render_template('home.html')


def home_stats():
    """
    Home stats route
    :return:
    """
    r = make_response(render_template('stats/home_stats', value='ON' if toggle_state else 'OFF'))
    return r


@app.route('/in')
def info():
    """
    Info route
    :return:
    """
    r = make_response(render_template('info.html', uptime=uptime(), percentage='88', dbm='-56'))
    return r


@app.route('/up')
def up():
    """
    Update route
    :return:
    """
    r = make_response(render_template('update.html'))
    return r


def allowed_file(filename):
    return True


@app.route('/u2', methods=['POST'])
def u2():
    """
    u2 POST route for update file upload, logs and saves uploaded files
    :return:
    """
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
            # securing filename and adding timestamp
            filename = secure_filename(file.filename)
            filename = str(datetime.datetime.now()).split('.')[0].replace(':', '-') + '_' + filename
            directory = 'logging/uploaded_files/'
            if not os.path.exists(directory):
                os.makedirs(directory)
            file.save(os.path.join(directory, filename))
            return render_template('upload_success.html')


@app.errorhandler(413)
def too_large(e):
    """
    Update file too large page
    :param e:
    :return:
    """
    return render_template('update_too_large.html')


@app.route('/cm')
def cm():
    """
    cm route: cmnd path, implements status and module command, else returns home
    :return:
    """
    if request.args.get('cmnd') is not None:
        if 'status' in request.args.get('cmnd').lower():
            with open('templates/stats/status.json', 'r') as file:
                r = make_response(file.read())
                r.mimetype = 'application/json'
                return r
        elif 'module' in request.args.get('cmnd').lower():
            with open('templates/stats/module.json', 'r') as file:
                r = make_response(file.read())
                r.mimetype = 'application/json'
                return r
        # TODO: log all unrecognized commands
    return home()


def uptime():
    """
    Returns the uptime timestamp dynamically
    :return:
    """
    start_date = datetime.datetime(2022, 9, 19, 14, 37, 3)
    duration = datetime.datetime.now() - start_date
    days = duration.days
    hours = int(duration.total_seconds() / 60 / 60) % 24
    minutes = int(duration.total_seconds() / 60) % 60
    seconds = int(duration.total_seconds() % 60)
    string = f'{days}T{hours}:{minutes}:{seconds}'  # TODO leading zero

    return string


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    """
    Home route
    :param path:
    :return:
    """
    return home()


if __name__ == '__main__':
    app.run()
