import numpy as np
from PIL import Image
import soundfile as sf
import torch
import torchaudio
import torchaudio.transforms as T
import librosa


def wavToSpect(wavPath, outputPath):
   ''' Creates a spectrogram from a given .wav file.
   A spectrogram shows the different frequencies or pitches 
   that are playing at each point in the song. To do this splits the 
   audio into small time sections (the hop_length sets how long each section is)
   and it splits the frequencies into small section (n_fft sets how many frequency sections there are).
   This creates a grid of pixels where the brighter they are the louder that frequency is
   at the point in the audio.'''
   
   # n_fft is the number of Fast Fourier transforms to apply 
   # basically how many vertical pixels the image will use
   # to show all the frequencies.
   n_fft = 16384   # Larger window -> better frequency resolution
   hop_length = 1024 # Step size between windows
   image_height_limit = 2000

   # Loads the waveform from the .wav with the torchaudio module 
   waveform, sr = torchaudio.load(wavPath)  # waveform shape: (channels, time)

   # # Convert to a single channel if stereo
   # if waveform.shape[0] > 1:
   #    waveform = torch.mean(waveform, dim=0, keepdim=True)

   # Use gpu if available just to speed things up
   # device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
   device = torch.device("mps")
   waveform = waveform.to(device)


   # This torch function does all the actual maths to create the spectrogram
   window = torch.hann_window(n_fft).to(device)
   stft_result = torch.stft(
      input=waveform,
      n_fft=n_fft,
      hop_length=hop_length,
      normalized=False,
      window=window,
      return_complex=True
   )

   # 4) Convert amplitude to dB
   # Interestingly humans hear the volume of sound on a logarithmic scale
   # so a noise that sounds twice as loud to us is actually 10 times the
   # power. Wav files just store the power so this ibrosa.power_to_db
   # function turns that into decibels which follow a logarithmic scale
   # like human hearing. This isn't really required but it makes the 
   # spectrograms look nicer because a pixel that is twice as bright
   # will sound twice as loud to us.
   magnitude = stft_result.abs()
   magnitude_db = 20.0 * torch.log10(magnitude + 1e-7)

   # 5) Move back to CPU for saving
   magnitude_db = magnitude.squeeze().cpu().numpy()[0]  # shape: (freqs, frames)
   
   # This just makes sure that all the loudness values are between 0 and 255
   to_draw_db = magnitude_db[:image_height_limit]
   db_min = to_draw_db.min()
   db_max = to_draw_db.max()
   clipped_db = np.clip(to_draw_db, db_min, db_max)
   scaled = 255 * ((clipped_db - db_min) / (db_max - db_min))

   # Sets the array to 8 bit integers (so values 0 to 255)
   scaled_uint8 = scaled.astype(np.uint8)
   
   # This turns the array into a bmp image so it can be viewed easily
   img = Image.fromarray(scaled_uint8, mode='L')

   # Then it just saves the image to the required output path
   img.save(f"{outputPath}")
   print(f"Saved BMP image to {outputPath}")


def wavToSpectNew(wavPath, outputPath):
   ''' Creates a spectrogram from a given .wav file.
   A spectrogram shows the different frequencies or pitches 
   that are playing at each point in the song. To do this splits the 
   audio into small time sections (the hop_length sets how long each section is)
   and it splits the frequencies into small section (n_fft sets how many frequency sections there are).
   This creates a grid of pixels where the brighter they are the louder that frequency is
   at the point in the audio.'''

   # Loads the waveform from the .wav with the torchaudio module 
   waveform, sr = torchaudio.load(wavPath)  # waveform shape: (channels, time)

   # This is the number of Fast Fourier transforms to apply 
   # basically how many vertical pixels the image will use
   # to show all the frequencies.
   n_fft = 4086

   # This torchaudio function does all the actual maths to make it work
   spectrogram = torchaudio.transforms.Spectrogram(n_fft=n_fft, hop_length=1024)

   # Interestingly humans hear the volume of sound on a logarithmic scale
   # so a noise that sounds twice as loud to us is actually 10 times the
   # power. Wav files just store the power so this ibrosa.power_to_db
   # function turns that into decibels which follow a logarithmic scale
   # like human hearing. This isn't really required but it makes the 
   # spectrograms look nicer because a pixel that is twice as bright
   # will sound twice as loud to us.
   spec = torch.tensor(librosa.power_to_db(spectrogram(waveform)))

   # This just turns the pytorch matrix into a 
   spec = np.array(spec)
   np.save(outputPath, spec[0])


