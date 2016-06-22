# coding: utf-8
"""
@author: Rodrigo Senra
"""

import logging
import threading
from datetime import datetime
from twython import TwythonStreamer
from solar import parse_tweet, LAT_FLAG, LONG_FLAG, BOAT_FLAG
from flask import Flask, render_template,  jsonify, request, Response
from formulas import calcula

# Twitter Access Configuration Tokens
APP_KEY = 'y8U2Hu1v6KQCbFFfr2kpPIg6F'
APP_SECRET = 'Uhi2dExZfGnPas3CzQoUqChWGhkcB3VI69Lji3VOFx1ZbxN52j'
OAUTH_TOKEN = '710522996050563072-CboNCGCvtckSGMDcqgtZsIZuEfcXknd'
OAUTH_TOKEN_SECRET = 'AvDXNs5JJa3UiITVI7qCFC48IRmnHUGPECuJtJdi80ZuH'

app = Flask(__name__)
app.queue = []
app.trail = []
app.boat_name = 'Não definido'


def enqueue(record):
    try:
        result = calcula(70,  # FIXME: porcentagem_de_bateria,
                         record['latitude_begin'],
                         record['longitude_begin'],
                         record['latitude_end'],
                         record['longitude_end'],
                         record['sampling_rate'],
                         100)  # distancia_a_percorrer)

        (calculated_current, engine_rpm, output_voltage,
            autonomy_time, energy_balance, calculated_speed,
            speed, distance_travelled) = result

        record['speed'] = speed
        record['engine_rpm'] = engine_rpm
        record['distance_travelled'] = distance_travelled

    except Exception as ex:
        logging.error("Falhou para calcular métricas. {0:s}".format(type(ex)))

    if (LONG_FLAG in record) and (LAT_FLAG in record):
        app.trail.append(record[LONG_FLAG, LAT_FLAG])
    app.queue.append(record)
    if BOAT_FLAG in record:
        app.boat_name = record[BOAT_FLAG]

@app.route('/')
def root_page():
    return render_template('root.html')


@app.route('/emulate', methods=['GET'])
def emulate_tweet():
    msg = request.args.get('msg', '')
    record = parse_tweet(msg)
    logging.info('Emulated tweet - Msg:{0}'.format(msg))
    enqueue(record)
    return Response("Ok")


@app.route('/telemetry')
def telemetry():
    valid = True
    try:
        record = app.queue.pop(0)
    except IndexError:
        valid = False
        record = {}
    return jsonify(hour=datetime.now(), valid=valid, boat_name=app.boat_name, **record)


class MyStreamer(TwythonStreamer):
    def on_success(self, tweet):
        if 'text' in tweet:
            msg = str(tweet['text'])
            src = str(tweet['user']['screen_name'])
            tstamp = tweet['created_at']
            logging.info('Tweet from @%s Date: %s Msg:%s' % (src, tstamp, msg))
            record = parse_tweet(msg)
            enqueue(record)
        else:
            logging.warn('No DATA %s' % tweet)

    def on_error(self, status_code, data):
        logging.error("%s %s" % (status_code, data))
        self.disconnect()


def new_stream(**kw):
    stream = MyStreamer(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET, client_args={'verify': False})
    stream.user(**kw)
    return stream


def background_thread():
    logging.info('Listening @MrGarllic')
    s = new_stream(track='MrGarllic')


def main(host, port):
    logging.basicConfig(filename='lunar.log', level=logging.DEBUG, format='%(asctime)s :: %(levelname)s :: %(message)s')

    thread = threading.Thread(target=background_thread, args=())
    thread.daemon = True
    thread.start()

    logging.info('Starting web server at %s' % port)
    app.run(host=host, port=port)


if __name__ == '__main__':
    import sys
    try:
        host = sys.argv[1]
        port = int(sys.argv[2])
    except IndexError as e:
        print("Expects : server_IP port")
    main(host, port)