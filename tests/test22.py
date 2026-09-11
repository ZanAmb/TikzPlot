import tikzplot.plots as plt
import numpy as np

Fs = 1000.0  # Sampling rate = 1000 Hz
t = np.linspace(0, 2.0, int(2.0 * Fs), endpoint=False)

# Signal components:
# - 50 Hz wave running continuously
# - 150 Hz wave starting at t = 1.0s with a phase offset
# - Random white noise across all frequencies
sig_50hz = np.sin(2 * np.pi * 50 * t)
sig_150hz = np.where(t >= 1.0, 0.6 * np.sin(2 * np.pi * 150 * t + np.pi/3), 0.0)
noise = 0.25 * np.random.default_rng(42).standard_normal(len(t))

x = sig_50hz + sig_150hz + noise

# 2. Setup 3x2 Grid Plot
fig, axes = plt.subplots(3, 2, figsize=(14, 10))

# Panel 0: Raw Time-Domain Signal
axes[0, 0].plot(t, x, color="tab:blue", lw=0.8)
axes[0, 0].set_title("Raw Time-Domain Signal $x(t)$")
axes[0, 0].set_xlabel("Time (s)")
axes[0, 0].set_ylabel("Amplitude")
axes[0, 0].grid(True, alpha=0.3)

# Panel 1: Magnitude Spectrum
axes[0, 1].magnitude_spectrum(x, Fs=Fs, color="tab:orange")
axes[0, 1].set_title("1. Magnitude Spectrum (`magnitude_spectrum`)")
axes[0, 1].grid(True, alpha=0.3)

# Panel 2: Angle Spectrum (Wrapped)
axes[1, 0].angle_spectrum(x, Fs=Fs, color="tab:green")
axes[1, 0].set_title(r"2. Angle Spectrum - Wrapped $[-\pi, \pi]$ (`angle_spectrum`)")
axes[1, 0].grid(True, alpha=0.3)

# Panel 3: Phase Spectrum (Unwrapped)
axes[1, 1].phase_spectrum(x, Fs=Fs, color="tab:red")
axes[1, 1].set_title("3. Phase Spectrum - Unwrapped (`phase_spectrum`)")
axes[1, 1].grid(True, alpha=0.3)

# Panel 4: Spectrogram (STFT)
Pxx, freqs, bins, im = axes[2, 0].specgram(x, Fs=Fs, NFFT=256, noverlap=128, cmap="viridis")
axes[2, 0].set_title("4. Spectrogram (`specgram`)")
axes[2, 0].set_xlabel("Time (s)")
axes[2, 0].set_ylabel("Frequency (Hz)")
fig.colorbar(im, ax=axes[2, 0], label="Power (dB)")

# Panel 5: Power Spectral Density (PSD)
axes[2, 1].psd(x, Fs=Fs, NFFT=256, noverlap=128, color="tab:purple")
axes[2, 1].set_title("5. Power Spectral Density (`psd`)")
axes[2, 1].grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("figure.tex")