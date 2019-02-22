from .scrape_exblog import ScrapeExblog


def data_wrapper(data, **kwargs):
    """for debug"""
    for i, v in kwargs.items():
        data[i] = v


def make_scraper(data):
    scraper = ScrapeExblog(
        url=data['url'],
        years=data['years'],
        selector_title=data['selector_title'],
        selector_body=data['selector_body'],
    )
    if data['is_test']:
        test_year = data['test_year']
        test_month = data['test_month']
        scraper.years = test_year
        scraper.exclude_func = lambda y, m: y == test_year and m == test_month
    return scraper
