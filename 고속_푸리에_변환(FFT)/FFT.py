import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf
from scipy.signal import butter, lfilter
import librosa
import librosa.display

# Function to design a Butterworth band-pass filter
def butter_bandpass(lowcut, highcut, fs, order=5):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return b, a

# Function to apply a Butterworth band-pass filter
def bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

# Function to compute FFT and PSD
def compute_fft_psd(data, sample_rate):
    n = len(data)
    fhat = np.fft.fft(data, n)
    PSD = fhat * np.conj(fhat) / n
    freq = (1 / (sample_rate * n)) * np.arange(n)
    L = np.arange(1, np.floor(n / 2), dtype='int')
    return fhat, freq, PSD, L

# Load the audio file
input_file = 'output.wav'  # replace with your audio file path
output_file = 'output1.wav'

# Read the audio data
audio_data, sample_rate = sf.read(input_file)
t = np.arange(len(audio_data)) / sample_rate

# Plot the original audio signal
plt.figure()
plt.plot(t, audio_data, color='c', linewidth=1.5, label='Noisy')
plt.title('Original Audio Signal')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')
plt.legend()
plt.show()

# Compute FFT and PSD of the original audio signal
fhat, freq, PSD, L = compute_fft_psd(audio_data, sample_rate)

# Plot the Power Spectral Density (PSD) of the original signal
plt.figure()
plt.plot(freq[L], PSD[L], color='c', linewidth=2, label='Noisy')
plt.title('Power Spectral Density of Original Signal')
plt.xlabel('Frequency [Hz]')
plt.ylabel('Power')
plt.legend()
plt.show()

# Define filter parameters
lowcut = 300.0  # Lower bound of the band-pass filter
highcut = 3400.0  # Upper bound of the band-pass filter

# Apply the band-pass filter to the audio data
filtered_audio_data = bandpass_filter(audio_data, lowcut, highcut, sample_rate, order=6)

# Plot the filtered audio signal
plt.figure()
plt.plot(t, filtered_audio_data, color='b', linewidth=2, label='Filtered')
plt.title('Filtered Audio Signal')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')
plt.legend()
plt.show()

# Compute FFT and PSD of the filtered audio signal
fhat_filtered, freq_filtered, PSD_filtered, L_filtered = compute_fft_psd(filtered_audio_data, sample_rate)

# Plot the Power Spectral Density (PSD) of the filtered signal
plt.figure()
plt.plot(freq_filtered[L_filtered], PSD_filtered[L_filtered], color='b', linewidth=2, label='Filtered')
plt.title('Power Spectral Density of Filtered Signal')
plt.xlabel('Frequency [Hz]')
plt.ylabel('Power')
plt.legend()
plt.show()

# Apply a threshold to the PSD of the filtered signal
threshold = 0.01  # Set an appropriate threshold value
indices = PSD_filtered > threshold
fhat_filtered_cleaned = fhat_filtered.copy()
fhat_filtered_cleaned[:len(indices)][~indices] = 0
fhat_filtered_cleaned[-len(indices):][~indices] = 0

filtered_audio_data_cleaned = np.fft.ifft(fhat_filtered_cleaned).real

# Plot the cleaned filtered audio signal
plt.figure()
plt.plot(t, filtered_audio_data_cleaned, color='g', linewidth=2, label='Cleaned')
plt.title('Cleaned Filtered Audio Signal')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')
plt.legend()
plt.show()

# Apply dynamic range compression using librosa
compressed_audio_data = librosa.effects.percussive(filtered_audio_data_cleaned)

# Apply equalization (simple example: boost mid frequencies)
def apply_eq(data, sample_rate):
    fft_data = np.fft.fft(data)
    frequencies = np.fft.fftfreq(len(fft_data), 1/sample_rate)
    
    # Simple EQ: boost frequencies between 500 Hz and 2000 Hz
    boost_factor = 1.5
    eq_filter = np.ones_like(fft_data)
    eq_filter[(frequencies > 500) & (frequencies < 2000)] *= boost_factor
    
    eq_data = np.fft.ifft(fft_data * eq_filter).real
    return eq_data

eq_audio_data = apply_eq(compressed_audio_data, sample_rate)

# Normalize the audio data
normalized_audio_data = eq_audio_data / np.max(np.abs(eq_audio_data))

# Plot the enhanced audio signal
plt.figure()
plt.plot(t, normalized_audio_data, color='m', linewidth=2, label='Enhanced')
plt.title('Enhanced Audio Signal')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')
plt.legend()
plt.show()

# Save the enhanced audio to a new file
sf.write(output_file, normalized_audio_data, sample_rate)
