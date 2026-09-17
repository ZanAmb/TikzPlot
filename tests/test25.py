import numpy as np
import tikzplot.plots as plt

np.random.seed(42)
Fs = 1000.0
t = np.arange(0, 2.0, 1 / Fs)

x = np.sin(2 * np.pi * 50 * t) + 0.5 * np.random.randn(len(t))
y = np.sin(2 * np.pi * 50 * t + np.pi / 4) + 0.5 * np.random.randn(len(t))

fig, axs = plt.subplots(2, 2, figsize=(12, 8))

axs[0, 0].acorr(x, maxlags=50, normed=True, usevlines=True, color="tab:blue")
axs[0, 0].set_title("ax.acorr(x)")
axs[0, 0].set_xlabel("Lags")
axs[0, 0].grid(True)

axs[0, 1].xcorr(x, y, maxlags=50, normed=True, usevlines=True, color="tab:green")
axs[0, 1].set_title("ax.xcorr(x, y)")
axs[0, 1].set_xlabel("Lags")
axs[0, 1].grid(True)

axs[1, 0].csd(x, y, NFFT=256, Fs=Fs, noverlap=128, color="tab:purple")
axs[1, 0].set_title("ax.csd(x, y)")
axs[1, 0].grid(True)

axs[1, 1].cohere(x, y, NFFT=256, Fs=Fs, noverlap=128, color="tab:red")
axs[1, 1].set_title("ax.cohere(x, y)")
axs[1, 1].grid(True)

plt.savefig("figure.tex")