#!/usr/bin/python
import argparse

parser = argparse.ArgumentParser(description="Define a word".title())
parser.add_argument('fileName', help='The file to append to')
parser.add_argument('toAppend', help='Stuff to append to the file', nargs='*', default=[])
args = parser.parse_args()

with open(args.fileName, 'a') as file:
    file.write('\n')
    # for i in args.toAppend:
    #     file.write(i + ' ')
    # file.write('\b')
    for i in range(len(args.toAppend) - 1):
        file.write(args.toAppend[i] + ' ')
    file.write(args.toAppend[len(args.toAppend) - 1])