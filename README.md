# Nifty-Python-Programs
A collection of small, useful python programs I've written over the years.



# File                             |   Progress                                                              |  Reliability
-----------------------------------|-------------------------------------------------------------------------|------------------------------------------------------
appendFile.py                      |   I think it works?                                                     |  Not to reliable
define.py                          |   Pretty much finished                                                  |  Pretty reliable
eyeglassesconverter.py             |   I don't remember. I don't think it works.                             |  Not at all
balanceChemicalEquationChempy.py   |   Still plenty of bugs, but the hard part is finished                   |  Not a ton, but if it does work, it should be correct
getRandomWord.py                   |   Mostly finished.                                                      |  Mostly reliable
minecraft miner.py                 |   Could use some editing, but to go much further, would be really hard  |  Fairly reliable, once it works
minecraft mineSwath.py             |   Could use some editing, but to go much further, would be really hard  |  Fairly reliable, once it works
minecraft treecapitator.py         |   Could use some editing, but to go much further, would be really hard  |  Pretty reliable, once it works
regex_a_file.py                    |   Far from done.                                                        |  Not reliable at all
getQuote.py                        |   Pretty much done.                                                     |  Very reliable.
monitorKeyboard- boilerplate.py    |   I don't remember. Probably works, but isn't glamorous                 |  Reliable enough.
minecraft copy coords - simple.py  |   Since this is intended to be simple, it's pretty much done.           |  Very reliable
minecraftAutocopyV2.py             |   Doesn't work, tons of bugs, and it really needs to be overhauled      |  Not reliable at all
convertToBinary.py                 |   Doesn't work, but I'm currently working on it. Will work soon         |  Not reliable yet
argparse boilderplate.py           |   Done.                                                                 |  Perfectly reliable
apod.py                            |   Done. If you think of any features to add, let me know                |  Very very reliable
CommonUsefulFunctions.py           |   Could use some touch ups                                              |  Mostly reliable
getPoemOfTheDay.py                 |   Unfinished. Doesn't work yet.                                         |  Not reliable at all


# appendFile.py
This is meant primarily meant to be used in the command line with a pipe to append data to the end of a file. I figure there's probably already a way to do this, but hey, this works.


# define.py
This simply defines a word passed into it. There's a couple command line arguements you can use to do things like get a random word and define it, define the word of the day, and things like that.


# eyeglassesconverter.py
This is a simple script for converting glasses prescriptions into contact prescriptions. I don't remember if it works, and is very limited.


# balanceChemicalEquationChempy.py
This balances chemical equations


# getRandomWord.py
This just gets a random word. That's all it does.


# minecraft miner.py
This uses pyautogui (a python library for sending keystrokes to the computer) to automatically mine a mineshaft in minecraft. It works pretty well, but will most likely require a little bit of tweaking to get it to work the first time. It also doesn't take into account longer breaking times for ore blocks, and the timing might be a tad off, so it's probably not good to leave it alone without supervision. (It will also run into lava)


# minecraft mineSwath.py
Very similar to minecraft miner.py, but only mines in a straight line. Now that I think about it, the two might be swapped. 


# minecraft trecapitator.py
Kind of similar to minecraft miner.py, but automatically cuts "down" 2x2 trees. This works pretty well, actually.


# regex_a_file.py
Replace regular expressions on a file.


# getQuote.py
Gets a quote from my personal quote board, and has a cow say it. Actually pretty reliable, and fun


# monitorKyeboard- boilerplate.py
Boilerplate code for monitoring the keyboard with the pyautogui library 


# minecraft copy coords - simple.py
Run this in the background, and press g to copy the coordinates of the block you're looking at in minecraft. The simple version. 


# minecraftAutocopyV2.py
The 4th is version of being able to copy coordinates in minecraft. The defualt usage is to look at a block, press g, look at another block, press g again, and it will automatically fill the area with the last block you looked at. There's a lot of nice options you can use with it as well. 


# convertToBinary.py
A super nice command line tool for converting numbers in one base system to another. Super useful \when it works\


# argparse boilderplate.py
A little bit of boilderplate code for using argparse, since I keep needing to copy it.


# apod.py
A command line interface for the Astronomy Picture of the day. apod description or apod -d prints the desciption of the picture of the day, apod save or apod -s <filepath> saves the image to the <filepath> location, and apod saveDescription saves the description to a file in the same directory. 


# CommonUsefulFunctions.py
A file full of common useful functions for doing cool things in python. Not meant for direct running, only include this file.


# getPoemOfTheDay.py
Prints the poem of the day.




























