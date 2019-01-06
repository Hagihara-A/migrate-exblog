from ConstructMTtext import ConstructMTtext
from scrapeExciteBlog import ScrapeExciteBlog
from pathlib import Path


class ExecStream:
    def __init__(self, isTest=True, **kwargs):
        if isTest:
            self.outputTest(**kwargs)
        else:
            self.scrapeAll(**kwargs)

    def outputTest(self,
                   url,
                   test_year=2018,
                   test_month=12,
                   container_path='entries',
                   selector_entry='.POST',
                   selector_title='.POST_TTL',
                   selector_body='.POST_CON',
                   selector_date='.TIME',
                   output_path=Path('migrate.mt.txt'),
                   mtTemplatePath=Path('mttemplate.txt'), **kwargs):
        scraper = ScrapeExciteBlog(url,
                                   container_path,
                                   selector_entry,
                                   selector_title,
                                   selector_body,
                                   selector_date)
        dayEntries = scraper.scrapeSinglePage(year=test_year, month=test_month)
        maker = ConstructMTtext(output_path=output_path)
        MTtext = maker.constructMTtextFromDayEntries(dayEntries)
        maker.saveMTtext(MTtext)

    def scrapeAll(self,
                  url,
                  years=(2000, 2019),
                  excludeFunc=lambda y, m: True,
                  container_path='entries',
                  selector_entry='.POST',
                  selector_title='.POST_TTL',
                  selector_body='.POST_CON',
                  selector_date='.TIME',
                  output_path=Path('migrate.mt.txt'),
                  mtTemplatePath=Path('mttemplate.txt'), **kwargs):

        scraper = ScrapeExciteBlog(url,
                                   container_path,
                                   selector_entry,
                                   selector_title,
                                   selector_body,
                                   selector_date)
        scraper.scrapeEntirePagesAndPickle(years=years, excludeFunc=excludeFunc)
        monthEntries = scraper.loadEveryMonthEntry()
        maker = ConstructMTtext(output_path=Path('migrate.mt.txt'))
        MTtext = maker.constructMTtextFromMonthEntries(monthEntries)
        maker.saveMTtext(MTtext)


if __name__ == '__main__':
    
    exe = ExecStream(isTest=True,
                     url='',
                     years=(2000, 2020),
                     test_year=2018,
                     test_month=12,
                     excludeFunc=lambda y, m: True,
                     container_path=Path('entries'),
                     selector_entry='.POST',
                     selector_title='.POST_TTL',
                     selector_body='.POST_CON',
                     selector_date='.TIME',
                     output_path=Path('migrate.mt.txt'))
