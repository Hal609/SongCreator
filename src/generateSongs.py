import numpy as np
import random as rand
from os import path
from pydub import AudioSegment

from .noteClass import Note
from .globals import *
from .pitchShift import *

from .createChordProgression import getChords
from .createDrumTracks import createTrack
from .generateBass import createBass
from .generateMelody import randomKey, generateMelody


bpm = int(np.random.normal(120, 20, 1)[0])     # 1 point with mean 120 and sd 20

# Set the duration of each 1/8 beat in milliseconds based on the bpm and duration
interval = (1/bpm * 60 * 1000) / 2

silence = AudioSegment.silent(duration=interval)
# silence = AudioSegment.silent(duration=len(silence))

# Load the samples
samplePath = "samples/808/"
kick = AudioSegment.from_file(samplePath + "Kick_1_808Flex.aif")
snare = AudioSegment.from_file(samplePath + "Snare_1_808Flex.aif")
hihat = AudioSegment.from_file(samplePath + "Hi-Hat_808Flex.aif")
ride = AudioSegment.from_file(samplePath + "Ride_808Flex.aif")

def addMelody(note_list):
    global silence

    # Create an empty AudioSegment to hold the beat
    audio = AudioSegment.empty()

    # Create the beat based on the beat list
    for i in range(len(note_list)):
        shift = notesToPitchShift(note_list[i])
        # hit = pitch_shift(lead, shift)
        hit = generate_sine_wave(Note(note_list[i]).get_frequency())
        audio += silence
        audio = audio.overlay(hit, position=len(audio)-len(silence))

    return audio

def addChords(key, progression):
    global silence
    # Create an empty AudioSegment to hold the beat
    chordsTrack = AudioSegment.empty()

    for i in range(len(progression)):
        progression[i] = str(progression[i])
    newSilence = silence * 8

    for j in range(4):
        # Create the beat based on the beat list
        for i in range(len(progression)):
            hit = generate_square_wave(Note(progression[i]).get_frequency())
            chordsTrack += newSilence
            currentLen = len(chordsTrack)

            chordsTrack = chordsTrack.overlay(hit, position=currentLen-len(newSilence))

            hit = generate_square_wave((Note(progression[i]) + 5).get_frequency())
            chordsTrack = chordsTrack.overlay(hit, position=currentLen-len(newSilence))

            hit = generate_square_wave((Note(progression[i]) + 8).get_frequency())
            chordsTrack = chordsTrack.overlay(hit, position=currentLen-len(newSilence))

    return chordsTrack

def notesToPitchShift(note):
    # Find number of steps relative to C3
    dif =  Note(note).get_key_number() - Note("C3").get_key_number()
    return dif


def addTrack(beat_list):
    global silence, kick, snare, hihat, ride

    # Define a dictionary mapping each beat type to its corresponding sample
    beat_samples = {0: silence, 1: kick, 2: snare, 3: hihat, 4: ride}

    # Create an empty AudioSegment to hold the beat
    beat = AudioSegment.empty()

    # Create the beat based on the beat list
    for i in range(len(beat_list)):
        beat_type = beat_list[i]
        hit = beat_samples.get(beat_type)
        beat += silence
        beat = beat.overlay(hit, position=len(beat)-len(silence))

    return beat

def createSong():
    global silence
    
    totalLength = 12*8

    key = Note(randomKey() )
    scaleDict = {0: majorKeyIntervals, 1: minorKeyIntervals, 2: bluesKeyIntervals}
    scaleChoice = scaleDict[rand.randint(0, 2)]

    melodyNotes = generateMelody(key, scaleChoice)

    tracks = [list(np.zeros(12*8))]

    tracks += createTrack(len(tracks[0]))

    fullBeat = addTrack(list(np.zeros(totalLength)))

    chordProgression = getChords(key, scaleChoice)

    bassNotes = createBass(chordProgression)

    fullMelodyNotes = []
    fullBassNotes = []
    for i in range(totalLength):
        nextNote = melodyNotes[i % len(melodyNotes)]
        fullMelodyNotes.append(nextNote)
        fullBassNotes.append(bassNotes[i % len(bassNotes)])

    fullBeat = fullBeat.overlay(addMelody(fullMelodyNotes))
    fullBeat = fullBeat.overlay(addChords(key, chordProgression))

    fullBeat = fullBeat.overlay(addMelody(fullBassNotes))

    for beat in tracks:
        fullBeat = fullBeat.overlay(addTrack(beat))

    # Export the final AudioSegment as a .mp3 file
    filepath = path.dirname(__file__) + f"/../output/output{0}.mp3"
    fullBeat.export(filepath)
