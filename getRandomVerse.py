import requests, json, os, re
from cowsay import cow
from random import randint, choice
from urllib.request import urlopen
from os.path import dirname, join
from bs4 import BeautifulSoup as bs
import bs4

DIR = dirname(__file__)
MANUAL = False
# CANNON_SELECTION = ("Book of Mormon", "Pearl of Great Price", "Doctorine and Covenants", "New Testament", "Old Testament")
CANNON_SELECTION = ("Book of Mormon", )

def addLines(string, width):
    pos, findSpace = 0, 0

    while pos < len(string) - width:
        pos     += width
        findSpace = pos

        while string[findSpace - 1] != ' ':
            findSpace -= 1

        string = string[:findSpace] + '\n' + string[findSpace:]

    return string

# summary = soup.head.meta.findNextSiblings()[4].get('content')
def fetchChapter(cannon, book, chap):
    url = f"https://www.churchofjesuschrist.org/study/scriptures/{cannon}/{book}/{chap}?lang=eng"
    soup = bs(urlopen(url).read(), 'lxml')
    return soup.body.div.div.findNextSibling().div.main.div.div.findNextSibling().findNextSibling().section.div.article.div.div


def getVerse(chapHtml, verse):
    def combineVerseHtml(html):
        elements = list(html.recursiveChildGenerator())
        skipNext = False

        for i in range(len(elements)):
            if len(elements) <= i:
                break

            elif type(elements[i]) is bs4.element.Tag and 'class' in elements[i].attrs and elements[i].attrs['class'] in (['study-note-ref'], ["marker"]):
                # print('removing', elements[i], 'and', elements[i+1])
                del elements[i]
                del elements[i + 1]

        return ''.join(i for i in elements if type(i) is bs4.element.NavigableString)

    for element in chapHtml.findChildren():
        if f'<span class="verse-number">{verse}' in str(element):
            return combineVerseHtml(element)

    #* Couldn't find the specified verse
    return None


def getVerseCount(chapHtml):
    highest = 0
    for element in chapHtml.findChildren():
        match = re.search(r'<span class\="verse\-number">(\d+)', str(element))
        if match:
            highest = max(highest, int(match.groups()[0]))
    return highest


def adjustReference(s, prettyVersions, add, cannon, chapter, book):
    if add:
        goodCannon = prettyVersions[cannon]  if cannon  in prettyVersions else cannon.title()
        goodBook   = prettyVersions[book]    if book    in prettyVersions else book.title()
        return f"{goodCannon} -- {goodBook} {chapter}:{s}"
    else:
        return s[2:]


def getKey(prettyName, prettyVersions):
    return list(prettyVersions.keys())[list(prettyVersions.values()).index(prettyName)] if prettyName in prettyVersions.values() else prettyName.lower()


def lookupBook(book, options):
    for cannon in options['cannons']:
        if book in options['books'][cannon]:
            return cannon
    return None


with open(join(DIR, 'scriptures.json'), 'r') as f:
    options, prettyNames = json.load(f)


if MANUAL:
    book, chap, verse = 'Habakkuk', 2, 20
    book = getKey(book, prettyNames)
    cannon = lookupBook(book, options)
else:
    # cannon = choice(options['cannons'])
    cannon = choice([getKey(i, prettyNames) for i in CANNON_SELECTION])
    book   = choice(options['books'][cannon])
    chap   = randint(1, options['chapters'][book])

soup = fetchChapter(cannon, book, chap)

if not MANUAL:
    verse = randint(1, getVerseCount(soup))

print(addLines(adjustReference(getVerse(soup, verse), prettyNames, True, cannon, chap, book), os.get_terminal_size().columns))
