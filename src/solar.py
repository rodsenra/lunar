# coding: utf-8
"""
@author: Diego Salomone
@author: Rodrigo Senra
"""

import re
import logging
from datetime import datetime as dt

MSG_FLAG = '$'
BOAT_FLAG = 'B'
LAT_FLAG = 'L'
LONG_FLAG = 'M'

PROTO = {
    'V': {"label": 'battery_voltage', "convert": lambda x: float(x)},
    'I': {"label": 'output_current',  "convert": lambda x: float(x)},
    'G': {"label": 'input_current', "convert": lambda x: float(x)},
    'F': {"label": 'battery_current', "convert": lambda x: float(x)},
    'J': {"label": 'latitude_begin', "convert": lambda x: float(x)},
    LAT_FLAG: {"label": 'latitude_end', "convert": lambda x: float(x)},
    # TODO: support sampling
    't': {"label": 'sampling_rate',  "convert": lambda x: int(x)},
    'K': {"label": 'longitude_begin', "convert": lambda x: float(x)},
    LONG_FLAG: {"label": 'longitude_end', "convert": lambda x: float(x)},
    'H': {"label": 'boat_timestamp', "unit": "",
          "convert": lambda x: dt(year=dt.now().year,
                                  month=dt.now().month,
                                  day=dt.now().day,
                                  hour=int(x[:2]),
                                  minute=int(x[3:5]),
                                  second=int(x[6:8]))},
    'T': {"label": 'box_temperature',  "convert": lambda x: float(x)},
    'X': {"label": 'output_voltage',  "convert": lambda x: float(x)},
    BOAT_FLAG: {"label": 'boat_name',  "convert": lambda x: x},
    MSG_FLAG: {"label": 'last_msg', "convert": lambda x: x},
}

PATTERN = re.compile(r"(\w[\-\+0-9\:\.]+)")


def extract_by_flag(flag, tweet):
    """
    Utility function to extract the content that follows the flag in the tweet or None.

    :param flag:  A letter defined in  PROTO that defines a piece of the message.
    :param tweet: The tweet message as a string.
    :return: The tweet prefix and the extracted field content that follows the flag (without the flag).
    """
    assert(type(tweet) == str)
    assert(len(tweet) > 0)
    if flag in tweet:
        position = tweet.index(flag)
        return tweet[:position], tweet[position+1:]
    else:
        return tweet, None


def parse_tweet(tweet):
    """
    Format is the concatenation of records beginning with letters followed by numbers

    :param tweet: the tweet message
    :return: a dictionary with tweet fields
    """

    record = {}
    prefix, msg = extract_by_flag(MSG_FLAG, tweet)
    if msg:
        record[PROTO[MSG_FLAG]['label']] = msg
    else:
        prefix, boat_name = extract_by_flag(BOAT_FLAG, tweet)
        if boat_name:
            record[PROTO[BOAT_FLAG]['label']] = boat_name

    parts = re.split(PATTERN, prefix)

    try:
        for part in parts:
            if not part:
                continue
            flag = part[0]
            msg = part[1:]
            record[PROTO[flag]['label']] = PROTO[flag]["convert"](msg)
    except Exception as ex:
        logging.error("Failed to parse {0:s} with exception {1:s}".format(tweet, ex))
    return record
