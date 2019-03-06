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
