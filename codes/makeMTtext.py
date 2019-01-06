from ConstructMTtext import ConstructMTtext
from scrapeExciteBlog import ScrapeExciteBlog
from pathlib import Path
import json
from pprint import pprint


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
                   output_path=Path('../migrate.mt.txt'),
                   mtTemplatePath=Path('mttemplate.txt'), **kwargs):
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
                  output_path=Path('../migrate.mt.txt'),
                  mtTemplatePath=Path('mttemplate.txt'), **kwargs):

        scraper = ScrapeExciteBlog(url=url,
                                   selector_entry=selector_entry,
                                   selector_title=selector_title,
                                   selector_body=selector_body,
                                   selector_date=selector_date,
                                   container_path=container_path)
        scraper.scrapeEntirePagesAndPickle(years=years, excludeFunc=excludeFunc)
        monthEntries = scraper.loadEveryMonthEntry()
        maker = ConstructMTtext(output_path=output_path)
        MTtext = maker.constructMTtextFromMonthEntries(monthEntries)
        maker.saveMTtext(MTtext)


def dataWrapper(data, **kwargs):
    for i, v in kwargs.items():
        data[i] = v


if __name__ == '__main__':
    input_path = Path('../input.json')
    with input_path.open('r') as f:
        data = json.load(f)
    dataWrapper(data, isTest=False, years=[2019, 2019])

    print('your input data is as follows')
    pprint(data)
    exe = ExecStream(**data)
