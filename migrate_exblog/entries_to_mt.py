from pathlib import Path

ABS_PATH = Path(__file__).resolve()
ABS_DIR = ABS_PATH.parent


class ConstructMTtext:
    def __init__(self,
                 mt_template_path=ABS_DIR / 'mt_template.txt'):
        path = self.validate_path(mt_template_path)
        with path.open('r') as f:
            self.MTtemplate = f.read()

    def validate_path(self, path):
        if isinstance(path, Path):
            return path
        elif isinstance(path, str):
            return Path(path)
        else:
            raise TypeError('path must be "str" or "pathlib.Path" object')

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
