import json
from pathlib import Path
from pprint import pprint

from migrate.entries_to_mt import ConstructMTtext
from migrate.scrape_exblog import ScrapeExblog

ABS_PATH = Path(__file__).resolve()
ABS_DIR = ABS_PATH.parent


def exec(data):
    scraper = ScrapeExblog(
        url=data['url'],
        selector_post=data['selector_post'],
        selector_title=data['selector_title'],
        selector_body=data['selector_body'],
        selector_foot=data['selector_foot']
    )
    if data['is_test']:
        test_year = data['test_year']
        test_month = data['test_month']
        scraper.years = test_year
        scraper.exclude_func = lambda y, m: y == test_year and m == test_month
    else:
        scraper.years = data['years']
    return scraper.scrape()


def dataWrapper(data, **kwargs):
    """for debug"""
    for i, v in kwargs.items():
        data[i] = v


def main():
    input_path = ABS_DIR / 'input.json'
    with input_path.open('r') as f:
        data = json.load(f)

    print('your input data is as follows')
    pprint(data)
    input('OK?')
    entries = exec(data)
    parser = ConstructMTtext()
    mttext = parser.make_mttext(entries)
    parser.save(mttext)
    print('finished')


if __name__ == '__main__':
    main()
