import re

from bs4 import BeautifulSoup

from .entries_to_mt import ConstructMTtext
from .scrape_exblog import ScrapeExblog

PAT_TITLE = re.compile(r'<\$postsubject\$>')
PAT_BODY = re.compile(r'<\$postcont\$>')
PAT_TAIL = re.compile(r'<\$posttail\$>')


def bake(url, structure_html, one_month=False, verbose=False):
    '''returns MT formatted entries

    Arguments:
        url {str} -- url to scrape
        structure_html {str} -- html that represents structure of blog-post

    Keyword Arguments:
        one_month {bool} -- scrape only one month to test (default: {False})
        verbose {bool} -- show progress bar (default: {False})

    Returns:
        str -- MT formatted entries
    '''

    class_dict = get_correct_class(structure_html)
    return bake_from_class_dict(url=url, class_dict=class_dict, one_month=one_month, verbose=verbose)


def bake_from_class_dict(url, class_dict, one_month=False, verbose=False):
    '''bake func that recieves class_dict instead of structure_html

    Arguments:
        url {str} -- url to scrape
        class_dict {dict of str} -- dict that express parent-class of title, content and footer

    Keyword Arguments:
        one_month {bool} -- scrape only one month to test (default: {False})
        verbose {bool} -- show progress bar (default: {False})

    Returns:
        str -- MT formatted entries
    '''

    scraper = ScrapeExblog(url=url, **class_dict)
    if one_month:
        entries = scraper.scrape_one_month(verbose=verbose)
    else:
        entries = scraper.scrape_all(verbose=verbose)
    mtparser = ConstructMTtext()
    mttext = mtparser.make_mttext(entries)
    return mttext


def get_correct_class(structure_html):
    '''parse parent class of title, content and footer

    Arguments:
        structure_html {str} -- html that represents structure of blog-post

    Returns:
        dict of str -- dict of parent class
    '''

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
