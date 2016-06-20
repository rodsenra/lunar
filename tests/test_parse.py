# coding: utf-8

import unittest
from solar import parse_tweet

class TestParser(unittest.TestCase):
    def test_parse_msg(self):
        tweet = "V3.53$Essa é para testar a mensagem"
        expected = ""
        effective = parse_tweet()