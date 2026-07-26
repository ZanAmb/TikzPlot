import tikzplot.plots as plt
import numpy as np

x = np.linspace(0, 10, 100)
y = np.sin(x) * np.exp(-x / 5)

fig, ax = plt.subplots(figsize=(8, 5))

ax.plot(
    x,
    y,
    color="#00ffcc",
    linewidth=2.5,
    label="Signal Decay"
)

ax.plot(x, y, color="#00ffcc", linewidth=6, alpha=0.3)

text_color = "#ffffff"

ax.set_title(
    "Data Over the Horizon")
ax.set_xlabel("Time (s)")
ax.set_ylabel("Amplitude")

ax.legend(
    facecolor="none", edgecolor=text_color, labelcolor=text_color
)

plt.tight_layout()

plt.savefig("transparent_graph.png")