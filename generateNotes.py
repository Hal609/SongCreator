from noteClass import Note

majorKeyIntervals = [2, 2, 1, 2, 2, 2, 1]
minorKeyIntervals = [2, 1, 2, 2, 1, 2, 2]
bluesKeyIntervals = [2, 1, 2, 1, 1, 2, 1, 1]

def printNotesScale(key, scale):
    for interval in scale:
        print(key)
        key += interval

key = Note("C2")
printNotesScale(key, bluesKeyIntervals)