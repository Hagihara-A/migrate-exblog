from pathlib import Path


class ConstructMTtext:
    def __init__(self,
                 mtTemplatePath=Path('mttemplate.txt'),
                 output_path=Path('../migrate.mt.txt')):
        path = self.template_pathValidation(mtTemplatePath)
        self.output_path = self.template_pathValidation(output_path)
        with path.open('r') as f:
            self.MTtemplate = f.read()

    def template_pathValidation(self, path):
        if isinstance(path, Path):
            return path
        elif isinstance(path, str):
            return Path(path)
        else:
            raise TypeError('path must be "str" or "pathlib.Path" object')

    def makeMTText(self, title, body, date, category=''):
        return self.MTtemplate.format(title=title,
                                      body=body,
                                      date=date.strftime('%m/%d/%Y %H:%M:%S'),
                                      category=category)

    def constructMTtextFromMonthEntries(self, monthEntries):
        MTfield = ''
        for monthEntry in monthEntries:
            MTfield += self.constructMTtextFromDayEntries(monthEntry)
        return MTfield

    def constructMTtextFromDayEntries(self, dayEntries):
        MTfield = ''
        for dayEntry in dayEntries:
            MTfield += self.makeMTText(**dayEntry)
            MTfield += '-' * 8 + '\n'

        return MTfield

    def saveMTtext(self, text):
        with self.output_path.open('w') as f:
            f.write(text)
