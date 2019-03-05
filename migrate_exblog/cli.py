import argparse as ap
import json
import os
from pathlib import Path

from .utils import bake, bake_from_class_dict

ABS_DIR = Path(__file__).parent
CONF_PATH = 'conf.json'
DEFAULT_CONF_PATH = ABS_DIR / CONF_PATH
OUTPUT_PATH = 'migrate.mt.txt'


def parse():
    parser = ap.ArgumentParser(fromfile_prefix_chars='@')
    parser.add_argument('-u', '--url', help='移行元のエキサイトブログのURLを指定してください')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-s', '--structure',
                       default='structure.html', help='構造htmlのパスを指定してください。デフォルトでは./structure.htmlです。')
    group.add_argument('-j', '--structure-json',
                       default=CONF_PATH, help=f'json形式の構造ファイルのパスを指定してください。デフォルトでは{CONF_PATH}です')

    parser.add_argument(
        '-o', '--output', default=f'{OUTPUT_PATH}', type=ap.FileType('w'), help=f'出力ファイルのパスを指定してください。デフォルトは{OUTPUT_PATH}です。')
    parser.add_argument('-t', '--test', action='store_true',
                        help='一月だけ出力することができます。')
    parser.add_argument('-v', '--verbose',
                        action='store_true', help='進行状況を表示します。')
    parser.set_defaults(func=migrate)

    subparsers = parser.add_subparsers()
    parser_conf = subparsers.add_parser('make-conf')
    parser_conf.add_argument(
        '-o', '--output', default=f'{CONF_PATH}', type=ap.FileType('w'), help=f'生成するテンプレートのパスを指定してください。デフォルトは{CONF_PATH}です。')
    parser_conf.set_defaults(func=output_conf)

    return parser.parse_args()


def output_conf(args):
    with DEFAULT_CONF_PATH.open('r') as f:
        args.output.write(f.read())


def migrate(args):
    cwd = os.getcwd()
    structure = os.path.join(cwd, args.structure)
    structure_json = os.path.join(cwd, args.structure_json)
    if os.path.exists(structure):
        with open(structure, 'r') as f:
            mttext = bake(url=args.url, structure_html=f.read(),
                          one_month=args.test, verbose=args.verbose)
    elif os.path.exists(structure_json):
        with open(structure_json, 'r') as f:
            class_dict = json.load(f)
            mttext = bake_from_class_dict(
                url=args.url, class_dict=class_dict, one_month=args.test, verbose=args.verbose)
    else:
        raise FileExistsError('no configure file exists')

    args.output.write(mttext)


def main():
    args = parse()
    args.func(args)


if __name__ == '__main__':
    main()
