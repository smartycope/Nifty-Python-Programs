import pyautogui as key
from time import sleep
# import keyboard
import sys

# sys.argv.pop(0)

global currentPickHits
global maxPickHits
global cobbleBreakTime
global torchesLeft
global sidePassageDepth
global lookUpAmount
global lookRightAmount
global moveForwardTime
global sectionSeperation

currentPickHits   = 0
maxPickHits       = 250
cobbleBreakTime   = .45 # .8 is all inclusive
sidePassageDepth  = 8
torchesLeft       = 37
lookUpAmount      = 140
lookRightAmount   = 240
moveForwardTime   = .15 #prev .111
sectionSeperation = 2
sectionAmount     = torchesLeft


def keyHold(which, duration):
    key.keyDown(which)
    sleep(duration)
    key.keyUp(which)

def breakBlock(breakTime):
    # key.mouseDown(x=0, y=0)
    global currentPickHits
    key.mouseDown()
    sleep(breakTime)
    key.mouseUp()
    currentPickHits += 1
    # print(f'The pickaxe has {maxPickHits - currentPickHits} durability left')
    # if keyboard.is_pressed('s'):
    #     exit(0)
    # if keyboard.is_pressed('p'):
    #     keyboard.wait('p')
    # key.mouseUp(x=0, y=0)

def lookUp(amount):
    key.move(0, -amount, .2)

def lookRight(amount):
    key.move(amount, 0, .2)

def moveForwardAndJump():
    key.keyDown('w')
    keyHold('space', .15)
    sleep(moveForwardTime)
    key.keyUp('w')
    # keyHold('space', 0.5)
    # keyHold('w', moveForwardTime)

def wiggle():
    key.keyDown('w')
    keyHold('a', moveForwardTime / 4)
    keyHold('d', moveForwardTime / 4)
    keyHold('d', moveForwardTime / 4)
    keyHold('a', moveForwardTime / 4)
    key.keyUp('w')

def moveForward(blocks = 1):
    # [keyHold('w', moveForwardTime) for _ in range(blocks)]
    for _ in range(blocks):
        keyHold('w', moveForwardTime)
        # sleep(0.1)
        key.press('shift')
    # keyHold('w', moveForwardTime * blocks)

def mineStep(amount = 1):
    for _ in range(amount):
        if torchesLeft == 0:
            key.alert('Out of torches!')
        elif currentPickHits == maxPickHits:
            key.alert('Pick broke!')
        else:
            breakBlock(cobbleBreakTime)
            lookUp(-lookUpAmount)
            breakBlock(cobbleBreakTime + .35)
            lookUp(lookUpAmount)
            moveForward(1)

def mineSection(amount = 1):
    global torchesLeft
    for _ in range(amount):
        # forward one
        mineStep()
        # turn right
        lookRight(lookRightAmount)
        # mine the specified amount
        mineStep(sidePassageDepth)
        if sidePassageDepth > 5:
            key.click(button='right')
            torchesLeft -= 1
        # turn around
        lookRight(-lookRightAmount * 2)
        # go back to the center
        moveForward(sidePassageDepth)
        # mine the specified amount that way
        mineStep(sidePassageDepth)
        if sidePassageDepth > 5:
            key.click(button='right')
            torchesLeft -= 1
        # turn around again
        lookRight(-lookRightAmount * 2)
        # go back to the center again
        moveForward(sidePassageDepth)
        # look forward again
        lookRight(-lookRightAmount)

        breakBlock(cobbleBreakTime)
        lookUp(-lookUpAmount)
        breakBlock(cobbleBreakTime)
        lookUp(lookUpAmount)

        wiggle()

        # mine the seperation
        mineStep(sectionSeperation - 1)
        # add a torch
        lookRight(lookRightAmount)
        key.click(button='right')
        torchesLeft -= 1
        lookRight(-lookRightAmount)

def mineSwath(length, spacing, amount = 1):
    for _ in range(amount):
        mineStep(length)
        key.click(button='right')
        lookRight(lookRightAmount)
        mineStep(spacing)
        lookRight(-lookRightAmount)
        key.click(button='right')
        lookRight(lookRightAmount * 2)
        mineStep(length)
        key.click(button='right')
        lookRight(-lookRightAmount)
        mineStep(spacing)
        lookRight(lookRightAmount)
        key.click(button='right')
        lookRight(-lookRightAmount * 2)


# goToMinecraft()
key.press('f12')
key.press('esc')
# sleep(5) # time to get into position

try:
    mineSwath(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
except:
    mineSwath(int(sys.argv[1]), int(sys.argv[2]))

key.alert('Done!')

# sleep(1)
# moveForward(8)