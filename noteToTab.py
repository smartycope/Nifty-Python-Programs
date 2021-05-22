from tkinter import Tk, IntVar, StringVar
import mido
from tkinter.ttk import *
import math
# import tkFileDialog
from tkinter import filedialog
import re
# import mido

noteOrder = {'E':4, 'F':5, 'G':7, 'A':9, 'B':11, 'C':0, 'D':2}
validNotes = noteOrder.keys()

lengthLimit = 80

error = -2


def checkValid(string:str):
    string.strip()

    if not len(string):
        return None

    notes = inNotes.get().split(' ')

    for cnt, note in enumerate(notes):
        if len(note) != 2 and len(note) != 3:
            return cnt
        if note[0].upper() not in validNotes:
            return cnt
        if not note[1].isnumeric() or int(note[1]) not in range(2, 6):
            return cnt
    return False


def calculateTab(capo):
    global error

    errmsg.set('')
    invalid = checkValid(inNotes.get())
    if invalid is None:
        return None

    elif not invalid:
        notes = inNotes.get().split(' ')

        songLen = (len(notes) * 2) + 5

        strings = {
            'E': '-'*songLen,
            'A': '-'*songLen,
            'D': '-'*songLen,
            'G': '-'*songLen,
            'B': '-'*songLen,
            'e': '-'*songLen
        }


        for pos, note in enumerate(notes):
            fret = getFretNum(note, capo, pos)
            if fret is None:
                printStrings()
                return
            if   isBetween(fret, 0+capo, 4+capo):
                strings['E'] = insertChar(strings['E'], pos * 2, str(fret - capo))
            elif isBetween(fret, 5+capo, 9+capo):
                strings['A'] = insertChar(strings['A'], pos * 2, str(fret - 5 - capo))
            elif isBetween(fret, 10+capo, 14+capo):
                strings['D'] = insertChar(strings['D'], pos * 2, str(fret - 10 - capo))
            elif isBetween(fret, 15+capo, 18+capo):
                strings['G'] = insertChar(strings['G'], pos * 2, str(fret - 15 - capo))
            elif isBetween(fret, 19+capo, 23+capo):
                strings['B'] = insertChar(strings['B'], pos * 2, str(fret - 19 - capo))
            else:
                strings['e'] = insertChar(strings['e'], pos * 2, str(fret - 24 - capo))


        return strings
    else:
        errmsg.set(f"Note {inNotes.get().split(' ')[invalid]}({invalid}) is invalid")
        #* This tells the print funtion to not do anything.
        return ''
        # Put the cursor at the incorrect note
        # errors.append(invalid)
        error = invalid
        # gotoProblem(invalid)
        # textBox.icursor(min([m.start() for m in re.finditer(r" ", inNotes.get())], key=lambda x:abs(x-invalid)))


def constrain(val, low=0, high=10000000):
    return min(high, max(low, val))


def getFretNum(Note:str, capo, notePos=-1):
    global error

    # errmsg.set('')
    octave = int(Note[1])
    # Capitalize the note (so we can recognize a lowercase b)
    if Note[0].islower():
        Note = insertChar(Note, 0, Note[0].upper())

    if   'b' in Note:
        fretNum = -1
    elif '#' in Note:
        fretNum = 1
    else:
        fretNum = 0

    note = Note[0]

    assert(octave >= 2)
    if note not in validNotes:
        errmsg.set(f"{Note}(note {notePos}) is not a valid note!")
        # gotoProblem(notePos)
        error = notePos
        return None

    fretNum += (octave - 2) * 12
    fretNum += noteOrder[note]
    # 4 because the guitar starts at E, not C
    fretNum -= 4

    if not isBetween(fretNum, capo, 47):
        errmsg.set(f"You can't play {Note}(note {notePos}) on the guitar with a capo on fret {capo}")
        # gotoProblem(notePos)
        error = notePos
        return None

    return fretNum


def printStrings(strings=None):
    if strings is None:
        strings = {'E': '-'*5, 'A': '-'*5, 'D': '-'*5, 'G': '-'*5, 'B': '-'*5, 'e': '-'*5}
    elif not len(strings):
        return

    outTab.set('')
    for i in reversed(list(strings.keys())):
        outTab.set(outTab.get() + f'{i} |-')

        for cnt, k in enumerate(strings[i]):
            outTab.set(outTab.get() + str(k))

            # if not cnt % lengthLimit:
            #     outTab.set(outTab.get() + '\n')

        outTab.set(outTab.get() + '\n')


def isBetween(val, start, end, beginInclusive=True, endInclusive=True):
    return (val >= start if beginInclusive else val > start) and \
           (val <= end   if endInclusive   else val < end)


def insertChar(string, index, char):
    return string[:index] + char + string[index+1:]


def decodeMidiNote(num):
    reversedNoteOrder = {6: 'F#', 8: 'G#', 10: 'A#', 1: 'C#', 3: 'D#', 4: 'E', 5: 'F', 7: 'G', 9: 'A', 11: 'B', 0: 'C', 2: 'D'}
    # E2 is 40
    # num -= 40
    octave = math.floor(num / 12) - 1
    note = reversedNoteOrder[num%12]
    return note[0] + str(octave) + (note[1] if len(note) == 2 else '')


def fromFile():
    file = filedialog.askopenfilename()
    # If we hit cancel
    if file is None:
        return

    inNotes.set('')

    mid = mido.MidiFile(file, clip=True)

    def getNotes():
        for i in mid.tracks[[str(i) for i in mid.tracks].index(trackBox.get())]:
            # print(i)
            if type(i) == mido.messages.messages.Message and i.dict()['type'] == 'note_on':
                inNotes.set(inNotes.get() + decodeMidiNote(i.dict()['note']) + ' ')
        win2.destroy()

    # Create a quick track select window
    if len(mid.tracks) > 1:
        win2 = Tk(className='Choose Track')
        Label(win2, text='Which track would you like to import?').pack(side='top')
        trackBox = Combobox(win2, values=[str(i) for i in mid.tracks], width=50)
        trackBox.pack()
        Button(win2, command=getNotes, text='Import').pack(side='bottom')
        win2.bind('<Escape>', lambda e: win2.destroy())
    else:
        for i in mid.tracks[0]:
            if type(i) == mido.messages.messages.Message:
                inNotes.set(inNotes.get() + decodeMidiNote(i.dict()['note']) + ' ')


def gotoProblem():
    global error
    if len(inNotes.get()):
        # invalid = checkValid(inNotes.get())
        textBox.focus_set()
        textBox.icursor(len(' '.join(inNotes.get().split(' ')[:error + 1])))


def save(strings):
    file = filedialog.asksaveasfilename()
    # If we hit cancel
    if file is None:
        return

    with open(file, 'w') as f:
        f.write('\n')
        for i in reversed(list(strings.keys())):
            f.write(str(i) + ' |-')

            for k in strings[i]:
                f.write(k)

            f.write('\n')



win = Tk(className='Note To Tab')

for i in range(5):
    win.grid_columnconfigure(i, weight=0)

fixed = Style()
fixed.configure('Fixed.TButton', font='TkFixedFont')

style = Style()
style.configure("BW.TLabel", foreground="white", background="#31363b", font='TkFixedFont', padding=6, relief="flat")

#* The instructional Text
Label(win, text='Enter space-seperated notes in the form "G2 C3# A1b"', style='BW.TLabel').grid(sticky='n', column=0, columnspan=3, row=0)

#* The Capo on label
Label(win, text='Capo on ', style='BW.TLabel').grid(column=1, row=2, sticky='e')

#* The capo spinbox
capo = IntVar(win, 0)
capoBox = Spinbox(win, textvariable=capo, from_=0, to=12, width=3)
capoBox.grid(column=2, row=2, sticky='w')

#* The input notes box
inNotes = StringVar(win, '')
textBox = Entry(win, textvariable=inNotes, exportselection=False, width=30)
textBox.grid(column=2, row=4, sticky='w')

#* The tab itself
outTab  = StringVar(win, '')
label   = Label(win, textvariable=outTab, style='BW.TLabel')
label.grid(row=6, column=1, sticky='w', columnspan=100)

#* The error message
errmsg  = StringVar(win, '')
errLabel= Label(win, textvariable=errmsg, style='BW.TLabel')
errLabel.grid(sticky='s', row=8, column=2)

#* Import button
importButton = Button(win, command=fromFile, text='Import From File')
importButton.grid(row=9, column=0)

#* Save button
Button(win, command=lambda: save(calculateTab(capo.get())), text='Save Tab').grid(row=9, column=1)

#* Go to error button
Button(win, text='Go to Error', command=lambda: gotoProblem()).grid(row=9, column=3)


win.bind('<Escape>', lambda e: exit(0))

# I don't know what 'w' is, but I'm afraid to touch it.
capo.trace('w',    lambda a, b, c: printStrings(calculateTab(capo.get())))
inNotes.trace('w', lambda a, b, c: printStrings(calculateTab(capo.get())))

win.mainloop()


























"""

print('Enter space-seperated notes in the form "G2 C3# A1b". To specify the capo fret, put the fret number at the beginning.:')

inNotes = input('\n')

notes = inNotes.split(' ')

songLen = (len(notes) * 2) + 5

if len(notes[0]) == 1:
    capo = int(notes[0])
    notes.pop(0)
else:
    capo = 0


strings = {
    'E': '-'*songLen,
    'A': '-'*songLen,
    'D': '-'*songLen,
    'G': '-'*songLen,
    'B': '-'*songLen,
    'e': '-'*songLen
}

noteOrder = {'E':4, 'F':5, 'G':7, 'A':9, 'B':11, 'C':0, 'D':2}
validNotes = noteOrder.keys()


def constrain(val, low=0, high=10000000):
    return min(high, max(low, val))



def getFretNum(Note:str):
    octave = int(Note[1])
    # Capitalize the note (so we can recognize a lowercase b)
    if Note[0].islower():
        Note = insertChar(Note, 0, Note[0].upper())

    if   'b' in Note:
        fretNum = -1
    elif '#' in Note:
        fretNum = 1
    else:
        fretNum = 0

    note = Note[0]

    assert(octave >= 2)
    if note not in validNotes:
        print(f"{Note} is not a valid note!")
        exit(1)

    fretNum += (octave - 2) * 12
    fretNum += noteOrder[note]
    # 4 because the guitar starts at E, not C
    fretNum -= 4

    if not isBetween(fretNum, capo, 47):
        print(f"You can't play {Note} on the guitar with a capo on fret {capo}!")
        exit(1)

    return fretNum


def printStrings():
    print()
<<<<<<< HEAD
    for i in reversed(liststrings.keys())):
=======
    for i in reversed(strings.keys()):
>>>>>>> 01ec8c6b9f04f1b3493592d0b78c7e32064ca9ed
        print(i, ' |-', sep='', end='')

        for k in strings[i]:
            print(k, sep='', end='')

        print()



def isBetween(val, start, end, beginInclusive=True, endInclusive=True):
    return (val >= start if beginInclusive else val > start) and \
           (val <= end   if endInclusive   else val < end)


def insertChar(string, index, char):
    return string[:index] + char + string[index+1:]


for pos, note in enumerate(notes):
    fret = getFretNum(note)
    if   isBetween(fret, 0+capo, 4+capo):
        strings['E'] = insertChar(strings['E'], pos * 2, str(fret - capo))
    elif isBetween(fret, 5+capo, 9+capo):
        strings['A'] = insertChar(strings['A'], pos * 2, str(fret - 5 - capo))
    elif isBetween(fret, 10+capo, 14+capo):
        strings['D'] = insertChar(strings['D'], pos * 2, str(fret - 10 - capo))
    elif isBetween(fret, 15+capo, 18+capo):
        strings['G'] = insertChar(strings['G'], pos * 2, str(fret - 15 - capo))
    elif isBetween(fret, 19+capo, 23+capo):
        strings['B'] = insertChar(strings['B'], pos * 2, str(fret - 19 - capo))
    else:
        strings['e'] = insertChar(strings['e'], pos * 2, str(fret - 24 - capo))


printStrings()
<<<<<<< HEAD
"""
=======
>>>>>>> 01ec8c6b9f04f1b3493592d0b78c7e32064ca9ed
