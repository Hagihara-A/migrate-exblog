import re

from bs4 import BeautifulSoup

from .entries_to_mt import ConstructMTtext
from .scrape_exblog import ScrapeExblog

PAT_TITLE = re.compile(r'<\$postsubject\$>')
PAT_BODY = re.compile(r'<\$postcont\$>')
PAT_TAIL = re.compile(r'<\$posttail\$>')


def bake(url, structure_html, one_month=False, verbose=False):
    class_dict = get_correct_class(structure_html)
    return bake_from_class_dict(url=url, class_dict=class_dict, one_month=one_month, verbose=verbose)


def bake_from_class_dict(url, class_dict, one_month=False, verbose=False):
    scraper = ScrapeExblog(url=url, **class_dict)
    if one_month:
        entries = scraper.scrape_one_month(verbose=verbose)
    else:
        entries = scraper.scrape_all(verbose=verbose)
    mtparser = ConstructMTtext()
    mttext = mtparser.make_mttext(entries)
    return mttext


def get_correct_class(structure_html):
    soup = BeautifulSoup(structure_html, 'html.parser')
    return {
        'class_title': get_title_class(soup),
        'class_body': get_body_class(soup),
        'class_tail': get_tail_class(soup),
    }


def get_title_class(soup):
    return parent_class(soup, PAT_TITLE)


def get_body_class(soup):
    return parent_class(soup, PAT_BODY)


def get_tail_class(soup):
    return parent_class(soup, PAT_TAIL)


def parent_class(soup, pattern):
    return soup.find(text=pattern).parent.get('class')[0]
