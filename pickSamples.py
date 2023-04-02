import random as rand
from pydub import AudioSegment
import os

def getRandomSnare():
    path = "/Library/Application Support/Logic/EXS Factory Samples/03 Drums & Percussion/03 Single Drums/02 Snares/Acoustic Snares/"
    choice = rand.randint(1, 33)
    path += f"Acoustic Snare D1 {choice}/"
    files = os.listdir(path)
    sample = files[len(files) // 2]
    return AudioSegment.from_file(path + sample)

def getRandomKick():
    path = "/Library/Application Support/Logic/EXS Factory Samples/03 Drums & Percussion/03 Single Drums/01 Kicks/Acoustic Kicks/"
    choice = rand.randint(1, 31)
    path += f"Acoustic Kick C1 {choice}/"
    files = os.listdir(path)
    sample = files[len(files) // 2]
    return AudioSegment.from_file(path + sample)