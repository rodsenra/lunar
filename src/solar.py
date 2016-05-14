# coding: utf-8
"""
@author: Diego Salomone
@author: Rodrigo Senra
"""

from datetime import datetime as dt


FORMATS = {
    'T': (4,   'battery_voltage', lambda x: float("{0}.{1}".format(x[:3], x[3]))),
    'I': (4,   'input_current',   lambda x: float("{0}.{1}".format(x[:3], x[3]))),
    'O': (4,   'output_current',  lambda x: float("{0}.{1}".format(x[:3], x[3]))),
    'A': (8,   'latitude',        lambda x: float("{0}.{1}".format(x[:3], x[3:]))),
    'G': (8,   'longitude',       lambda x: float("{0}.{1}".format(x[:3], x[3:]))),
    'H': (6,   'timestamp',       lambda x: dt(year=dt.now().year, month=dt.now().month, day=dt.now().day, \
                                               hour=int(x[:2]), minute=int(x[2:4]), second=int(x[4:6]))),
    '$': (140, 'msg',             lambda x: x)
}

REC_SIZES = {k: v[0] for k,v in FORMATS.items()}
REC_NAMES = {k: v[1] for k,v in FORMATS.items()}
REC_MASKS = {k: v[2] for k,v in FORMATS.items()}
REC_MARKS = {v[1]: k for k,v in FORMATS.items()}


def parse_tweet(tweet):
    """
    Format is the concatenation of records beginning with letters followed by numbers

    :param tweet: the tweet message
    :return: a dictionary with tweet fields

    >>> parse_tweet('T1235I0023O0015A+2487543G-4256789H123421')
    {'timestamp': datetime.datetime(2016, 2, 17, 12, 34, 21), 'battery_voltage': 123.5, 'longitude': -42.56789, 'input_current': 2.3, 'latitude': 24.87543, 'output_current': 1.5}

    >>> parse_tweet('T1235$OK TUDO BEM')
    {'msg': 'OK TUDO BEM', 'battery_voltage': 123.5}

    """

    record = {}
    t = tweet[:]

    while t:
        rec_type = t[0]
        rec_data = t[1: REC_SIZES[rec_type]+1]
        record[REC_NAMES[rec_type]] = REC_MASKS[rec_type](rec_data)
        t = t[REC_SIZES[rec_type]+1:]

    return record


def encode_tweet(**kw):
    """
    Encode parameters in the tweet message format.

    :param kwt: all the named message parameters as defined in FORMATS.

    :return: the textual representation of the tweet.

    >>> encode_tweet(timestamp=dt(2016, 2, 17, 12, 34, 21), battery_voltage=123.5, longitude=-42.56789, input_current=2.3, latitude=24.87543, output_current=1.5)
    'H123421T1235G-4256789I23A2487543O15'


    """
    def format_(field_name, field_value):
        mark = REC_MARKS[field_name]
        if mark in ('T', 'I', 'O', 'A', 'G'):
            value = str(field_value).replace('.', '')
        elif mark == '$':
            value = field_value[:140]
        elif mark == 'H':
            value = str(field_value.time())[:8].replace(':', '')
        else:
            raise Exception('Unexpected {0} mark in {1}:{2}'.format(mark, field_name, field_value))

        return "{0}{1}".format(mark, value)

    tweet = ''.join([format_(k, v) for k,v in kw.items()])
    return tweet


def test():
    import doctest
    doctest.testmod(verbose=True, exclude_empty=True)


if __name__ == '__main__':
    test()