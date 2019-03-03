import json
from pathlib import Path
from unittest import TestCase

from export import make_scraper

ABS_PATH = Path(__file__).resolve()
ABS_DIR = ABS_PATH.parent


class TestScrapeExblog(TestCase):
    def setUp(self):
        input_file = Path(ABS_DIR / 'test_input.json')
        with input_file.open('r') as f:
            input_data = json.load(f)
        self.scraper = make_scraper(input_data)

    def test_get_indv_urls(self):
        indv_urls2018_12 = {
            'https://staff.exblog.jp/238944045/',
            'https://staff.exblog.jp/238911510/',
            'https://staff.exblog.jp/238902905/',
            'https://staff.exblog.jp/238888884/'
        }
        res = set(self.scraper.get_indv_urls())
        self.assertSetEqual(res, indv_urls2018_12)
