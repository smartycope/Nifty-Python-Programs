import re, os
from urllib.request import urlopen, Request
# from html.parser import HTMLParser
from urllib.parse import urlparse
# from BeautifulSoup import BeautifulSoup
from bs4 import BeautifulSoup
# import bs4
# from bs4 import *

def printFile(stuffToPrint, fileName):
    # os.system('touch ' + fileName)
    with open(fileName, 'w') as file:
        file.write(str(stuffToPrint))


def insert(pattern, index, string):
    return string[:index] + pattern + string[index:]


# import bs4

def getPOTD():
    testFile = r'/home/Robert/hello/Nifty Python Programs/test.del'
    # html = urlopen('https://www.poetryfoundation.org/poems/poem-of-the-day').read()
    html = Request('https://www.poetryfoundation.org/poems/poem-of-the-day', headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(html).read()
    html_parsed = BeautifulSoup(webpage, 'html.parser').find('div', attrs={'class':'o-poem'}).text
    # print(html_parsed)
    # printFile(html_parsed, r'/home/Robert/hello/Nifty Python Programs/test.del')
    # html = urlparse('https://www.poetryfoundation.org/poems/poem-of-the-day')
    # printFile(html_parsed.find('div', attrs={'class':'o-poem'}), testFile)
    num = 0

    # while True:
    for _ in range():
        print(f"Found {num} matches")
        # match = re.match(r'[A-Z]', html_parsed)
        index = html_parsed.find('A-Z')
    # html_parsed.insert('\n', match.endpos - 1)
        insert('\n', index, html_parsed)
        num += 1

    # printFile(html_parsed, testFile)
    print(html_parsed)
    # ).insert('\n'), testFile)
    '''
    # print(type(html))
    items = re.find(r'<span class="def" htag="span" hclass="def">(\w+)</span>', str(html), re.S)
    <div class="o-poem">
        <div style="text-indent: -1em; padding-left: 1em;">Why is it, in Bristol Bay, a sea cormorant<br></div><div style="text-indent: -1em; padding-left: 1em;">hovers, sings a two-fold song with a hinged cover<br></div><div style="text-indent: -1em; padding-left: 1em;"> <br></div><div style="text-indent: -1em; padding-left: 1em;">for a mouth, teeth set in sockets, with a hissing grind<br></div><div style="text-indent: -1em; padding-left: 1em;">of spikelets biting the air? Dip one.<br></div><div style="text-indent: -1em; padding-left: 1em;"> <br></div><div style="text-indent: -1em; padding-left: 1em;">The lips of vanished flames in lava coals<br></div><div style="text-indent: -1em; padding-left: 1em;">glow...<br></div><div style="text-indent: -1em; padding-left: 1em;"><br></div>
    </div>
    # print(html)
    # print('-------------------------------')
    print(items)
    defs = [re.sub('<.*?>','', x).strip() for x in items]
    print('-------------------------------')
    print(defs)
    for i, d in enumerate(defs):
        print('\n', '%s'%(i+1), d)
    '''

getPOTD()















import re
from urllib.request import urlopen
# from html.parser import HTMLParser
from urllib.parse import urlparse
# from BeautifulSoup import BeautifulSoup
from bs4 import BeautifulSoup
# import bs4
# from bs4 import *

# import bs4

def getPOTD():
    html = urlopen('https://www.poetryfoundation.org/poems/poem-of-the-day').read()
    html_parsed = BeautifulSoup(html)
    # html = urlparse('https://www.poetryfoundation.org/poems/poem-of-the-day')
    print(html_parsed.body.find('div', attrs={'class':'container'}).text)
    '''
    # print(type(html))
    items = re.find(r'<span class="def" htag="span" hclass="def">(\w+)</span>', str(html), re.S)
    <div class="o-poem">
        <div style="text-indent: -1em; padding-left: 1em;">Why is it, in Bristol Bay, a sea cormorant<br></div><div style="text-indent: -1em; padding-left: 1em;">hovers, sings a two-fold song with a hinged cover<br></div><div style="text-indent: -1em; padding-left: 1em;"> <br></div><div style="text-indent: -1em; padding-left: 1em;">for a mouth, teeth set in sockets, with a hissing grind<br></div><div style="text-indent: -1em; padding-left: 1em;">of spikelets biting the air? Dip one.<br></div><div style="text-indent: -1em; padding-left: 1em;"> <br></div><div style="text-indent: -1em; padding-left: 1em;">The lips of vanished flames in lava coals<br></div><div style="text-indent: -1em; padding-left: 1em;">glow...<br></div><div style="text-indent: -1em; padding-left: 1em;"><br></div>
    </div>
    # print(html)
    # print('-------------------------------')
    print(items)
    defs = [re.sub('<.*?>','', x).strip() for x in items]
    print('-------------------------------')
    print(defs)
    for i, d in enumerate(defs):
        print('\n', '%s'%(i+1), d)
    '''

getPOTD()
