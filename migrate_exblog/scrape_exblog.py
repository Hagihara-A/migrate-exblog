import re
import urllib.parse as up
from datetime import datetime
from time import sleep

import requests
from bs4 import BeautifulSoup, Comment
from tqdm import tqdm


def get_soup(url, interval=0.5):
    """get soup of html in url and sleep

    Arguments:
        url {str} -- url to get soup

    Keyword Arguments:
        interval {float} -- interval to sleep (default: {0.5})

    Returns:
        BeautifulSoup -- BeautifulSoup object that parses html in url
    """
    res = requests.get(url)
    sleep(interval)
    res.encoding = res.apparent_encoding
    return BeautifulSoup(res.content, 'html.parser')


class ScrapeExblog:
    """scrape and parse exblog entries

    Raises:
        TypeError -- if url is not str

    Attributes:
        scrape_all: scrape all entries and returns parsed ones
        scrape_one_month: scrape entries posted during one month
    """

    def __init__(self,
                 url,
                 class_title,
                 class_body,
                 class_tail,
                 class_time='TIME'):
    """
    Arguments:
        url {str} -- url to scrape and parse
        class_title {str} -- parent class of title
        class_body {str} -- parent class of body
        class_tail {str} -- parent class of footer

    Keyword Arguments:
        class_time {str} -- footer's class placed in inner of class_tail. This is auto genereted by exblog (default: {'TIME'})

    Raises:
        TypeError -- if url is not str
    """

    self.url = self.validate_url(url)
    self.selector_title = self.class_to_selector(class_title)
    self.selector_body = self.class_to_selector(class_body)
    self.selector_tail = self.class_to_selector(class_tail)
    self.selector_time = self.class_to_selector(class_time)

    self.date_pat = re.compile(r'^\d{4}-\d{1,2}-\d{1,2}')
    self.tag_path_pat = re.compile(r'/i\d+/')

    def validate_url(self, url):
        if isinstance(url, str):
            return up.urlparse(url)
        else:
            raise TypeError(
                'url must be "str" or "urllib.parse.ParseResult" object')

    def class_to_selector(self, class_):
        if class_.startswith('.'):
            return class_
        elif class_ is None:
            return class_
        else:
            return '.' + class_

    def scrape_one_month(self, verbose=False):
        """scrape only one month. Probably recent month.

        Keyword Arguments:
            verbose {bool} -- show progress bar (default: {False})

        Returns:
            dict -- dict of parsed entries.Keys are 'title', 'body', 'date' and 'category'
        """

        entries = []
        month_archive_url = self.get_month_archive_urls()[0]
        indv_urls = self.get_indv_url_from_month_archive_urls(
            [month_archive_url])
        if verbose:
            indv_urls = tqdm(indv_urls)
        for i_url in indv_urls:
            entries.append(self.parse_indv_page(i_url))
        return entries

    def scrape_all(self, verbose=False):
        """scrape all entries

        Keyword Arguments:
            verbose {bool} -- show progress bar (default: {False})

        Returns:
            dict -- dict of parsed entries.Keys are 'title', 'body', 'date' and 'category'
        """

        entries = []
        indv_urls = self.get_indv_urls()
        if verbose:
            indv_urls = tqdm(indv_urls)
        for i_url in indv_urls:
            entries.append(self.parse_indv_page(i_url))
        return entries

    def get_indv_urls(self):
        month_archive_urls = self.get_month_archive_urls()
        return self.get_indv_url_from_month_archive_urls(month_archive_urls)

    def get_month_archive_urls(self):
        """get archive urls to get indidual urls.
        Note:
            all archive urls is listed on `self.url + '/m1900-01-01'`. what a poor url...

        Returns:
            list of str -- archive urls
        """

        month_archive_urls = []
        archive_url = up.urljoin(self.url.geturl(), 'm1900-01-01/')
        soup = get_soup(archive_url)
        archive_soup = soup.select_one('.ARCHIVE_BODY')
        for a in archive_soup.find_all('a'):
            href = a.get('href')
            if href:
                month_archive_urls.append(up.urljoin(self.url.geturl(), href))
        return month_archive_urls

    def get_indv_url_from_month_archive_urls(self, archive_urls):
        indv_urls = []
        for arc_url in archive_urls:
            soup = get_soup(arc_url)
            indv_urls.extend(self.extruct_indv_urls_from_archive_soup(soup))
        return indv_urls

    def extruct_indv_urls_from_archive_soup(self, soup):
        indv_urls = []
        archive_list = soup.select_one('.archivelist')

        for a in archive_list.find_all('a'):
            href = a.get('href')
            if self.if_indv_url(href):
                indv_urls.append(href)
        return indv_urls

    def if_indv_url(self, url):
        """judgbe whether url in individual url or not

        Note:
            individual url's path is sequence of int

        Arguments:
            url {str} -- url to judge

        Returns:
            bool -- True if individual url
        """
        url = up.urlparse(url)
        if (url.netloc == self.url.netloc) and re.search(r'^/\d*/$', url.path):
            return True
        else:
            return False

    def parse_indv_page(self, indv_url):
        post = get_soup(indv_url)
        post_time = post.select_one(
            self.selector_tail + ' ' + self.selector_time)
        entry = {
            'title': self.parse_title(post),
            'body': self.parse_body(post),
            'date': self.parse_date(post_time),
            'category': self.parse_category(post_time)
        }
        return entry

    def parse_title(self, post):
        ttl = post.select_one(self.selector_title)
        return ttl.get_text(strip=True)

    def parse_body(self, post):
        body = post.select_one(self.selector_body)
        # remove unnecessary divs
        divs = body.find_all(
            class_=['sm_icon_mini', 'ad-yads_common', 'bbs_preview', 'exblog_cpc', 'clear'])
        [div.decompose() for div in divs]
        [comment.extract() for comment in body.find_all(
            text=lambda x: isinstance(x, Comment))]
        return body.prettify()

    def parse_date(self, post_time):
        for a in post_time.find_all('a'):
            text = a.get_text()
            if self.date_pat.match(text):
                return datetime.strptime(text, '%Y-%m-%d %H:%M')

    def parse_category(self, post_time):
        for a in post_time.find_all('a'):
            url = up.urlparse(a.get('href'))
            if self.tag_path_pat.match(url.path):
                return a.get_text()
        return ''
