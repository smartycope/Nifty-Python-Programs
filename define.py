import requests, json, argparse
from random_word import RandomWords
from autocorrect import Speller
from PyDictionary import PyDictionary

# def cli():
parser = argparse.ArgumentParser(description="Define a word".title())
group = parser.add_mutually_exclusive_group()
group.add_argument('word'             , help='The word to be defined'                    , nargs='?')
group.add_argument('-r'  , '--random' , help='Define a random word'                      , type=int, nargs='?', const=1         , default=False)
group.add_argument('-d'  , '--wotd'   , help='Define the word of the day'                                                       , action='store_true')
parser.add_argument('-v' , '--verbose'                                                                                          , action='store_true')
parser.add_argument('-a' , '--all'    , help='Give all the definitions of the word'                                             , action='store_true')
parser.add_argument('--rarity'        , help='Set the rarity of the random word (1-10)'  , type=int, choices=range(1, 10)       , default=5)
parser.add_argument('--length'        , help='Set the minimum length oaf the random word', type=int                             , default=1)
parser.add_argument('--use-py'        , help='Use the built-in python dictionary instead of the Oxford dictionary'              , action='store_true')
parser.add_argument('-f', '--force'   , help='Don\'t try to use the built-in python dictionary if Oxford doesn\'t have the word', action='store_true')

args = parser.parse_args()

# print('args =', args)

class NotAWordError(BaseException): pass

global used

def printDefs(string):
    # global used
    tmp = define(string)
    if tmp == "Sorry, that's not a word.":
        print(tmp)
        return
    if len(tmp) == 1:
        print(tmp.pop())
    else:
        print()
        for num, i in enumerate(tmp):
            print(num + 1, ': ', i.capitalize(), sep='')
    if args.verbose: print('Defined with the ', used, '.', sep='')

def define(word, usePy = args.use_py):
    if usePy:
        try:
            return definePy(word)
        except(NotAWordError):
            if args.verbose: print("Couldn't find the definition of", word, "in the python dictionary, trying Oxford...")
            if not args.force:
                return defineOxford(word)
            else:
                return "Sorry, that's not a word."
    else:
        tmp = defineOxford(word)
        if tmp == "Sorry, that's not a word.":
            if args.verbose: print("Couldn't find the definition of", word, "in the Oxford dictionary, trying default...")
            if not args.force:
                try:
                    return definePy(word)
                except(NotAWordError):
                    return "Sorry, that's not a word."
            else:
                return "Sorry, that's not a word."
        else:
            return tmp

def definePy(word):
    global used
    used = 'PyDictionary library'
    try:
        # print(PyDictionary().meaning(word))
        return PyDictionary().meaning(word)
    except:
        raise(NotAWordError)

def defineOxford(word):
    global used
    used = 'Oxford dictionary'

    # if args.verbose: print('Fetching the definition of ' + word + '...')
    app_id  = '4bf3ec4a'
    app_key = '51ef43cee6995c7d2231da8f12729878'

    language = 'en-us'
    fields = 'definitions'
    strictMatch = 'false'

    url = 'https://od-api.oxforddictionaries.com:443/api/v2/entries/' + language + '/' + word.lower() + '?fields=' + fields + '&strictMatch=' + strictMatch

    r = requests.get(url, headers = {'app_id': app_id, 'app_key': app_key})

    #                                     don't ask me why they make you do this, it's beyond stupid.
    # print(json.dumps(r.json()['results'].pop(0)['lexicalEntries'].pop(0)['entries'].pop(0)['senses'].pop(0)['subsenses'], indent=4), '\n\n\n')
    if args.all:
        try:
            listOfDef = [r.json()['results'].pop(0)['lexicalEntries'].pop(0)['entries'].pop(0)['senses'].pop(0)['definitions'].pop(0).capitalize()]
            try:
                dictsOfDef = r.json()['results'].pop(0)['lexicalEntries'].pop(0)['entries'].pop(0)['senses'].pop(0)['subsenses']# .capitalize()
                for i in dictsOfDef:
                    listOfDef.append(i['definitions'].pop(0))
            except(KeyError):
                pass
            return listOfDef
        except(KeyError):
                return "Sorry, that's not a word."
    else:
        try:
            return [r.json()['results'].pop(0)['lexicalEntries'].pop(0)['entries'].pop(0)['senses'].pop(0)['definitions'].pop(0).capitalize()]
        except(KeyError):
                return "Sorry, that's not a word."

def getRandomWord(rarity = 747192343, length = args.length):
    while True:
        try:
            return RandomWords().get_random_word(maxCorpusCount=rarity, minLength=length, hasDictionaryDef='true')
        except(Exception):
            if args.verbose:
                print('RandomWords() ran into an error, skipping it...')
            pass

def getWOTD():
    return str(json.loads(RandomWords().word_of_the_day())['word'])



if args.random:
    r = getRandomWord(rarity=int((747192343 ** (1 / 9)) ** args.rarity)) # this makes the word frequency more user friendly
    while define(r) == "Sorry, that's not a word.":
        if args.verbose:
            print(r, 'is not a word, trying again...')
        r = getRandomWord(rarity=args.rarity)
        # if args.verbose:
    #         return RandomWords().get_random_word(maxCorpusCount=rarity, minLength=length, hasDictionaryDef='true')
    #     else:
    print(r, '\b:', end=' ')
    printDefs(r)

elif args.wotd:
    w = getWOTD()
    print('The word of the day is' , w, "\b:", end=' ')
    printDefs(w)

elif args.word:
    if define(args.word) == "Sorry, that's not a word.":
        if args.verbose: print('Incorrect spelling, looking for possible corrections...')
        corrected = Speller().autocorrect_word(args.word)
        if corrected == args.word:
            print('Couldn\'t find a correct spelling. Quiting.') if args.verbose else print("Sorry, that's not a word.")
            exit(0)
        else:
            ans = input(args.word.capitalize() + ' is not a word. Did you mean ' + corrected + '?\n(y/n) ').lower()
            if ans == 'y':
                printDefs(corrected)
            else:
                exit(0)
    else:
        printDefs(args.word)

else:
    printDefs(input("Enter word: "))
