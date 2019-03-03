import argparse as ap
import json
from pathlib import Path
from pprint import pprint

from .utils import bake

ABS_DIR = Path(__file__).parent
CONF_PATH = './migrate-conf.json'
DEFAULT_CONF_PATH = ABS_DIR / CONF_PATH
OUTPUT_PATH = './migrate.mt.txt'


def parse():

    parser = ap.ArgumentParser()

    subparsers = parser.add_subparsers()

    parser_conf = subparsers.add_parser(
        'make-conf', description=f'<--config-file-path>に設定ファイルを作成します.デフォルトは{CONF_PATH}です.')
    parser_conf.add_argument('--config-file-path',
                             default=CONF_PATH, type=ap.FileType('w'),
                             help="設定ファイルのパスを指定してください.")
    parser_conf.set_defaults(func=output_json_template)

    parser_migrate = subparsers.add_parser(
        'migrate', description='ブログを出力します.')
    parser_migrate.add_argument(
        '--conf-path', default=CONF_PATH, type=ap.FileType('r'), help=f'設定ファイルのパスを指定してください.デフォルトでは{CONF_PATH}です.')
    parser_migrate.add_argument(
        '--output-path', default=OUTPUT_PATH, type=ap.FileType('w'), help=f'出力ファイルのパスを指定してください。デフォルトでは{OUTPUT_PATH}です.')
    parser_migrate.set_defaults(func=migrate)

    def print_help(args):
        parser.print_help()

    parser.set_defaults(func=print_help)

    return parser.parse_args()


def load_default_json(path=DEFAULT_CONF_PATH, jsonize=True):
    with path.open('r') as f:
        if jsonize:
            return json.load(f)
        else:
            return f


def output_json_template(args):
    default_json = load_default_json(jsonize=False).read()
    args.config_file_path.write(default_json)


def migrate(args, confirm=True):
    conf = json.load(args.conf_path)
    if confirm:
        print('your input data is as follows:')
        pprint(conf)
        input('OK? press any key.')
    mttext = bake(conf)
    args.output_path.write(mttext)


def main():
    args = parse()
    args.func(args)


if __name__ == '__main__':
    main()
