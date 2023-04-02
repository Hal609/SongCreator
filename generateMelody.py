from noteClass import Note
import numpy as np
import random as rand
from globals import *

def sumScaleNotes(initial, change, scale):
    sum = 0

    position = initial % len(scale)
    if change < 0:
        sign = -1
    else:
        sign = 1
        position -= 1  # Compensate for asymetry of -1 being first negative wheras 0 is first positive

    for i in range(abs(change)):
        position += 1 * sign
        if position == len(scale):
            position = 0
        if position == -len(scale):
            position = 0

        sum += scale[position] * sign
    return sum

majorKeyIntervals = [2, 2, 1, 2, 2, 2, 1]
def createMelody(key, scale):
    melody = []
    melodyLength = rand.randint(8, 16)
    melodyLength -= melodyLength % 4
    currentNote = key
    scalePos = 0
    for i in range(melodyLength):
        melody.append(currentNote)
        noteChange = int(np.random.normal(0, 3, 1))     # 1 point with mean 0 and sd 1
        currentNote += sumScaleNotes(scalePos, noteChange, scale)
        scalePos += noteChange
    return melody

keyDict = {0: "A", 1: "A#", 2: "B", 3: "C", 4: "C#", 5: "D", 6: "D#", 7: "E", 8: "F", 9: "F#", 10: "G", 11: "G#"}
def randomKey():
    key = rand.randint(0, 11)
    return keyDict[key]

scaleDict = {0: majorKeyIntervals, 1: minorKeyIntervals, 2: bluesKeyIntervals}
def generateMelody():
    root = randomKey() + str(rand.randint(2, 4))
    key = Note(root)
    scaleChoice = rand.randint(0, 2)
    melody = createMelody(key, scaleDict[scaleChoice])

    outputData = ""
    for note in melody:
        outputData += str(note) + ","

    outputFile = open("melody_output.csv", "w")
    outputFile.write(outputData[:-1])
    outputFile.close()

generateMelody()