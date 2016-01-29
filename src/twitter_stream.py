# coding: utf-8
"""
@author: Diego Salomone
@author: Rodrigo Senra
"""

from datetime import datetime as dt
from twython import TwythonStreamer
import json


# Twitter Access Configuration Tokens
APP_KEY = 'xnRnnWSzt3jHhsRCw3Ivh7WHj'
APP_SECRET = 'A57nO60HCO1KZdVjgYKLoODKZyyu4PAKBjDLnDdlzqO29D2GIv'
OAUTH_TOKEN = '3347810553-B0NHhWECzL2PNL3bLuaMBy8BUhXu86M8EHZkwZo'
OAUTH_TOKEN_SECRET = '1GKYPfERcjd5PfmoGhf9J1FWofJ44vYhF2gz75bOMOEAx'


class MyStreamer(TwythonStreamer):
    def on_success(self, tweet):
        if 'text' in tweet:
            print('Tweet from @%s Date: %s' % (tweet['user']['screen_name'].encode('utf-8'),
                                               tweet['created_at']))
            print(tweet['text'].encode('utf-8'), '\n')
        else:
            print('Not DATA', tweet, type(tweet), dir(tweet))

    def on_error(self, status_code, data):
        print('Error', status_code, data)

def new_stream(**kw):
    stream = MyStreamer(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    stream.statuses.filter(**kw)
    return stream

def test():
    while True:
        s = new_stream(follow='brdcresearcher')

    #import doctest
    #doctest.testmod(verbose=True, exclude_empty=True)


if __name__ == '__main__':
    test()