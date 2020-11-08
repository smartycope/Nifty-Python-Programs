import pyautogui as key
from time import sleep
import sys

# sys.argv.pop(0)
treeHeight = 25
upOnly, downOnly = bool(), bool()

for i in sys.argv[1:]:
    if i.isdigit():
        treeHeight = int(i)
    elif i == '-up':
        upOnly = True
    elif i == '-down':
        downOnly = True
    else:
        print('Error: invalid command line params')
        exit(0)



key.FAILSAFE = True

_debug = False

'''
Usage notes:
place yourself in front of a 2x2 super tree,
facing front & center of the left block holding an iron
axe. Call this program, and then you have 5 seconds to
get back to minecraft. Don't inturrupt the tree cutting
process, or it will mess it up. There's also no easy way to stop it, as of yet, other than going back to
the terminal and pressing ctrl+c.

Also:
 options/controls/mouse settings/raw input must be set to off
 and minecraft must be maximized, but not fullscreen.

'''

woodBreakTime = .68
moveForwardTime = .1
treeHeight = 25

lookHeight = 180
lookLength = 240

def keyHold(which, duration):
    key.keyDown(which)
    sleep(duration)
    key.keyUp(which)

def breakBlock():
    # key.mouseDown(x=0, y=0)
    key.mouseDown()
    sleep(woodBreakTime)
    key.mouseUp()
    # key.mouseUp(x=0, y=0)

def lookUp(amount):
    key.move(0, -amount, .2)

def lookDown():
    key.move(0, lookHeight * 2, .2)

def lookRight(amount):
    key.move(amount, 0, .2)

def moveForwardAndJump():
    key.keyDown('w')
    keyHold('space', .15)
    sleep(moveForwardTime)
    key.keyUp('w')
    # keyHold('space', 0.5)
    # keyHold('w', moveForwardTime)

'''
def goToMinecraft():
    key.press('F12')
    key.hotkey('alt', 'shift', 'tab')
    key.keyDown('alt')
    sleep(0.5)
    key.keyDown('tab')
    sleep(0.5)
    # key.hotkey('alt', 'tab')

    tooMany = 0
    restart = True
    while restart:
        try:
            key.click('MinecraftTab.png')
            key.keyUp('tab')
            restart = False
            print("Found the tab")
        except:
            tooMany += 1
            if tooMany > 5:
                print("Didn't find the minecraft tab, giving up")
                exit(0)
            print('Didn\'t find the minecraft tab, trying again')
            key.keyUp('tab')
            key.press('tab')
            key.press('tab')

    key.keyUp('alt')
'''


# goToMinecraft()
key.press('f12')
key.press('esc')
# sleep(2) # time to get into position

def upTheTree():
    breakBlock()
    lookUp(lookHeight)
    breakBlock()
    # lookUp()
    breakBlock()
    lookUp(-lookHeight)
    moveForwardAndJump()
    tmp = treeHeight
    while tmp:
        print("Starting on level", tmp)
        breakBlock()
        lookUp(lookHeight)
        breakBlock()
        # lookUp()
        breakBlock()
        lookUp(-lookHeight)
        moveForwardAndJump()
        lookRight(lookLength)
        tmp -= 1


def downTheTree():
    tmp = treeHeight
    while tmp:
        print("Starting on level", tmp)
        breakBlock()
        lookRight(-lookLength)
        tmp -= 1

if upOnly:
    upTheTree()
elif downOnly:
    downTheTree()
else:
    upTheTree()
    downTheTree()

key.alert("Timber!")