import pyaudio
import numpy as np
import scipy.fftpack
import time

class AudioProcessor:
    def __init__(self, sample_rate=16000, chunk_duration=0.025, total_duration=0.25):
        self.SAMPLE_RATE = sample_rate  # Samples per second
        self.CHUNK_DURATION = chunk_duration  # Duration of each chunk in seconds
        self.TOTAL_DURATION = total_duration  # Total duration to capture in seconds
        self.SAMPLES_PER_CHUNK = int(self.SAMPLE_RATE * self.CHUNK_DURATION)
        self.NUM_CHUNKS = int(self.TOTAL_DURATION / self.CHUNK_DURATION)
        self.FREQ_BANDS = [(100, 300), (300, 600), (600, 1000), (1000, 3000), (3000, 5000), (5000, 8000)]  # Hz

        # Initialize PyAudio
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16,
                                  channels=1,
                                  rate=self.SAMPLE_RATE,
                                  input=True,
                                  frames_per_buffer=self.SAMPLES_PER_CHUNK)

    def get_frequency_band_energy(self, data):
        """Extracts normalized energy levels for predefined frequency bands using FFT."""
        fft_vals = np.abs(scipy.fftpack.fft(data))[:len(data)//2]
        freqs = np.fft.fftfreq(len(data), d=1/self.SAMPLE_RATE)[:len(data)//2]

        band_energies = []
        for (low, high) in self.FREQ_BANDS:
            mask = (freqs >= low) & (freqs < high)
            band_energy = np.sum(fft_vals[mask])
            band_energies.append(min(1, band_energy / 1e6))  # Normalize and cap at 1

        return band_energies

    def get_volume(self, data):
        """Computes normalized RMS volume of audio data."""
        rms = np.sqrt(np.mean(np.square(data)))
        return min(1, rms / 32768)  # Normalize and cap at 1

    def update(self):
        """Captures audio for the total duration and returns volume and band energies for each chunk."""
        volumes = []
        band_energies = [[] for _ in range(len(self.FREQ_BANDS))]

        for _ in range(self.NUM_CHUNKS):
            audio_data = np.frombuffer(self.stream.read(self.SAMPLES_PER_CHUNK, exception_on_overflow=False), dtype=np.int16)
            volume = self.get_volume(audio_data)
            volumes.append(volume)

            energies = self.get_frequency_band_energy(audio_data)
            for i, energy in enumerate(energies):
                band_energies[i].append(energy)

        return volumes, band_energies

    def close(self):
        """Closes the audio stream and terminates PyAudio."""
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

