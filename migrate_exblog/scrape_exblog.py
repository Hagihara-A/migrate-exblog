import re
import types
import urllib.parse as up
from datetime import datetime
from pathlib import Path
import requests
from bs4 import BeautifulSoup
from time import sleep

from bs4 import Comment
from tqdm import tqdm


def get_soup(url, interval=0.20):
    res = requests.get(url)
    sleep(interval)
    res.encoding = res.apparent_encoding
    return BeautifulSoup(res.content, 'lxml')


class ScrapeExblog:
    def __init__(self,
                 url,
                 date_dict,
                 selector_title,
                 selector_body,
                 selector_time='.TIME'):
        self.url = self.validate_url(url)
        self.date_dict = date_dict
        self.selector_title = self.validate_selector(selector_title)
        self.selector_body = self.validate_selector(selector_body)
        self.selector_time = self.validate_selector(selector_time)

        self.exclude_func = lambda *x: True
        self.entries = []

    def validate_url(self, url):
        if isinstance(url, str):
            return up.urlparse(url)
        elif isinstance(url, up.ParseResult):
            return url
        else:
            raise TypeError(
                'url must be "str" or "urllib.parse.ParseResult" object')

    def validate_container_path(self, container_path):
        if isinstance(container_path, Path):
            return container_path
        elif isinstance(container_path, str):
            return Path(container_path)
        else:
            raise TypeError(
                'container_path must be "str" or "pathlib.Path" object')

    def validate_selector(self, selector):
        if isinstance(selector, str):
            return selector
        else:
            raise TypeError('selector must be str')

    def parse_title(self, post):
        ttl = post.select_one(self.selector_title)
        return ttl.get_text(strip=True)

    def parse_body(self, post):
        body = post.select_one(self.selector_body)
        divs = body.find_all(
            class_=['sm_icon_mini', 'ad-yads_common', 'bbs_preview', 'exblog_cpc', 'clear'])
        [div.decompose() for div in divs]
        [comment.extract() for comment in body.find_all(
            text=lambda x: isinstance(x, Comment))]
        return body.prettify()

    def parse_date(self, post):
        reg_pat = r'^\d{4}-\d{1,2}-\d{1,2}'
        times = post.select(self.selector_time + ' a')
        for time in times:
            time_str = time.get_text()
            if re.search(reg_pat, time_str):
                return datetime.strptime(time_str, '%Y-%m-%d %H:%M')

    def make_month_archive_url(self, y, m):
        anchive_url = datetime(y, m, 1)
        url_str = anchive_url.strftime('m%Y-%m-%d')
        return up.urljoin(self.url.geturl(), url_str)

    def get_indv_url_from_month_archive_urls(self, archive_urls):
        indv_urls = []
        for arc_url in archive_urls:
            soup = get_soup(arc_url)
            indv_urls.extend(self.extruct_indv_urls_from_archive_soup(soup))
        return indv_urls

    def extruct_indv_urls_from_archive_soup(self, soup):
        indv_urls = []
        titles = soup.select(self.selector_title)

        for title in titles:
            try:
                url = title.a.get('href')
                if self.if_indv_url(url):
                    indv_urls.append(url)
            except AttributeError:
                continue
        return indv_urls

    def if_indv_url(self, url):
        url = up.urlparse(url)
        if (url.netloc == self.url.netloc) and re.search(r'^/\d*/$', url.path):
            return True
        else:
            return False

    def date_iter(self):
        for year, month_list in self.date_dict.items():
            for month in month_list:
                yield (year, month)

    def scrape(self):
        entries = []
        indv_urls = self.get_indv_urls()
        for i_url in tqdm(indv_urls):
            entries.append(self.parse_indv_page(i_url))
        return list(entries)

    def parse_indv_page(self, indv_url):
        post = get_soup(indv_url)
        entry = {
            'title': self.parse_title(post),
            'body': self.parse_body(post),
            'date': self.parse_date(post)
        }
        return entry

    def get_indv_urls(self):
        dates = self.date_iter()
        archive_urls = map(
            lambda y_m: self.make_month_archive_url(*y_m), dates)
        return self.get_indv_url_from_month_archive_urls(archive_urls)

