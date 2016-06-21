# coding: utf-8

import unittest
from solar import parse_tweet, extract_by_flag, MSG_FLAG, BOAT_FLAG


class TestSolar(unittest.TestCase):

    def test_extract_by_flag_MSG(self):
        prefix, effective = extract_by_flag(MSG_FLAG, "V3.53$Essa é para testar a mensagem")
        expected = "Essa é para testar a mensagem"
        self.assertEqual(expected, effective)
        self.assertEqual(prefix, "V3.53")

    def test_extract_by_flag_MSG(self):
        prefix, effective = extract_by_flag(BOAT_FLAG, "BeSB1")
        expected = "eSB1"
        self.assertEqual(expected, effective)
        self.assertEqual(prefix, "")

    def test_parse_two_parts(self):
        record = parse_tweet("V39.75I25.78")
        self.assertEqual(record["V"], 39.75)
        self.assertEqual(record["I"], 25.78)
