import re
import types
import urllib
from datetime import datetime
from pathlib import Path

import requests
from bs4 import BeautifulSoup, Comment


class ScrapeExblog:
    def __init__(self,
                 url,
                 selector_entry,
                 selector_title,
                 selector_body,
                 selector_date):
        self.url = self.validate_url(url)
        self.selector_entry = self.validate_selector(selector_entry)
        self.selector_title = self.validate_selector(selector_title)
        self.selector_body = self.validate_selector(selector_body)
        self.selector_date = self.validate_selector(selector_date)

        self.years = None
        self.exclude_func = lambda x: True

    def validate_url(self, url):
        if isinstance(url, str):
            return urllib.parse.urlparse(url)
        elif isinstance(url, urllib.parse.ParseResult):
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

    def scrapeDayEntriesFromMonthPage(self, url_str):
        r = requests.get(url_str)
        r.encoding = r.apparent_encoding
        soup = BeautifulSoup(r.content, 'lxml')
        return self.fetchDayentriesFromSoup(soup)

    def fetchDayentriesFromSoup(self, soup):
        dayEntries = []
        posts = soup.select(self.selector_entry)
        for post in posts:
            try:
                dayEntries.append(dict(
                    title=self.extractTitle(post),
                    body=self.extractBody(post),
                    date=self.extractDate(post),
                ))
            except (IndexError, AttributeError):
                continue
        return dayEntries

    def extractTitle(self, post):
        ttl = post.select(self.selector_title)
        ttl = self.validateTag(ttl)
        return ttl.get_text().replace('\u3000', '').strip()

    def extractBody(self, post):
        con = post.select(self.selector_body)
        con = self.validateTag(con)
        divs = con.find_all(
            class_=['sm_icon_mini', 'ad-yads_common', 'bbs_preview', 'exblog_cpc', 'clear'])
        [div.decompose() for div in divs]
        [comment.extract() for comment in con.find_all(
            text=lambda x: isinstance(x, Comment))]
        return str(con)

    def extractDate(self, soup):
        time = soup.select(self.selector_date)
        time = self.validateTag(time)
        anchor = time.find('a', text=re.compile(r'^\d{4}-\d{1,2}-\d{1,2}'))
        time = anchor.get_text()
        return datetime.strptime(time, '%Y-%m-%d %H:%M')

    def validateTag(self, items):
        return items[0]

    def constructUrl(self, year, month):
        entryUrl = datetime(year, month, 1)
        url_str = entryUrl.strftime('m%Y-%m-%d')
        return urllib.parse.urljoin(self.url.geturl(), url_str)

    def scrapeWithDateIter(self, date_iter):
        monthEntries = []
        for y, m in date_iter:
            print(f'now processing {y}/{m}')
            url = self.constructUrl(y, m)
            dayEntries = self.scrapeDayEntriesFromMonthPage(url)
            monthEntries.append(dayEntries)
        return monthEntries

    def date_iter(self):
        self.years[1] += 1
        for year in range(*self.years):
            for month in range(1, 13):
                if self.excludeFunc(year, month):
                    yield (year, month)

    def scrape(self):
        date_iter = self.date_iter
        return self.scrapeWithDateIter(date_iter=date_iter)

    @property
    def years(self):
        return self.years

    @years.setter
    def year(self, years):
        if isinstance(years, int):
            years = [years, years]
            self.years = years
        elif isinstance(years, list):
            self.years = years
        else:
            raise TypeError('years must be int pr list')

    @property
    def exclude_func(self):
        return self.exclude_func

    @exclude_func.setter
    def exclude_func(self, func):
        if isinstance(func, types.FunctionType):
            self.exclude_func = func
        else:
            raise TypeError('exclude_func must be function')