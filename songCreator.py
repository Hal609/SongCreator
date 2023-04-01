from pydub import AudioSegment
import numpy as np
import librosa

def pitch_shift(sound, n_half_steps):
    octaves = n_half_steps / 12

    new_sample_rate = int(sound.frame_rate * (2.0 ** octaves))

    lowpitch_sound = sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})

    # y = np.frombuffer(sound._data, dtype=np.int16).astype(np.float32)/2**15
    # y = librosa.effects.pitch_shift(y, sound.frame_rate, n_steps=n_steps)
    # a  = AudioSegment(np.array(y * (1<<15), dtype=np.int16).tobytes(), frame_rate = sound.frame_rate, sample_width=2, channels = 1)
    return lowpitch_sound

def addMelody(note_list):
    # Create an empty AudioSegment to hold the beat
    audio = AudioSegment.empty()

    # Create the beat based on the beat list
    for i in range(len(note_list)):
        # beat_type = beat_list[i]
        if i < 4:
            hit = lead
        else:
            hit = pitch_shift(lead, 4)
        audio += silence
        audio = audio.overlay(hit, position=len(audio)-len(silence))

    return audio

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

# Set the number of kicks and snares in the beat based on bpm and duration
bpm = 120
# Set the duration of each 1/8 beat in milliseconds based on the bpm and duration
interval = (1/bpm * 60 * 1000) / 2

silence = AudioSegment.silent(duration=interval)

# Load the samples
samplePath = "/Library/Application Support/Logic/EXS Factory Samples/03 Drums & Percussion/02 Electronic Drum Kits/808 Flex Kit/"
kick = AudioSegment.from_file(samplePath + "Kick_1_808Flex.aif")
snare = AudioSegment.from_file(samplePath + "Snare_1_808Flex.aif")
hihat = AudioSegment.from_file(samplePath + "Hi-Hat_808Flex.aif")
ride = AudioSegment.from_file(samplePath + "Ride_808Flex.aif")
leadPath =  "/Library/Application Support/Logic/Alchemy Samples/Keys/Electric Pianos/EPiano FM Classic/"
lead = AudioSegment.from_file(leadPath + "EPiano FM Classic C3.wav")
silence = AudioSegment.silent(duration=len(silence))


tracks = [
    [1, 0, 2, 2, 0, 0, 2, 0, 1, 0, 2, 2, 0, 0, 2, 0],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
]


fullBeat = addTrack(list(np.zeros(len(tracks[0]))))

noteTrack = list(np.zeros(len(tracks[0])))
for i in range(len(noteTrack)):
    noteTrack[i] = "A4"
fullBeat = fullBeat.overlay(addMelody(noteTrack))

for beat in tracks:
    fullBeat = fullBeat.overlay(addTrack(beat))

# Export the final AudioSegment as a .mp3 file
fullBeat.export("/Users/hal/Documents/PythonScripts/SongCreator/output.mp3", format="mp3")