import doctest
from datetime import datetime
from unittest import TestCase


from migrate_exblog import scrape_exblog
from migrate_exblog.scrape_exblog import ScrapeExblog


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(scrape_exblog))
    return tests


class TestScrapeExblogOnStaffBlog(TestCase):
    def setUp(self):
        staffblog_args = {
            "url": 'https://staff.exblog.jp/',
            "class_title": "post-title",
            "class_body": "post-main",
            "class_tail": "post-tail"
        }
        demoblog_args = {
            "url": 'https://scrapedemo.exblog.jp/',
            "class_title": "post-title",
            "class_body": "post-main",
            "class_tail": "post-tail"
        }

        self.demo_scraper = ScrapeExblog(**demoblog_args)
        self.staff_scraper = ScrapeExblog(**staffblog_args)

    def test_staff_get_month_archive_urls(self):
        m_urls_actual = self.staff_scraper.get_month_archive_urls()
        correct_m_urls = [
            'https://staff.exblog.jp/m2017-05-01/',
            'https://staff.exblog.jp/m2015-12-01/',
            'https://staff.exblog.jp/m2004-07-01/'
        ]
        wrong_m_urls = [
            'http://staff.exblog.jp/i4/',
            'https://staff.exblog.jp/238613602/',
            'https://staff.exblog.jp/iv/list/?d=2004-07-01'
        ]
        for correct_m_url in correct_m_urls:
            with self.subTest(correct_month_archive_url=correct_m_url):
                self.assertIn(correct_m_url, m_urls_actual)
        for wrong_m_url in wrong_m_urls:
            with self.subTest(wrong_url=wrong_m_url):
                self.assertNotIn(wrong_m_url, m_urls_actual)

    def test_staff_get_indv_urls_from_month_archive_urls(self):
        urls = {
            'https://staff.exblog.jp/m2019-01-01/': [
                'https://staff.exblog.jp/239072912/',
                'https://staff.exblog.jp/239054322/',
                'https://staff.exblog.jp/238956088/'
            ],
            'https://staff.exblog.jp/m2015-12-01/': [
                'https://staff.exblog.jp/22036973/',
                'https://staff.exblog.jp/21907454/',
                'https://staff.exblog.jp/21885690/'
            ],
            'https://staff.exblog.jp/m2004-07-01/': [
                'https://staff.exblog.jp/739520/',
                'https://staff.exblog.jp/710052/',
                'https://staff.exblog.jp/700291/'
            ]
        }
        for m_url, i_urls in urls.items():
            i_urls_actual = self.staff_scraper.get_indv_url_from_month_archive_urls([
                                                                                    m_url])
            for i_url in i_urls:
                with self.subTest(month_archive_url=m_url, indv_url=i_url):
                    self.assertIn(i_url, i_urls_actual)

    def test_staff_parse_indv_page(self):
        contents = {
            'https://staff.exblog.jp/239072912/': {
                'title': '【webプッシュ通知】記事内にプロモーションボタンが設置できるようになりました',
                'body': ['いつもエキサイトブログをご利用いただきありがとうございます。',
                         '新規投稿・テンプレート作成・フリーページ作成内のメニューから設定ができますのでぜひご利用ください。',
                         '（以下のボタンをクリックしてご登録ください）'],
                'date': datetime(2019, 1, 22, 12, 32),
                'category': ''
            },
            'https://staff.exblog.jp/21885690/': {
                'title': '【募集開始】アサヒカメラ×Exciteブログ企画フォトコンテスト',
                'body': ['いつもエキサイトブログをご利用いただき誠にありがとうございます。',
                         'あなたらしく撮った子どもの写真や家族の心あたたまる写真を大募集します。',
                         '以上、今後共エキサイトブログをよろしくお願いいたします。'],
                'date': datetime(2015, 12, 1, 17, 37),
                'category': 'お知らせ'
            },
            'https://staff.exblog.jp/700291/': {
                'title': '「エキサイトブログ向上委員会」スタート',
                'body': ['はじめまして。',
                         'ひっそりとはじまった「エキサイトブログ向上委員会」ですが、ここでは新機能の紹介や開発報告などをしていきます。',
                         'エキサイトブログは、一番キレイで一番いい香りのする花を目指して行きます。'],
                'date': datetime(2004, 7, 20, 5, 27),
                'category': ''
            }
        }
        for i_url, entry in contents.items():
            actual_entry = self.staff_scraper.parse_indv_page(i_url)
            for k, v in entry.items():
                if k == 'body':
                    for part in v:
                        with self.subTest(key=k, value=part):
                            self.assertIn(part, actual_entry[k])
                else:
                    with self.subTest(key=k, value=v):
                        self.assertEqual(v, actual_entry[k])
