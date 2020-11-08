import argparse

description = ''

parser = argparse.ArgumentParser(description=description)
parser.add_argument('command', help='', nargs='+')
parser.add_argument('-', '--', help='', type=, default=)
parser.add_argument('-', '--', help='', type=, default=, choices=[])
parser.add_argument('-', '--', help='', action='store_true')

args = parser.parse_args()
