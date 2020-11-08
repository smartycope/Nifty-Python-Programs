import argparse, math

description = 'A helpful tool to visualize number of different bases'

parser = argparse.ArgumentParser(description=description)
parser.add_argument('input',                help='The input numbers',                        nargs='+')
# parser.add_argument('-v' , '--verbose',                                                    action='store_true')
parser.add_argument('-b', '--input-base',   help='Specify an input base',                    type=int, default=0)
parser.add_argument('-B', '--output-base',  help='Specify an output base',                   type=int, default=2)
parser.add_argument('-e', '--endian',       help='Specify the endian',                       type=str, default='little', choices=['little', 'big'])
parser.add_argument('-l', '--label',        help='Specify what kind of label to add',        type=str, default='power',  choices=['power, index, count, none'])
parser.add_argument('-t', '--translate',    help='Specify a base to convert the input to',   type=int, default=10)
parser.add_argument('-c', '--no-colors',    help='Don\'t use colors',                        action='store_true')
parser.add_argument('-p', '--pad',          help='Specify the size of the number',           type=int, default=None)
parser.add_argument('-u', '--no-underline', help='Don\'t underline the indecies',            action='store_true')
parser.add_argument('-z', '--start-0',      help='Start the indecies from 0',                action='store_true')
# parser.add_argument('-z', '--start-0',      help='Start the indecies from 0',                action='store_true')

args = parser.parse_args()


def underline(s):
    if args.no_underline:
        return s
    else:
        return f'\x1b[4m{s}\x1b[24m'

def baseN(num,b,numerals="0123456789abcdefghijklmnopqrstuvwxyz"):
    return ((num == 0) and numerals[0]) or (baseN(num // b, b, numerals).lstrip(numerals[0]) + numerals[num % b])

def getBase(string):
    hex = ['0x', '#', 'h', 'hex', '\\x']
    oct = ['o', 'q', '0o', '0q', '\\', '@', '&', '$']
    bin = ['b', 'bin', 'bin ', '%', '0b', '#b']

    for i in bin:
        if string[0:(len(i)-1)].lower() == i or string[-1].lower() == 'b':
            return 2
    for i in oct:
        if string[0:(len(i)-1)].lower() == i or string[-1].lower() == 'o':
            return 8
    for i in hex:
        if string[0:(len(i)-1)].lower() == i or string[-1].lower() == 'h':
            return 16
    
    return args.translate

def ilen(num):
    return int(math.log10(num)) + 1

def displayLabel(power, littleEndian, start0, spacer, maxLength):
    if littleEndian:
        iterate = reversed(range(not start0, maxLength + (not start0)))
    else:
        iterate = range(not start0, maxLength + (not start0))

    for i in iterate:
        if power:
            tmp = format(2**(i - 1), str(len(spacer) + 1)) # str(ilen(2**(i - 1)) + 1))
        else:
            tmp = format(i, str(len(spacer) + 1))

        print(underline(tmp), underline(spacer), end='', sep='')

#* Display the numbers
def displayNum(string, spacer, littleEndian, maxLen, inBase=0, outBase=2, length=None, colors=True):
    if not inBase:
        base = getBase(string)
    else:
        base = inBase

    if length is None:
        # Round to the nearest (base / 4)
        length = int(maxLen / base) * base
    # if args.label == 'power':
        # spacer = ' ' *
        # pass

    
    num = str(int(string, inBase))

    # num = (spacer * 2).join(format(string, '0' + str(length) + 'b'))

    print('\n', ' ' * len(spacer), sep='', end='')

    if littleEndian:
        iterate = num
    else:
        iterate = reversed(num)

    for char in iterate:
        if colors:
            if base == 2 and char == '1':
                print(oneColor, char, spacer, resetColor, sep='', end='')
            # Uncomment this if you want to color spaces seperately
            # elif i == ' ':
            #     coloredBinNum += spaceColor + ' '
            elif base == 2 and char == '0':
                print(zeroColor, char, resetColor, sep='', end='')
        else:
            print(char, spacer, sep='', end='')

    print()


def getSpacer(power, maxLength):
    if power:
        return ' ' * (ilen(2**(maxLength - 1)))
    else:
        return ' ' * (ilen(maxLength) - 1)

#* Check that all the base systems are the same (unless the user hasns't specified an input base and has specified no idecies)
def verifyBases(nums, label, inputBase):
    for i in nums:
        if label != 'none' or inputBase:
            if getBase(i) != getBase(nums[0]):
                print('Cannot mix base systems without -l none specified')
                exit(0)


# if args.pad is None:
#     maxLength = max(nums, key=ilen)
# else:
#     maxLength = args.pad

resetColor = u'\033[0m'
oneColor   = u'\033[42m'
zeroColor  = u'\033[44m'
spaceColor = resetColor


verifyBases(args.input, args.label, args.input_base)

if args.pad is None:
    longestInput = max(args.input, key=lambda n: ilen(int(n, args.input_base)))
    maxLength = ilen(int(longestInput, args.input_base))

    if not args.input_base:
        base = getBase(longestInput)
    else:
        base = args.input_base

    l = int(maxLength / base) * base
else:
    l = args.pad

spacer = getSpacer(args.label.lower() == 'power', l)

if args.label.lower() != 'none':
    displayLabel(args.label.lower() == 'power', args.label.lower() == 'little', args.start_0, spacer, maxLength)

for i in args.input:
    displayNum(i, spacer, args.endian.lower() == 'little', maxLength, inBase=args.input_base, outBase=args.output_base, length=args.pad, colors=not args.no_colors)
