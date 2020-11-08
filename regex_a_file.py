import re
import sys

args = sys.argv
args.pop(0)

print(args)

filename = [args.pop(0) if len(args) else input('Filename: ')].pop(0)
pattern  = [args.pop(0) if len(args) else input('Search Pattern: ')].pop(0)
replace  = [args.pop(0) if len(args) else input('Replace with: ')].pop(0)
# replace  = re.sub(r'[\][\]', r'[\]]', replace)

print(f"\nFilename = {filename}, pattern = {pattern}, and replace = {replace}")

with open(filename, 'r') as f:
    subbedFile = re.sub(pattern, replace, f.read())

with open(filename, 'w') as f:
    f.write(subbedFile)

print('')
print(open(filename, 'r').read())