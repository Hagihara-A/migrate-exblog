from unittest import TestCase


class TestScrapeExblog(TestCase):
    def setUp(self):
        from scrape_exblog import ScrapeExblog
        self.class_dict = {
            "class_title": "post-title",
            "class_body": "post-main",
            "class_tail": "post-tail"
        }

    def test_get_indv_urls(self):
        indv_urls2018_12 = {
            'https://staff.exblog.jp/238944045/',
            'https://staff.exblog.jp/238911510/',
            'https://staff.exblog.jp/238902905/',
            'https://staff.exblog.jp/238888884/'
        }
        res = set(self.scraper.get_indv_urls())
        self.assertSetEqual(res, indv_urls2018_12)
