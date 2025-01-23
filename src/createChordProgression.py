import random
from .noteClass import Note
from .globals import *

def pickProgression():
    progressions = []
    with open("data/chord_progressions.txt") as chordProgressions:
        for line in chordProgressions:
            line = line.strip("\n")
            progressions.append(line)

    choice = random.randint(0, len(progressions) - 1)
    return progressions[choice]

def getChords(key, scale):
    progression = pickProgression()
    progression = progression.split("-")
    chords = []
    for i in range(0, len(progression)):
        keyInterval = sum(scale[:numeralDict[progression[i]] - 1])
        chords.append(key + keyInterval)
        if progression[i].islower():
            chordString = str(chords[-1])
            chords[-1] = f"{chordString[:-1]}m{chordString[-1]}"
    return chords
