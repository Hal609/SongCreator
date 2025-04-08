import os
import numpy as np
import random as rand
from os import path
from pydub import AudioSegment
import pathlib

from .noteClass import Note
from .globals import *

from .createChordProgression import getChords
from .createDrumTracks import createTrack
from .generateBass import createBass
from .generateMelody import randomKey, generateMelody

from .wavToSpect import wavToSpect

# Load the samples
samplePath = "samples/drums/808/"
kick = AudioSegment.from_file(samplePath + "Kick.aif")
snare = AudioSegment.from_file(samplePath + "Snare.aif")
hihat = AudioSegment.from_file(samplePath + "Hi-Hat.aif")
ride = AudioSegment.from_file(samplePath + "Ride.aif")

def addMelody(note_list, instSamplePath, silence):
    # Create an empty AudioSegment to hold the beat
    audio = AudioSegment.empty()

    # Create the beat based on the beat list
    for i in range(len(note_list)):
        note = Note(note_list[i])
        notePath = instSamplePath + f"{note.get_key_number():02}-{note.note}.wav"
        hit = AudioSegment.from_file(notePath)
        audio += silence
        audio = audio.overlay(hit, position=len(audio)-len(silence))

    return audio

def addChords(key, progression, instSamplePath, silence):
    # Create an empty AudioSegment to hold the beat
    chordsTrack = AudioSegment.empty()

    for i in range(len(progression)):
        progression[i] = str(progression[i])
    newSilence = silence * 8

    for j in range(4):
        # Create the beat based on the beat list
        for i in range(len(progression)):
            root = progression[i].replace("m", "")
            note = Note(root)
            hit = AudioSegment.from_file(instSamplePath + f"{note.get_key_number()}-{note.note}.wav")
            chordsTrack += newSilence
            currentLen = len(chordsTrack)

            chordsTrack = chordsTrack.overlay(hit, position=currentLen-len(newSilence))

            note = Note(root) + 5
            hit = AudioSegment.from_file(instSamplePath + f"{note.get_key_number()}-{note.note}.wav")
            chordsTrack = chordsTrack.overlay(hit, position=currentLen-len(newSilence))

            note = Note(root) + 8
            hit = AudioSegment.from_file(instSamplePath + f"{note.get_key_number()}-{note.note}.wav")
            chordsTrack = chordsTrack.overlay(hit, position=currentLen-len(newSilence))

    return chordsTrack

def addTrack(beat_list, silence):
    global kick, snare, hihat, ride

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

def countCurrentSpectrograms():
    return len([name for name in os.listdir('data/spectrograms')])

def createNMultiInstSpectrograms(n, keepWAVs = False):
    global kick, snare, hihat, ride

    count = countCurrentSpectrograms()

    for i in range(n):
        print(count)
        
        bpm = int(np.random.normal(108, 20, 1)[0])     # 1 point with mean 108 and sd 20

        # Set the duration of each 1/8 beat in milliseconds based on the bpm and duration
        interval = (1/bpm * 60 * 1000) / 2

        silence = AudioSegment.silent(duration=interval)

        totalLength = 12*8

        key = Note(randomKey())

        scaleDict = {0: majorKeyIntervals, 1: minorKeyIntervals, 2: bluesKeyIntervals}
        scaleChoice = scaleDict[rand.randint(0, 2)]

        melodyNotes = generateMelody(key, scaleChoice)

        tracks = [list(np.zeros(12*8))]

        tracks += createTrack(len(tracks[0]))

        fullBeat = addTrack(list(np.zeros(totalLength)), silence)

        chordProgression = getChords(key, scaleChoice)

        bassNotes = createBass(chordProgression)

        fullMelodyNotes = []
        fullBassNotes = []
        for j in range(totalLength):
            nextNote = melodyNotes[j % len(melodyNotes)]
            fullMelodyNotes.append(nextNote)
            fullBassNotes.append(bassNotes[j % len(bassNotes)])
        
        count += 1
        
        num_instruments = rand.randint(2, 5)
        instrumentTracks = {}
        trackPaths = {}
        unused_insts = ["piano", "bass", "drums", "guitar", "synth"]
        used_insts = []
        for k in range(num_instruments):
            # Step 1: Pick an instrument to create a spectrogram for
            inst = rand.choice(unused_insts)
            unused_insts.remove(inst)
            used_insts.append(inst)

            # Step 2: Pick a voice for the chosen instrument
            voice = rand.choice(voices[inst])

            # Step 3: Save the path to the chosen instrument samples
            instSamplePath = f"samples/{inst}/{voice}/"

            if inst == "drums":
                kick = AudioSegment.from_file(instSamplePath + "Kick.wav")
                snare = AudioSegment.from_file(instSamplePath + "Snare.wav")
                hihat = AudioSegment.from_file(instSamplePath + "Hi-Hat.wav")
                ride = AudioSegment.from_file(instSamplePath + "Ride.wav")

            # Step 4: Select what sort of playing to create
            num_items = rand.randint(1, len(parts_can_add[inst]))
            if inst in ["guitar", "bass"]: num_items = 1
            selected_items = rand.sample(parts_can_add[inst], num_items)
            if inst in ["synth", "piano"] and "melody" in selected_items and "chords" in selected_items:
                if rand.random() < 0.5:
                    selected_items.remove("chords")
                else:
                    selected_items.remove("melody")

            if "melody" in selected_items:
                fullBeat = fullBeat.overlay(addMelody(fullMelodyNotes, instSamplePath, silence))
            if "chords" in selected_items:
                fullBeat = fullBeat.overlay(addChords(key, chordProgression, instSamplePath, silence))
            if "bass" in selected_items:
                fullBeat = fullBeat.overlay(addMelody(fullBassNotes, instSamplePath, silence))
            if "drums" in selected_items:
                for beat in tracks:
                    fullBeat = fullBeat.overlay(addTrack(beat, silence))

        filepath = path.dirname(__file__) + f"/../temp/track{count:04}_full.wav"
        fullBeat.export(filepath)
        
        gloPath = pathlib.Path(__file__).parent.resolve()
        newPath = f"{gloPath}/../data/spectrograms/track{count:04}.bmp"
        wavToSpect(filepath, newPath)
        if not keepWAVs: os.remove(filepath)

        # filename,piano,bass,drums,guitar,synth
        res = ""
        for inst in ["piano", "bass", "drums", "guitar", "synth"]:
            if inst in used_insts:
                res += ",0"
            else:
                res += ",1"

        text = f"\ntrack{count:04}.bmp" + res
        with open("data/labels.csv", "a") as csv:
            csv.write(text)

