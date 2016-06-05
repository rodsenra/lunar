# coding: utf-8
"""
@author: Rodrigo Senra
"""

import logging
import threading
from datetime import datetime
from twython import TwythonStreamer
from solar import parse_tweet
from flask import Flask, render_template,  jsonify

# Twitter Access Configuration Tokens
APP_KEY = 'y8U2Hu1v6KQCbFFfr2kpPIg6F'
APP_SECRET = 'Uhi2dExZfGnPas3CzQoUqChWGhkcB3VI69Lji3VOFx1ZbxN52j'
OAUTH_TOKEN = '710522996050563072-CboNCGCvtckSGMDcqgtZsIZuEfcXknd'
OAUTH_TOKEN_SECRET = 'AvDXNs5JJa3UiITVI7qCFC48IRmnHUGPECuJtJdi80ZuH'

app = Flask(__name__)
app.queue = []

@app.route('/')
def root_page():
    return render_template('root.html')

@app.route('/telemetry')
def telemetry():
    result = {
        "hour": datetime.now(),
        "valid": True
    }
    try:
        telemetry = app.queue.pop(0)
        result.update(telemetry)
    except IndexError:
        result["valid"] = False
    return jsonify(**result)


class MyStreamer(TwythonStreamer):
    def on_success(self, tweet):
        if 'text' in tweet:
            msg = tweet['text'].encode('utf-8')
            src = tweet['user']['screen_name'].encode('utf-8')
            tstamp = tweet['created_at']
            logging.info('Tweet from @%s Date: %s Msg:%s' % (src, tstamp, msg))
            telemetry = parse_tweet(msg)
            app.queue.append(telemetry)
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


def main():
    logging.basicConfig(filename='lunar.log', level=logging.DEBUG, format='%(asctime)s :: %(levelname)s :: %(message)s')
    import sys
    try:
        host = sys.argv[1]
        port = int(sys.argv[2])
    except IndexError as e:
        print("Expects : server_IP port")

    thread = threading.Thread(target=background_thread, args=())
    thread.daemon = True
    thread.start()

    logging.info('Starting web server at %s' % port)
    app.run(host=host, port=port)


if __name__ == '__main__':
    main()