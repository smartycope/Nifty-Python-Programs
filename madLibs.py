import re, argparse, randomwordz

description = 'Mad Libs!'
parser = argparse.ArgumentParser(description=description)
parser.add_argument('file', help='The path to the madlibs file', nargs='+')
parser.add_argument('-a', '--auto', help='Auto fill the madlibs for you', action='store_true')
args = parser.parse_args()

adj = re.compile(r'#\w+')
rw = randomwordz.WordGenerator()

def getString(filepath):
    try:
        with open(filepath, 'r') as f:
            return f.read()
    except FileNotFoundError:
        try:
            with open(filepath + '.txt', 'r') as f:
                return f.read()
        except FileNotFoundError:
            print('Could not open file.')
            exit(0)

def getAdjs(string):
    return adj.findall(string)

def askForAdjs(adjs):
    ans = []
    for i in adjs:
        ans.append(input(i[1:] + ': '))
    return ans

def replaceAdjs(replacements, string):
    for i in replacements:
        string = adj.sub(i, string, count=1)
    return string

def getRandAdjs(adjs):
    returnMe = []
    for i in adjs:
        if i == '?':
            returnMe.append('{unknown part of speech}')
        else:
            returnMe.append(rw.get_random(i))
    return returnMe


def mapAdjs(adjs):
    returnMe = []
    # ['ADJ', 'ADP', 'CONJ', 'DET', 'NOUN', 'NUM', 'PRON', 'PRT', 'VERB', 'NAME']

    for i in adjs:
        if i.lower() == '#noun':
            returnMe.append('NOUN')
        elif i.lower() == '#verb':
            returnMe.append('VERB')
        elif i.lower() == '#adjective':
            returnMe.append('ADJ')
        elif i.lower() == '#conjunction':
            returnMe.append('CONJ')
        elif i.lower() == '#pronoun':
            returnMe.append('PRON')
        # As far as I can tell...
        elif i.lower() == '#preposition':
            returnMe.append('ADP')
        elif i.lower() == '#number':
            returnMe.append('NUM')
        elif i.lower() == '#name':
            returnMe.append('NAME')
        elif i.lower() == '#???':
            returnMe.append('DET')
        elif i.lower() in ['#interjection', '#adverb']:
            returnMe.append('PRT')
        else:
            returnMe.append('?')
    return returnMe
        
    

string = getString(args.file[0])

if args.auto:
    print(replaceAdjs(getRandAdjs(mapAdjs(getAdjs(string))), string))
else:
    print(replaceAdjs(askForAdjs(getAdjs(string)), string))
