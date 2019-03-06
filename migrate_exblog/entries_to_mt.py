from pathlib import Path

ABS_PATH = Path(__file__).resolve()
ABS_DIR = ABS_PATH.parent


class ConstructMTtext:
    """convert parsed entries to MT formatted text

    Attributes:
        make_mttext: make MT formatted text from list of parsed entries
    """

    def __init__(self,
                 mt_template_path=ABS_DIR / 'mt_template.txt'):
        path = Path(mt_template_path)
        with path.open('r') as f:
            self.MTtemplate = f.read()

    def format_mttext(self, title, body, date, category):
        """format entries

        Arguments:
            title {str} -- title
            body {str} -- body
            date {datetime.datetime} -- published date
            category {str} -- category

        Returns:
            str -- Mt formatted entries

        Example:
            >>> from migrate_exblog.entries_to_mt import ConstructMTtext
            >>> from datetime import datetime
            >>> formatter = ConstructMTtext()
            >>> entry = {'title': 'this is title', 'body': 'this is body', 'date': datetime(2000,1,1,1,1), 'category': 'sample category'}
            >>> formatter.format_mttext(**entry)
            'TITLE: this is title\\nSTATUS: Publish\\nDATE: 01/01/2000 01:01:00\\nCATEGORY: sample category\\n-----\\nBODY:\\nthis is body\\n-----\\n'
        """

        return self.MTtemplate.format(title=title,
                                      body=body,
                                      date=date.strftime('%m/%d/%Y %H:%M:%S'),
                                      category=category)

    def make_mttext(self, entries):
        """make MT formatted text

        Arguments:
            entries {list of dict} -- list of dict of parsed entries

        Returns:
            str -- MT formatted text
        """

        MTtext = ''
        for entry in entries:
            MTtext += self.format_mttext(**entry)
            MTtext += '-' * 8 + '\n'

        return MTtext


if __name__ == "__main__":
    import doctest
    doctest.testmod()
