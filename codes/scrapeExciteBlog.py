import requests
import re
from pathlib import Path
import pickle
from datetime import datetime
from bs4 import BeautifulSoup, Comment
import urllib


class ScrapeExciteBlog:
        def __init__(self,
                     url,
                     container_path,
                     selector_entry='.POST',
                     selector_title='.POST_TTL',
                     selector_body='.POST_CON',
                     selector_date='.TIME'):
            self.url = self.urlValidation(url)
            self.container_path = self.container_pathValidation(container_path)
            self.selector_entry = self.selectorValidation(selector_entry)
            self.selector_title = self.selectorValidation(selector_title)
            self.selector_body = self.selectorValidation(selector_body)
            self.selector_date = self.selectorValidation(selector_date)

        def urlValidation(self, url):
            if isinstance(url, str):
                return urllib.parse.urlparse(url)
            elif isinstance(url, urllib.parse.ParseResult):
                return url
            else:
                raise TypeError('url must be "str" or "urllib.parse.ParseResult" object')

        def container_pathValidation(self, container_path):
            if isinstance(container_path, Path):
                return container_path
            elif isinstance(container_path, str):
                return Path(container_path)
            else:
                raise TypeError('container_path must be "str" or "pathlib.Path" object')

        def selectorValidation(self, selector):
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
            divs = con.find_all(class_=['sm_icon_mini', 'ad-yads_common', 'bbs_preview', 'exblog_cpc', 'clear'])
            [div.decompose() for div in divs]
            [comment.extract() for comment in con.find_all(text=lambda x: isinstance(x, Comment))]
            return str(con)

        def extractDate(self, soup):
            time = soup.select(self.selector_date)
            time = self.validateTag(time)
            anchor = time.find('a', text=re.compile('^\d{4}-\d{1,2}-\d{1,2}'))
            time = anchor.get_text()
            return datetime.strptime(time, '%Y-%m-%d %H:%M')

        def validateTag(self, items):
            return items[0]

        def constructUrl(self, year, month):
            entryUrl = datetime(year, month, 1)
            url_str = entryUrl.strftime('m%Y-%m-%d')
            return urllib.parse.urljoin(self.url.geturl(), url_str)

        def pickleDayEntries(self, data, year, month):
            if not data:
                return
            dir = self.container_path / f'{year}'
            if not dir.exists():
                dir.mkdir(parents=True)

            file = dir / f'{month}.pickle'
            with file.open('wb') as f:
                pickle.dump(data, f)

        def scrapeAndPickleWithDateIter(self, date_iter):
            for y, m in date_iter:
                print(f'now processing {y}/{m}')
                url = self.constructUrl(y, m)
                dayEntries = self.scrapeDayEntriesFromMonthPage(url)
                self.pickleDayEntries(dayEntries, y, m)

        def makeDateIter(self, years=(2005, 2019), excludeFunc=lambda y, m: True):
            for year in range(years[0], years[1] + 1):
                for month in range(1, 13):
                    if excludeFunc(year, month):
                        yield (year, month)

        def scrapeEntirePagesAndPickle(self, years=(2005, 2019), excludeFunc=lambda y, m: True):
            date_iter = self.makeDateIter(years=years, excludeFunc=excludeFunc)
            self.scrapeAndPickleWithDateIter(date_iter)

        def loadEveryMonthEntry(self, deserialize=True):
            monthEntries = self.container_path.glob('**/*.pickle')
            if deserialize:
                def deserializer(pickledFile):
                    with pickledFile.open('rb') as f:
                        return pickle.load(f)
                monthEntries = list(map(deserializer, monthEntries))

            return monthEntries

        def scrapeSinglePage(self, year, month):
            url = self.constructUrl(year, month)
            return self.scrapeDayEntriesFromMonthPage(url)
