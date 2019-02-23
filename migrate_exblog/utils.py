from .scrape_exblog import ScrapeExblog
import re


class ParseRange:
    def __init__(self, range_dic):
        self.range_dic = range_dic
        self.single_pat = re.compile(r'^(?P<y>\d{4})$')
        self.mult_pat = re.compile(r'^(?P<y1>\d{4})-(?P<y2>\d{4})$')

    def parse(self):
        range_dic = {}
        for k, v in self.range_dic.items():
            month_list = self.parse_month(v)
            single_match = self.single_pat.match(k)
            mult_match = self.mult_pat.match(k)
            if single_match:
                year = self.pick_year(single_match)
                range_dic[year] = month_list
            elif mult_match:
                y1, y2 = self.pick_years(mult_match)
                for y in range(y1, y2+1):
                    range_dic[y] = month_list
        return range_dic

    def pick_years(self, match):
        dic = match.groupdict()
        y1 = int(dic['y1'])
        y2 = int(dic['y2'])
        if y1 > y2:
            raise ValueError(f'{y1} is larger than {y2}')
        return y1, y2

    def pick_year(self, match):
        return int(match.groupdict()['y'])

    def parse_month(self, v):
        if v == 'all':
            return list(range(1, 13))
        elif isinstance(v, list) and all([1 <= m <= 12 and isinstance(m, int) for m in v]):
            return v


def data_wrapper(data, **kwargs):
    """for debug"""
    for i, v in kwargs.items():
        data[i] = v


def make_scraper(conf):
    p = ParseRange(conf['date'])
    date_dict = p.parse()

    scraper = ScrapeExblog(
        url=conf['url'],
        date_dict=date_dict,
        selector_title=conf['selector_title'],
        selector_body=conf['selector_body'],
    )
    return scraper
