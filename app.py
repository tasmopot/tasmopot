from flask import Flask, render_template, send_from_directory, request, make_response
import datetime

app = Flask(__name__)


@app.route('/')
def home():
    if request.args.get('m') is not None:
        return home_stats()

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


def uptime():
    start_date = datetime.datetime(2022, 9, 19, 14, 37, 3)
    duration = datetime.datetime.now() - start_date
    hours = int(duration.total_seconds() / 60 / 60)
    minutes = int(duration.total_seconds() / 60) - hours*60
    seconds = int(duration.total_seconds() % 60)
    string = f'{duration.days}T{hours}:{minutes}:{seconds}'  # TODO leading zero

    return string


if __name__ == '__main__':
    app.run()
