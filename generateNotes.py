from noteClass import Note
import numpy as np
import random as rand

majorKeyIntervals = [2, 2, 1, 2, 2, 2, 1]
minorKeyIntervals = [2, 1, 2, 2, 1, 2, 2]
bluesKeyIntervals = [2, 1, 2, 1, 1, 2, 1, 1]

def printNotesScale(key, scale):
    for interval in scale:
        print(key)
        key += interval

def createNotesList(key, scale):
    notesList = []
    lowKey = key - sum(scale)
    for i in range(2):
        for j in range(len(scale)):
            notesList.append(lowKey)
            lowKey += scale[j]
    return notesList

keyDict = {0: "A", 1: "A#", 2: "B", 3: "C", 4: "C#", 5: "D", 6: "D#", 7: "E", 8: "F", 9: "F#", 10: "G", 11: "G#"}
def randomKey():
    key = rand.randint(0, 11)
    return keyDict[key]

root = randomKey() + str(rand.randint(0, 6))
key = Note(root)
key = Note("C4")
notesList = createNotesList(key, majorKeyIntervals)
# createMelody(notesList)