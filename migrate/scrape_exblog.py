import re
import types
import urllib.parse as up
from datetime import datetime
from pathlib import Path
from time import sleep

import requests
from bs4 import BeautifulSoup, Comment


def get(*args, interval=0.5, **kwargs):
    sleep(interval)
    return requests.get(*args, **kwargs)


def get_soup(*args, **kwargs):
    res = get(*args, **kwargs)
    res.encoding = res.apparent_encoding
    return BeautifulSoup(res.content, 'lxml')


class ScrapeExblog:
    def __init__(self,
                 url,
                 selector_post,
                 selector_title,
                 selector_body,
                 selector_foot,
                 selector_time='.TIME'):
        self.url = self.validate_url(url)
        self.selector_post = self.validate_selector(selector_post)
        self.selector_title = self.validate_selector(selector_title)
        self.selector_body = self.validate_selector(selector_body)
        self.selector_foot = self.validate_selector(selector_foot)
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
        return ttl.get_text().strip()

    def parse_body(self, post):
        body = post.select_one(self.selector_body)
        divs = body.find_all(
            class_=['sm_icon_mini', 'ad-yads_common', 'bbs_preview', 'exblog_cpc', 'clear'])
        [div.decompose() for div in divs]
        [comment.extract() for comment in body.find_all(
            text=lambda x: isinstance(x, Comment))]
        return body.prettify()

    def parse_date(self, soup):
        footer = soup.select_one(self.selector_foot)
        time = footer.select_one('.TIME')
        anchor = time.find('a', text=re.compile(r'^\d{4}-\d{1,2}-\d{1,2}'))
        time = anchor.get_text()
        return datetime.strptime(time, '%Y-%m-%d %H:%M')

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
            url = title.a.get('href')
            if self.if_indv_url(url):
                indv_urls.append(url)
        return indv_urls

    def if_indv_url(self, url):
        url = up.urlparse(url)
        if url.netloc == self.url.netloc and re.search(r'\d{9}', url.path):
            return True
        else:
            return False

    def date_iter(self):
        for year in range(self.years[0], self.years[1] + 1):
            for month in range(1, 13):
                if self.exclude_func(year, month):
                    yield (year, month)

    def scrape(self):
        indv_urls = self.get_indv_urls()
        entries = map(self.parse_indv_page, indv_urls)
        return list(entries)

    def parse_indv_page(self, indv_url):
        soup = get_soup(indv_url)
        post = soup.select_one(self.selector_post)
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

    @property
    def years(self):
        return self._years

    @years.setter
    def years(self, years):
        if isinstance(years, int):
            self._years = (years, years)
        elif isinstance(years, tuple) and len(years) == 2:
            self._years = years
        else:
            raise TypeError('years must be int or list')

    @property
    def exclude_func(self):
        return self._exclude_func

    @exclude_func.setter
    def exclude_func(self, func):
        if isinstance(func, types.FunctionType):
            self._exclude_func = func
        else:
            raise TypeError('exclude_func must be function')
