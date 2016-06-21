# coding: utf-8

import unittest
from solar import parse_tweet, extract_by_flag, MSG_FLAG, BOAT_FLAG
from plot_curve import plot_matplotlib_fig
from datetime import datetime, timedelta
import os


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
        self.assertEqual(record["battery_voltage"], 39.75)
        self.assertEqual(record["output_current"], 25.78)

    def test_parse_many_parts_as_in_doc(self):
        record = parse_tweet('H09:49:12V39.75X29.35F43.34G15.45I25.78T26.34J54.555K-45.992L54.552M-45.989')
        self.assertEqual(record["battery_voltage"], 39.75)


class TestPlot(unittest.TestCase):

    def tearDown(self):
        os.remove("BatteryCurrent.png")

    def test_plot_curve(self):
        datetime_vector = []
        a = datetime.now()
        current_vector = []

        for i in range(10):
            d = timedelta(seconds=300*i)
            datetime_vector.append(a - d)
            current_vector.append(1)

        self.assertEqual(plot_matplotlib_fig(datetime_vector, current_vector, 3, 7), 0.25)
        self.assertTrue(os.path.exists("BatteryCurrent.png"))
