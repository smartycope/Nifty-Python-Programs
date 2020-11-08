import clipboard, re, sys, select, tty, termios, time
import pyautogui as key
from pynput import keyboard, mouse
# from pynput.keyboard import Key, Controller
# key = Controller()

count = 0
setToAir = False
setToWater = False
dontPaste = False
triggerPressed = False
onlyCoords = False
startLoc = ''
endLoc = ''
blockType = ''
triggerButton = 'g' # Also const


#* Keys
def on_press(key):
    global setToAir, dontPaste, count, triggerPressed, setToWater, onlyCoords
    try:
        # Restart the sequence
        if key.char == 'r':
            count = 1
            print('Sequence restarted')

        # Do everything, but set the block type to be air (and don't automatically paste the command, either)
        elif key.char == 'o': # and count == 1:
            setToAir = True
            print("Type set to air")

        elif key.char == 'p': # and count == 1:
            setToWater = True
            print("Type set to water")

        elif key.char == 'm':
            onlyCoords = not onlyCoords
            count = 0
            print('Only coords toggled to', onlyCoords)

        # Do everything except paste the command automatically
        elif key.char == 'h': # and count == 1:
            dontPaste = True
            c = clipboard.paste()
            print('\"', c, '\"', 'copied to clipboard', sep='')

        elif key.char == triggerButton:
            runStep()
            # if count == 1:
            #     print('Filled from ', startLoc[0], ', ', startLoc[1], ', ', startLoc[2], ' to ',
            #         endLoc[0], ', ', endLoc[1], ', ', endLoc[2], ' with ', blockType[0], sep='')

    except AttributeError:
        pass

#* Mouse
# def on_click(x, y, button, pressed):
#     global triggerPressed
#     # print(button)
#     if button == "Button.middle":
#         runStep()
#         with key.pressed('F3'):
#             key.press('i')
#             key.release('i')

def pasteCommand():
    key.keyUp('F3')
    time.sleep(.06)
    key.press('t')
    time.sleep(.06)
    key.hotkey('ctrl', 'v')
    time.sleep(.06)
    key.press('enter')

def runStep():
    global count, setToAir, dontPaste, triggerPressed, startLoc, endLoc, blockType, setToWater, onlyCoords
    print("COUNT =", count)
    print("running step!")

    key.hotkey("F3", 'i')

    count += 1

    clip = clipboard.paste()
    print(clip)

    try:
        if clip[:9] == '/setblock':
            # print('passed inspection.')
            if count == 1:
                startLoc = re.findall(r'-?\d+', clip)
                if onlyCoords:
                    clipboard.copy(startLoc[0] + ' ' + startLoc[1] + ' ' + startLoc[2])
                print("Starting location set to", startLoc[0] + ' ' + startLoc[1] + ' ' + startLoc[2])

            elif count >= 2:
                endLoc = re.findall(r'-?\d+', clip)
                print('End location set to', endLoc[0] + ' ' + endLoc[1] + ' ' + endLoc[2])

            # Uncomment this line and set steps to 4 to add an extra step to pick the type of block
            # elif count % steps == steps - 1:
                if setToAir:
                    blockType = ['minecraft:air']
                elif setToWater:
                    blockType = ['minecraft:water']
                else:
                    blockType = re.findall(r'([m][i][n][e][c][r][a][f][t][:].+)', clip)

                if not onlyCoords:
                    print('Block type set to', blockType[0])
                    command = "/fill " + startLoc[0] + ' ' + startLoc[1] + ' ' + startLoc[2] + ' ' + endLoc[0] + ' ' + endLoc[1] + ' ' + endLoc[2] + ' ' + blockType[0]
                    if setToAir:
                        command += ' replace'
                    elif setToWater:
                        command += ' destroy'
                    elif not dontPaste:
                        pass
                        # command += ' hollow'

                    clipboard.copy(command)
                    if not dontPaste:
                        pasteCommand()
                    print('\"', command, '\"', ' copied to clipboard.', sep = '')
                else:
                    clipboard.copy(startLoc[0] + ' ' + startLoc[1] + ' ' + startLoc[2] + ' ' + endLoc[0] + ' ' + endLoc[1] + ' ' + endLoc[2])

                dontPaste = False
                setToAir = False
                setToWater = False
                count = 0

    except IndexError:
        print("Invalid clipboard data!")
        key.alert("Invalid clipboard data!")

        # count += 1


#* Non-blocking
# mouseListener = mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll)
# keyboardListener = keyboard.Listener(on_press=on_press, on_release=on_release)

# keyboardListener.start()
# mouseListener.start()

#* Blocking
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()

key.alert("Auto Copy Died!")

# with mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll) as listener:
#     listener.join()


# Lightweight version (just press F3 + i to copy those coords)
'''
import clipboard, re, time

prevClip = ''
while True:
    clip = clipboard.paste()
    if prevClip != clip:
        prevClip = clip
        data = re.search(r'[-]?\d+ [-]?\d+ [-]?\d+', clip)
        if data is not None:
            data = clip[data.span()[0]:data.span()[1]]
            clipboard.copy(data)
    time.sleep(0.1)
'''