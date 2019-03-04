import re
from bs4 import BeautifulSoup

from .entries_to_mt import ConstructMTtext
from .scrape_exblog import ScrapeExblog


def bake(url, design_html):
    class_dict = get_correct_class(design_html)
    return bake_from_class_dict(url=url, class_dict=class_dict)


def bake_from_class_dict(url, class_dict):
    scraper = ScrapeExblog(url=url, **class_dict)
    entries = scraper.scrape()
    mtparser = ConstructMTtext()
    mttext = mtparser.make_mttext(entries)
    return mttext


def get_correct_class(design_html):
    soup = BeautifulSoup(design_html)
    return {
        'selector_post': get_post_class(soup),
        'selector_title': get_title_class(soup),
        'selector_body': get_body_class(soup),
        'selector_tail': get_tail_class(soup),
    }


def get_post_class(soup):
    pass


def get_title_class(soup):
    pass


def get_body_class(soup):
    pass


def get_tail_class(soup):
    pass
