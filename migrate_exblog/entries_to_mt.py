from pathlib import Path

ABS_PATH = Path(__file__).resolve()
ABS_DIR = ABS_PATH.parent


class ConstructMTtext:
    """convert parsed entries to MT formatted text

    Attributes:
        make_mttext: make MT formatted text from list of parsed entries

    TODO:
        this should not be class. change to function.
    """

    def __init__(self,
                 mt_template_path=ABS_DIR / 'mt_template.txt'):
        path = Path(mt_template_path)
        with path.open('r') as f:
            self.MTtemplate = f.read()

    def format_mttext(self, title, body, date, category=''):
        return self.MTtemplate.format(title=title,
                                      body=body,
                                      date=date.strftime('%m/%d/%Y %H:%M:%S'),
                                      category=category)

    def make_mttext(self, entries):
        MTfield = ''
        for entry in entries:
            MTfield += self.format_mttext(**entry)
            MTfield += '-' * 8 + '\n'

        return MTfield
