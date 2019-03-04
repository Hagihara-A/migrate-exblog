import re
import urllib.parse as up
from datetime import datetime
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
                 class_post,
                 class_title,
                 class_body,
                 class_tail,
                 class_time='TIME'):
        self.url = self.validate_url(url)
        self.selector_post = self.class_to_selector(class_post)
        self.selector_title = self.class_to_selector(class_title)
        self.selector_body = self.class_to_selector(class_body)
        self.selector_tail = self.class_to_selector(class_tail)
        self.selector_time = self.class_to_selector(class_time)

        self.entries = []

    def validate_url(self, url):
        if isinstance(url, str):
            return up.urlparse(url)
        elif isinstance(url, up.ParseResult):
            return url
        else:
            raise TypeError(
                'url must be "str" or "urllib.parse.ParseResult" object')

    def class_to_selector(self, class_):
        if class_.startswith('.'):
            return class_
        else:
            return '.' + class_

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

    def parse_category(self, post):
        pass

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

    def scrape(self, verbose=False):
        entries = []
        indv_urls = self.get_indv_urls()
        if verbose:
            indv_urls = tqdm(indv_urls)
        for i_url in indv_urls:
            entries.append(self.parse_indv_page(i_url))
        return entries

    def parse_indv_page(self, indv_url):
        post = get_soup(indv_url)
        entry = {
            'title': self.parse_title(post),
            'body': self.parse_body(post),
            'date': self.parse_date(post),
            'category': self.parse_category(post)
        }
        return entry

    def get_indv_urls(self):
        pass
