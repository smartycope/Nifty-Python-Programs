##############################################
# Common Useful Python Functions and Classes #
#                                            #
#  Little things to help you do more things. #
##############################################


#* Color constants for changing the terminal colors - by Mike Stewart - http://MediaDoneRight.com
# Requires: none
class TerminalColors:
    # Reset
    RESET=u"\033[0m"       # Text Reset

    # Regular Colors
    BLACK=u"\033[0;30m"        # Black
    RED=u"\033[0;31m"          # Red
    GREEN=u"\033[0;32m"        # Green
    YELLOW=u"\033[0;33m"       # Yellow
    BLUE=u"\033[0;34m"         # Blue
    PURPLE=u"\033[0;35m"       # Purple
    CYAN=u"\033[0;36m"         # Cyan
    WHITE=u"\033[0;37m"        # White

    # Bold
    BOLD_BLACK=u"\033[1;30m"       # Black
    BOLD_RED=u"\033[1;31m"         # Red
    BOLD_GREEN=u"\033[1;32m"       # Green
    BOLD_YELLOW=u"\033[1;33m"      # Yellow
    BOLD_BLUE=u"\033[1;34m"        # Blue
    BOLD_PURPLE=u"\033[1;35m"      # Purple
    BOLD_CYAN=u"\033[1;36m"        # Cyan
    BOLD_WHITE=u"\033[1;37m"       # White

    # Underline
    UNDERLINE_BLACK=u"\033[4;30m"       # Black
    UNDERLINE_RED=u"\033[4;31m"         # Red
    UNDERLINE_GREEN=u"\033[4;32m"       # Green
    UNDERLINE_YELLOW=u"\033[4;33m"      # Yellow
    UNDERLINE_BLUE=u"\033[4;34m"        # Blue
    UNDERLINE_PURPLE=u"\033[4;35m"      # Purple
    UNDERLINE_CYAN=u"\033[4;36m"        # Cyan
    UNDERLINE_WHITE=u"\033[4;37m"       # White

    # Background
    BACKGROUND_BLACK=u"\033[40m"       # Black
    BACKGROUND_RED=u"\033[41m"         # Red
    BACKGROUND_GREEN=u"\033[42m"       # Green
    BACKGROUND_YELLOW=u"\033[43m"      # Yellow
    BACKGROUND_BLUE=u"\033[44m"        # Blue
    BACKGROUND_PURPLE=u"\033[45m"      # Purple
    BACKGROUND_CYAN=u"\033[46m"        # Cyan
    BACKGROUND_WHITE=u"\033[47m"       # White

    # High Intensty
    INTENSE_BLACK=u"\033[0;90m"       # Black
    INTENSE_RED=u"\033[0;91m"         # Red
    INTENSE_GREEN=u"\033[0;92m"       # Green
    INTENSE_YELLOW=u"\033[0;93m"      # Yellow
    INTENSE_BLUE=u"\033[0;94m"        # Blue
    INTENSE_PURPLE=u"\033[0;95m"      # Purple
    INTENSE_CYAN=u"\033[0;96m"        # Cyan
    INTENSE_WHITE=u"\033[0;97m"       # White

    # Bold High Intensty
    INTENSE_BOLD_BLACK=u"\033[1;90m"      # Black
    INTENSE_BOLD_RED=u"\033[1;91m"        # Red
    INTENSE_BOLD_GREEN=u"\033[1;92m"      # Green
    INTENSE_BOLD_YELLOW=u"\033[1;93m"     # Yellow
    INTENSE_BOLD_BLUE=u"\033[1;94m"       # Blue
    INTENSE_BOLD_PURPLE=u"\033[1;95m"     # Purple
    INTENSE_BOLD_CYAN=u"\033[1;96m"       # Cyan
    INTENSE_BOLD_WHITE=u"\033[1;97m"      # White

    # High Intensty backgrounds
    INTENSE_BACKGROUND_BLACK=u"\033[0;100m"   # Black
    INTENSE_BACKGROUND_RED=u"\033[0;101m"     # Red
    INTENSE_BACKGROUND_GREEN=u"\033[0;102m"   # Green
    INTENSE_BACKGROUND_YELLOW=u"\033[0;103m"  # Yellow
    INTENSE_BACKGROUND_BLUE=u"\033[0;104m"    # Blue
    INTENSE_BACKGROUND_PURPLE=u"\033[10;95m"  # Purple
    INTENSE_BACKGROUND_CYAN=u"\033[0;106m"    # Cyan
    INTENSE_BACKGROUND_WHITE=u"\033[0;107m"   # White

    # Various variables you might want for your PS1 prompt instead
    Time12h=u"\T"
    Time12a=u"\@"
    PathShort=u"\w"
    PathFull=u"\W"
    NewLine=u"\n"
    Jobs=u"\j"

#* Standard color class
# Requires: none
class Color:
    def __init__(self, r = 0, g = 0, b = 0, a = 255):
        self.r = r
        self.g = g
        self.b = b
        self.a = a
        self.color = [self.r, self.g, self.b, self.a]
    
#* Color function for extending the Color class to take named color inputs
# Requires: none
def namedColor(color):
    if color == 'red':
        return Color(255, 0, 0)
    if color == 'blue':
        return Color(0, 0, 255)
    if color == 'green':
        return Color(0, 255, 0)
    if color == 'white':
        return Color(255, 255, 255)
    if color == 'black':
        return Color()

#* Adds lines to a string at a given width, without splitting words
# Requires: none
def addLines(string, width):
    pos, findSpace = 0, 0

    while pos < len(string) - width:
        pos     += width
        findSpace = pos
        
        while string[findSpace - 1] != ' ':
            findSpace -= 1

        string = string[:findSpace] + '\n' + string[findSpace:]

    return string

#* Gets a random quote from my Trello Board.
# Requires: define(), requests, random
def getQuote():
    headers = {"Accept": "application/json"}
    url = "https://api.trello.com/1/boards/5b95ec6c86050b153bbc3cc2/cards?key=54d07639427faa733acb9f053875a089&token=95cc4a76b985e33a0b28d9e397a4fd985a7a217bb4d666f81a5f753edc37dc60"
    response = requests.request("GET", url, headers=headers)
    allCards = json.loads(response.text)
    quote = allCards[random.randint(0, len(allCards))]['name']
    if len(quote.split()) == 1:
        quote += ' - ' + define(quote)
    return quote

#* Centers text given to it based on the width of the terminal. 
# Requires: os
def center(string):
    # return (((os.get_terminal_size().columns - len(string)) / 2) * ' ') + string
    # return string.ljust(int((os.get_terminal_size().columns / 2)))
    for _ in range(int((os.get_terminal_size().columns - len(string)) / 2)): string = ' ' + string
    return string

#* Gets the definition of the given word from the Oxford dictionary
# Requires: requests, json
def define(word):
    # print(word)
    app_id = '4bf3ec4a'
    app_key = '51ef43cee6995c7d2231da8f12729878'

    language = 'en-us'
    fields = 'definitions'
    strictMatch = 'false'

    url = 'https://od-api.oxforddictionaries.com:443/api/v2/entries/' + language + '/' + word.lower() + '?fields=' + fields + '&strictMatch=' + strictMatch

    r = requests.get(url, headers = {'app_id': app_id, 'app_key': app_key})

    #                                                    don't ask me why they make you do this, it's beyond stupid.
    # print(r.json())
    try:
        return r.json()['results'].pop(0)['lexicalEntries'].pop(0)['entries'].pop(0)['senses'].pop(0)['definitions'].pop(0).capitalize()
    except:
        return "Sorry, that's not a word."

#* Gets a random word
# Requires: random_word.RandomWords
def getRandomWord():
    return RandomWords().get_random_word()

#* Gets the "Word of the Day"
# Requires: random_word.RandomWords
def getWOTD():
    return RandomWords().word_of_the_day()




def getNearestIndex(num, l):
    prev, ans = 5000, 0
    # print(l)
    # print(list(range(0, 42)))
    for index, i in enumerate(l):
        if abs(num - i) < prev: # if the number you have is closer to the number you're looking at than it was before...
            prev = abs(num - i)
            ans = index
            # print(ans)
    return ans

def myround(x, base=5):
    return base * round(x/base)

import os
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
    # print(chr(27) + "[2J")
    # pass

def printToFile(stuffToPrint, fileName):
    # os.system('touch ' + fileName)
    with open(fileName, 'w') as file:
        file.write(str(stuffToPrint))

def insert(pattern, index, string):
    return string[:index] + pattern + string[index:]

def delete(pattern, string, amount = 0):
    return string.replace(pattern, '', amount)



