import requests, random, json, os
from cowsay import cow
# import re
# from urllib.request import urlopen

# trello api key = 54d07639427faa733acb9f053875a089
# trello token   = 95cc4a76b985e33a0b28d9e397a4fd985a7a217bb4d666f81a5f753edc37dc60
# trello Oauth1 something = 883d0644400691bd3c282c2803bcc3e6978d0a6f101842a9b5f8b49cd6a13950

# oxford api 'credentials' = 4bf3ec4a
# oxford api key = 	51ef43cee6995c7d2231da8f12729878
# oxford api id  = 	4bf3ec4a

def define(word):
    app_id = '4bf3ec4a'
    app_key = '51ef43cee6995c7d2231da8f12729878'

    language = 'en-gb'
    # word_id = 'Ace'
    fields = 'definitions'
    strictMatch = 'false'

    url = 'https://od-api.oxforddictionaries.com:443/api/v2/entries/' + language + '/' + word.lower() + '?fields=' + fields + '&strictMatch=' + strictMatch

    r = requests.get(url, headers = {'app_id': app_id, 'app_key': app_key})

    # print("code {}\n".format(r.status_code))
    # print("text \n" + r.text)
    #                                                    don't ask me why they make you do this, it's beyond stupid.
    return r.json()['results'].pop(0)['lexicalEntries'].pop(0)['entries'].pop(0)['senses'].pop(0)['definitions'].pop(0).capitalize()
    # print('json \n', json.loads(r.json()))
    # print(re.findall(r"definitions", r.text))
    # print(r.json()['results']['lexical entries']['entries']['senses']['definitions'])



# def define(word):
#     html = urlopen('https://www.oxfordlearnersdictionaries.com/definition/english/' + word + '?q=' + word).read()
#     # print(type(html))
#     items = re.findall(r'<span class="def" htag="span" hclass="def">(\w+)</span>', str(html), re.S)
#     # print(html)
#     # print('-------------------------------')
#     print(items)
#     defs = [re.sub('<.*?>','', x).strip() for x in items]
#     print('-------------------------------')
#     print(defs)
#     for i, d in enumerate(defs):
#         print('\n', '%s'%(i+1), d)

def addLines(string, width):
    pos, findSpace = 0, 0

    while pos < len(string) - width:
        pos     += width
        findSpace = pos
        
        while string[findSpace - 1] != ' ':
            findSpace -= 1

        string = string[:findSpace] + '\n' + string[findSpace:]

    return string

def getQuote():
    headers = {"Accept": "application/json"}
    url = "https://api.trello.com/1/boards/5b95ec6c86050b153bbc3cc2/cards?key=54d07639427faa733acb9f053875a089&token=95cc4a76b985e33a0b28d9e397a4fd985a7a217bb4d666f81a5f753edc37dc60"
    response = requests.request("GET", url, headers=headers)
    allCards = json.loads(response.text)
    quote = allCards[random.randint(0, len(allCards))]['name']
    if len(quote.split()) == 1:
        quote += ' - ' + define(quote)
    return quote

print(cow(addLines(getQuote(), 50)))
# print(define(input("Enter a word to define: ")))