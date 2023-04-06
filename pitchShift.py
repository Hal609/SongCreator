import numpy as np
from pydub import AudioSegment


def generate_square_wave(frequency, duration=1500, volume=4000):
    # Set the sample rate and duration
    sample_rate = 44100  # 44.1 kHz sample rate
    duration_in_seconds = duration / 1000  # Convert duration from milliseconds to seconds
    
    # Create a numpy array with the square wave
    t = np.linspace(0, duration_in_seconds, int(sample_rate * duration_in_seconds), False)
    note_wave = volume * np.sign(np.sin(frequency * 2 * np.pi * t))
    
    # Convert numpy array to pydub AudioSegment
    note_wave = np.array(note_wave, np.int16)
    note_segment = AudioSegment(note_wave.tobytes(), frame_rate=sample_rate, channels=1, sample_width=2)

    return note_segment


def generate_sine_wave(frequency, duration=1500, volume=4000):
    # Set the sample rate and duration
    sample_rate = 44100  # 44.1 kHz sample rate
    duration_in_seconds = duration / 1000  # Convert duration from milliseconds to seconds
    
    # Create a numpy array with the sine wave
    t = np.linspace(0, duration_in_seconds, int(sample_rate * duration_in_seconds), False)  
    note_wave = volume * np.sin(frequency * 2 * np.pi * t)
    
    # Convert numpy array to pydub AudioSegment
    note_wave = np.array(note_wave, np.int16)
    note_segment = AudioSegment(note_wave.tobytes(), frame_rate=sample_rate, channels=1, sample_width=2)

    return note_segment

def pitch_shift(sound, n_half_steps):
    '''Function which takes a pydub AudioSegment and a number of half steps and
    returns a new pytdub AudioSegment with the frequency shifted by that number
    of half steps'''

    octaves = n_half_steps / 12
    new_sample_rate = int(sound.frame_rate * (2.0 ** octaves))
    newpitch_sound = sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})

    return newpitch_sound
