inNotes = input('Enter space-seperated notes in the form "G2 C3# A1b". To specify the capo fret, put the fret number at the beginning.:\n')

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
    for i in reversed(strings.keys()):
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
