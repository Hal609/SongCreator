import random
from noteClass import Note
from globals import *

def pickProgression():
    progressions = []
    with open("chord_progressions.txt") as chordProgressions:
        for line in chordProgressions:
            line = line.strip("\n")
            progressions.append(line)

    choice = random.randint(0, len(progressions) - 1)
    return progressions[choice]

def getChords(key, scale):
    progression = pickProgression()
    progression = progression.split("-")
    chords = [key]
    for i in range(1, len(progression)):
        keyInterval = sum(scale[:numeralDict[progression[i]] - 1])
        chords.append(key + keyInterval)
        if progression[i].islower():
            chordString = str(chords[-1])
            chords[-1] = f"{chordString[:-1]}m{chordString[-1]}"
    return chords
    # for note in chords:
    #     print(note)

key = Note("E3")
getChords(key, bluesKeyIntervals)
