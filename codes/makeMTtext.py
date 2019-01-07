from ConstructMTtext import ConstructMTtext
from scrapeExciteBlog import ScrapeExciteBlog
from pathlib import Path
import json
from pprint import pprint

ABS_PATH = Path(__file__).resolve()


class ExecStream:
    def __init__(self, isTest=True, **kwargs):
        if isTest:
            self.outputTest(**kwargs)
        else:
            self.scrapeAll(**kwargs)

    def outputTest(self,
                   url,
                   test_year,
                   test_month,
                   selector_entry,
                   selector_title,
                   selector_body,
                   selector_date,
                   container_path='entries',
                   output_path=ABS_PATH.parents[1] / 'migrate.mt.txt',
                   mtTemplatePath=ABS_PATH.parent / 'mttemplate.txt',
                   **kwargs):
        scraper = ScrapeExciteBlog(url=url,
                                   selector_entry=selector_entry,
                                   selector_title=selector_title,
                                   selector_body=selector_body,
                                   selector_date=selector_date,
                                   container_path=container_path)
        dayEntries = scraper.scrapeSinglePage(year=test_year, month=test_month)
        maker = ConstructMTtext(output_path=output_path)
        MTtext = maker.constructMTtextFromDayEntries(dayEntries)
        maker.saveMTtext(MTtext)

    def scrapeAll(self,
                  url,
                  selector_entry,
                  selector_title,
                  selector_body,
                  selector_date,
                  years,
                  excludeFunc=lambda y, m: True,
                  container_path='entries',
                  output_path=ABS_PATH.parents[1] / 'migrate.mt.txt',
                  mtTemplatePath=ABS_PATH.parent / 'mttemplate.txt',
                  **kwargs):

        scraper = ScrapeExciteBlog(url=url,
                                   selector_entry=selector_entry,
                                   selector_title=selector_title,
                                   selector_body=selector_body,
                                   selector_date=selector_date,
                                   container_path=container_path)
        monthEntries = scraper.scrapeEntirePagesButPickle(years=years, excludeFunc=excludeFunc)
        maker = ConstructMTtext(output_path=output_path)
        MTtext = maker.constructMTtextFromMonthEntries(monthEntries)
        maker.saveMTtext(MTtext)


def dataWrapper(data, **kwargs):
    for i, v in kwargs.items():
        data[i] = v


def main():
    input_path = Path(__file__).resolve().parents[1] / 'input.json'
    with input_path.open('r') as f:
        data = json.load(f)
    dataWrapper(data, output_path=ABS_PATH.parents[1] / 'migrate.mt.txt', isTest=False)

    print('your input data is as follows')
    pprint(data)
    input('OK?')
    ExecStream(**data)


if __name__ == '__main__':
    main()
