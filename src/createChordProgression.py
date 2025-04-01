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
    print("Key:", key, " Scale:", scale)
    print("Progression:", progression)
    chords = []
    for i in range(0, len(progression)):
        print(f"Progression {i}: {progression[i]}")
        print("Numeral dict:", numeralDict[progression[i]])
        print("scale[:numercaldict-1]", scale[:numeralDict[progression[i]] - 1])
        keyInterval = sum(scale[:numeralDict[progression[i]] - 1])
        print("keyInterval", keyInterval)
        chords.append(key + keyInterval)
        if progression[i].islower():
            chordString = str(chords[-1])
            chords[-1] = f"{chordString[:-1]}m{chordString[-1]}"
    return chords
