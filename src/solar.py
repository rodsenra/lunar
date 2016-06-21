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

PROTO = {
    'V': {"label": 'Tensão da bateria', "unit": "V", "convert": lambda x: float(x)},
    'I': {"label": 'Corrente de Saída', "unit": "A", "convert": lambda x: float(x)},
    'G': {"label": 'Corrente de Entrada', "unit": "A", "convert": lambda x: float(x)},
    'F': {"label": 'Corrente da Bateria', "unit": "A", "convert": lambda x: float(x)},
    'J': {"label": 'Latitude Inicial', "unit": "", "convert": lambda x: float(x)},
    't': {"label": 'Intervalo de Amostragem', "unit": "s", "convert": lambda x: int(x)},
    'K': {"label": 'Longitude Inicial', "unit": "", "convert": lambda x: float(x)},
    'M': {"label": 'Longitude Final', "unit": "", "convert": lambda x: float(x)},
    'H': {"label": 'Hora da Embarcação', "unit": "",
          "convert": lambda x: dt(year=dt.now().year,
                                  month=dt.now().month,
                                  day=dt.now().day,
                                  hour=int(x[:2]),
                                  minute=int(x[2:4]),
                                  second=int(x[4:6]))},
    'T': {"label": 'Temperatura na caixa', "unit": "C", "convert": lambda x: float(x)},
    'X': {"label": 'Tensão da saída', "unit": "V", "convert": lambda x: float(x)},
    BOAT_FLAG: {"label": 'Embarcação', "unit": "", "convert": lambda x: x},
    MSG_FLAG: {"label": 'Último aviso recebido', "unit": "", "convert": lambda x: x},
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
        record[PROTO[MSG_FLAG]] = msg
    else:
        prefix, boat_name = extract_by_flag(BOAT_FLAG, tweet)
        if boat_name:
            record[PROTO[BOAT_FLAG]] = boat_name

    parts = re.split(PATTERN, prefix)

    try:
        for part in parts:
            if not part:
                continue
            flag = part[0]
            msg = part[1:]
            record[flag] = PROTO[flag]["convert"](msg)
    except Exception as ex:
        logging.error("Failed to parse {0:s} with exception {1:s}".format(tweet, ex))
    return record
