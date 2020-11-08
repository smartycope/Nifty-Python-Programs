from random_word import RandomWords
import sys

def getRandomWord():
    return RandomWords().get_random_word()

def getWOTD():
    return RandomWords().word_of_the_day()

if ('-d' or '-wotd') in sys.argv:
    print(getWOTD)
else:
    print(getRandomWord())