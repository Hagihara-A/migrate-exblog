import argparse as ap
import json
from pathlib import Path
from pprint import pprint

from .entries_to_mt import ConstructMTtext
from .utils import make_scraper

ABS_DIR = Path(__file__).parent
DEFAULT_JSON_PATH = ABS_DIR / 'input.json'


def parse():

    parser = ap.ArgumentParser()

    subparsers = parser.add_subparsers()

    parser_template = subparsers.add_parser('json-template')
    parser_template.add_argument('--json-template-path',
                                 default='./input.json', type=ap.FileType('w'))
    parser_template.set_defaults(func=output_json_template)

    parser_migrate = subparsers.add_parser('migrate')
    parser_migrate.add_argument(
        '--input-path', default='./input.json', type=ap.FileType('r'))
    parser_migrate.add_argument(
        '--output-path', default='./migrate.mt.txt', type=ap.FileType('w'))
    parser_migrate.set_defaults(func=migrate)

    def print_help(args):
        parser.print_help()

    parser.set_defaults(func=print_help)

    return parser.parse_args()


def output_json_template(args):
    with DEFAULT_JSON_PATH.open('rt') as f:
        default_json = f.read()
    args.json_template_path.write(default_json)


def migrate(args):
    data = json.load(args.input_path)
    print('your input data is as follows:')
    pprint(data)
    input('OK? press any key.')
    scraper = make_scraper(data)
    entries = scraper.scrape()
    mtparser = ConstructMTtext()
    mttext = mtparser.make_mttext(entries)
    args.output_path.write(mttext)


def main():
    args = parse()
    args.func(args)


if __name__ == '__main__':
    main()
