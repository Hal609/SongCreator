from pydub import AudioSegment
import numpy as np
from noteClass import Note
import generateMelody as grtMel
import random as rand
import createChordProgression as chords
import createDrumTracks as drums
from globals import *
from pickSamples import *
from pitchShift import *

def addMelody(note_list):
    # Create an empty AudioSegment to hold the beat
    audio = AudioSegment.empty()

    # Create the beat based on the beat list
    for i in range(len(note_list)):
        shift = notesToPitchShift(note_list[i])
        hit = pitch_shift(lead, shift)
        hit = generate_square_wave(Note(note_list[i]).get_frequency())
        audio += silence
        audio = audio.overlay(hit, position=len(audio)-len(silence))

    return audio

def addChords(key, progression):
    # Create an empty AudioSegment to hold the beat
    chordsTrack = AudioSegment.empty()

    for i in range(len(progression)):
        progression[i] = str(progression[i])
    newSilence = silence * 8

    for j in range(4):
        # Create the beat based on the beat list
        for i in range(len(progression)):
            shift = notesToPitchShift(progression[i])
            hit = pitch_shift(lead, shift)
            hit = generate_sine_wave(Note(progression[i]).get_frequency())
            chordsTrack += newSilence
            currentLen = len(chordsTrack)

            chordsTrack = chordsTrack.overlay(hit, position=currentLen-len(newSilence))

            shift = notesToPitchShift(str(Note(progression[i]) + 5))
            hit = pitch_shift(lead, shift)
            hit = generate_sine_wave((Note(progression[i]) + 5).get_frequency())
            chordsTrack = chordsTrack.overlay(hit, position=currentLen-len(newSilence))

            shift = notesToPitchShift(str(Note(progression[i]) + 8))
            hit = pitch_shift(lead, shift)
            hit = generate_sine_wave((Note(progression[i]) + 8).get_frequency())
            chordsTrack = chordsTrack.overlay(hit, position=currentLen-len(newSilence))

    return chordsTrack

def notesToPitchShift(note):
    # Find number of steps relative to C3
    dif =  Note(note).get_key_number() - Note("C3").get_key_number()
    return dif


def addTrack(beat_list):
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

for n in range(6):
    # Set the number of kicks and snares in the beat based on bpm and duration
    bpm = 120
    # Set the duration of each 1/8 beat in milliseconds based on the bpm and duration
    interval = (1/bpm * 60 * 1000) / 2

    silence = AudioSegment.silent(duration=interval)

    # Load the samples
    samplePath = "/Library/Application Support/Logic/EXS Factory Samples/03 Drums & Percussion/02 Electronic Drum Kits/808 Flex Kit/"
    kick = getRandomKick()
    snare = getRandomSnare()
    kick = AudioSegment.from_file(samplePath + "Kick_1_808Flex.aif")
    snare = AudioSegment.from_file(samplePath + "Snare_1_808Flex.aif")
    hihat = AudioSegment.from_file(samplePath + "Hi-Hat_808Flex.aif")
    ride = AudioSegment.from_file(samplePath + "Ride_808Flex.aif")
    leadPath =  "/Library/Application Support/Logic/Alchemy Samples/Keys/Acoustic Pianos/Seaward Piano/"
    lead = AudioSegment.from_file(leadPath + "Seaward Piano fff C2.wav")
    # leadPath =  "/Library/Application Support/Logic/Alchemy Samples/Keys/Electric Pianos/Synth Tines/"
    # lead = AudioSegment.from_file(leadPath + "Synth Tines 03.wav")
    # leadPath = "/Library/Application Support/Logic/Alchemy Samples/Guitars/Acoustic Guitars/Acc Guit/"
    # lead = AudioSegment.from_file(leadPath + "Acc Guit C3.wav")


    totalLength = 12*8

    silence = AudioSegment.silent(duration=len(silence))
    key = Note(grtMel.randomKey() )
    scaleDict = {0: majorKeyIntervals, 1: minorKeyIntervals, 2: bluesKeyIntervals}
    scaleChoice = scaleDict[rand.randint(0, 2)]
    melodyNotes = grtMel.generateMelody(key, scaleChoice)
    chords.getChords(key, scaleChoice)

    tracks = [list(np.zeros(12*8))]

    tracks += drums.createTrack(len(tracks[0]))

    fullBeat = addTrack(list(np.zeros(totalLength)))

    fullNotes = []
    for i in range(totalLength):
        nextNote = melodyNotes[i % len(melodyNotes)]
        fullNotes.append(nextNote)

    fullBeat = fullBeat.overlay(addMelody(fullNotes))
    fullBeat = fullBeat.overlay(addChords(key, chords.getChords(key, scaleChoice)))

    for beat in tracks:
        fullBeat = fullBeat.overlay(addTrack(beat))

    # Export the final AudioSegment as a .mp3 file
    fullBeat.export(f"output/output{n}.mp3", format="mp3")