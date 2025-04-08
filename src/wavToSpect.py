
import numpy as np
from PIL import Image
import librosa
import soundfile as sf
import torch
import torchaudio


def wavToSpect(wavPath, outputPath):
   n_fft = 16384 # 16384 # 8192 # 4096      # Larger window -> better frequency resolution
   hop_length = 1024 # Step size between windows
   image_height_limit = 2000

   waveform, sr = torchaudio.load(wavPath)  # waveform shape: (channels, time)

   # Convert to a single channel if stereo
   if waveform.shape[0] > 1:
      waveform = torch.mean(waveform, dim=0, keepdim=True)

   # device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
   device = torch.device("mps")
   waveform = waveform.to(device)

   window = torch.hann_window(n_fft).to(device)

   # 3) Compute STFT on GPU
   stft_result = torch.stft(
      input=waveform,
      n_fft=n_fft,
      hop_length=hop_length,
      normalized=False,
      window=window,
      return_complex=True
   )

   # 4) Convert amplitude to dB
   # stft_result shape: (channels, freqs, frames)
   magnitude = stft_result.abs()
   magnitude_db = 20.0 * torch.log10(magnitude + 1e-7)

   # 5) Optionally move back to CPU for plotting
   magnitude_db = magnitude.squeeze().cpu().numpy()  # shape: (freqs, frames)

   to_draw_db = magnitude_db[:image_height_limit]

   db_min = to_draw_db.min()
   db_max = to_draw_db.max()

   clipped_db = np.clip(to_draw_db, db_min, db_max)

   scaled = 255 * ((clipped_db - db_min) / (db_max - db_min))

   scaled_uint8 = scaled.astype(np.uint8)

   img = Image.fromarray(scaled_uint8, mode='L')

   img.save(f"{outputPath}")
   print(f"Saved BMP image to {outputPath}")


def wavToSpectNew(wavPath, outputPath):
   n_fft = 16384 # 16384 # 8192 # 4096      # Larger window -> better frequency resolution
   hop_length = 1024 # Step size between windows

   waveform, sr = torchaudio.load(wavPath)  # waveform shape: (channels, time)

   if waveform.shape[0] > 1:
      waveform = torch.mean(waveform, dim=0, keepdim=True)

   device = torch.device("mps")
   waveform = waveform.to(device)

   window = torch.hann_window(n_fft).to(device)
   
   stft_result = torch.stft(
      input=waveform,
      n_fft=n_fft,
      hop_length=hop_length,
      normalized=False,
      window=window,
      return_complex=True
   )

   magnitude = stft_result.abs()
   magnitude_db = 20.0 * torch.log10(magnitude + 1e-7)

   magnitude_db = magnitude.squeeze().cpu().numpy()  # shape: (freqs, frames)

   np.save(outputPath, magnitude_db)
