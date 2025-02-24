import pyaudio
import numpy as np
import scipy.fftpack
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

# Audio settings
SAMPLE_RATE = 16000  # 16 kHz
CHUNK_DURATION = 0.025  # 25 ms
TOTAL_DURATION = 10  # 10 seconds
SAMPLES_PER_CHUNK = int(SAMPLE_RATE * CHUNK_DURATION)  # 400 samples per chunk
FREQ_BANDS = [(100, 300), (300, 600), (600, 1000), (1000, 3000), (3000, 5000), (5000, 8000)]  # Hz

# Initialize PyAudio
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=SAMPLE_RATE, input=True, frames_per_buffer=SAMPLES_PER_CHUNK)

# Storage for plotting
volume_data = []
band_energy_data = [[] for _ in range(len(FREQ_BANDS))]  # List of lists for each frequency band
time_stamps = []
start_time = time.time()

def get_frequency_band_energy(data, sample_rate):
    """Extracts energy levels for predefined frequency bands using FFT."""
    fft_vals = np.abs(scipy.fftpack.fft(data))[:len(data)//2]  # Compute FFT and take first half
    freqs = np.fft.fftfreq(len(data), d=1/sample_rate)[:len(data)//2]  # Get frequency values

    band_energies = []
    for (low, high) in FREQ_BANDS:
        mask = (freqs >= low) & (freqs < high)
        band_energy = np.sum(fft_vals[mask])  # Sum energy in the band
        band_energies.append(min(1,(band_energy/1e6)))

    
    return band_energies

def get_volume(data):
    """Computes RMS volume of audio data."""
    return min(1,np.sum(data)) # Root Mean Square (RMS) volume

# Setup the plot
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 6))
ax1.set_title("Live Audio Volume")
ax1.set_xlabel("Time (s)")
ax1.set_ylabel("Volume")
line1, = ax1.plot([], [], color="black")

ax2.set_title("Live Frequency Band Energy")
ax2.set_xlabel("Time (s)")
ax2.set_ylabel("Energy")
lines2 = [ax2.plot([], [], label=f"{low}-{high} Hz")[0] for low, high in FREQ_BANDS]
ax2.legend()

def init():
    ax1.set_xlim(0, TOTAL_DURATION)
    ax1.set_ylim(0, 1)
    ax2.set_xlim(0, TOTAL_DURATION)
    ax2.set_ylim(0, 1)  # Adjust if needed
    return [line1] + lines2

def update(frame):
    """Reads audio, processes it, and updates the plot."""
    audio_data = np.frombuffer(stream.read(SAMPLES_PER_CHUNK, exception_on_overflow=False), dtype=np.int16)
    
    band_energies = get_frequency_band_energy(audio_data, SAMPLE_RATE)
    volume = get_volume(band_energies)
    current_time = time.time() - start_time

    # Store data
    volume_data.append(volume)
    time_stamps.append(current_time)
    for i in range(len(FREQ_BANDS)):
        band_energy_data[i].append(band_energies[i])

    # Keep only the last 10 seconds
    if len(time_stamps) > SAMPLE_RATE // SAMPLES_PER_CHUNK * TOTAL_DURATION:
        volume_data.pop(0)
        time_stamps.pop(0)
        for i in range(len(FREQ_BANDS)):
            band_energy_data[i].pop(0)

    # Update plots
    line1.set_data(time_stamps, volume_data)
    for i, line in enumerate(lines2):
        line.set_data(time_stamps, band_energy_data[i])

    return [line1] + lines2

# Start animation
ani = animation.FuncAnimation(fig, update, init_func=init, interval=CHUNK_DURATION * 1000, blit=True)
plt.show()

# Cleanup
stream.stop_stream()
stream.close()
p.terminate()
