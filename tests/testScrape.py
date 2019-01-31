from unittest import TestCase
from migrate.scrape_exblog import ScrapeExblog
from migrate.parse_entries import ConstructMTtext
from pathlib import Path
import json


class TestScrape(TestCase):
    def setUp(self):
        input_file = Path('input.json')
        with input_file.open('r') as f:
            input_data = json.load(f)
        self.input_data = input_data

        self.output_path = 'output.tmp.txt'

    def testDefaultInput(self):
        scraper = ScrapeExblog(**self.input_data)
        entries = scraper.scrapeSinglePage(2018, 12)
        maker = ConstructMTtext(self.output_path)
        MTtext = maker.constructMTtextFromMonthEntries(entries)
        maker.saveMTtext(MTtext)
        with open(self.output_path, 'r') as f:
            saved = f.read()

        self.assertEqual(saved, )
