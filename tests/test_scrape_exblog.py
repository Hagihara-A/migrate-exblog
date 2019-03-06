from unittest import TestCase
import doctest
from migrate_exblog import scrape_exblog
from migrate_exblog.scrape_exblog import ScrapeExblog


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(scrape_exblog))
    return tests


class TestScrapeExblog(TestCase):
    def setUp(self):
        self.default_class_dict = {
            "class_title": "post-title",
            "class_body": "post-main",
            "class_tail": "post-tail"
        }

    def test_get_indv_urls(self):
        scraper = ScrapeExblog('https://staff.exblog.jp/',
                               **self.default_class_dict)
        i_urls = scraper.get_indv_urls()
        self.assertIn('https://staff.exblog.jp/239072912/', i_urls)
        self.assertIn('https://staff.exblog.jp/1606524/', i_urls)
        self.assertNotIn('https://staff.exblog.jp/m2013-11-01/', i_urls)
