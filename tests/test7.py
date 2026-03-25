import numpy as np
import tikzplot.plots as plt
from tikzplot import Colorbar, TikzConfig

# --- Optional: tweak global config ---
TikzConfig.modifyParam(
    DEFAULT_WIDTH=16,
    DEFAULT_HEIGHT=20,
)

# --- Data ---
x = np.linspace(0, 10, 200)
y = np.sin(x)
y2 = np.cos(x)

noise = np.random.normal(0, 0.2, size=len(x))

# --- Figure with 2x3 subplots ---
fig, axs = plt.subplots(3,2)

# =========================
# (1) Basic plot + styling
# =========================
ax = axs[0, 0]
ax.plot(x, y, color="blue", lw=1.5, label="sin(x)")
ax.plot(x, y2, ls="--", color="red", label="cos(x)")
ax.grid()
ax.legend(loc="upper right")

# =========================
# (2) Scatter + markers
# =========================
ax = axs[0, 1]
sc = ax.scatter(x, y + noise, c="green", marker="o", label="noisy")
ax.grid()

ax2 = ax.twinx()
p1 = ax2.plot([0,10],[0,0], lw=2)
p2 = ax2.plot([0,10],[-1,1])
p3 = ax2.plot([0,10],[1,-1])

ax.legend([p1,p2, p3], ["pl1", "pl2", "pl3"], loc=9, ncols = 2)
# =========================
# (3) Log scale
# =========================
ax = axs[1, 0]
ax.semilogy(x, np.abs(y) + 1e-2, color="purple", label="sin")
ax.grid(which="both")
ax.legend(["$|\\sin(x)|$"])

# =========================
# (4) Errorbar + fill_between
# =========================
ax = axs[1, 1]
x = x[::10]
y = y[::10]
ax.errorbar(x, y, yerr=0.2, fmt="-", color="black", label="data")
ax.fill_between(x, y - 0.1, y + 0.1, alpha=0.3, color="gray")
ax.legend()

# =========================
# (5) Histogram
# =========================
ax = axs[2, 0]
data = np.random.normal(size=1000)
ax.hist(data, bins=30, density=True, cumulative=False, color="orange")

# =========================
# (6) Image + Colorbar
# =========================
ax = axs[2, 1]
X, Y = np.meshgrid(np.linspace(-3, 3, 100), np.linspace(-3, 3, 100))
Z = np.exp(-X**2 - Y**2) - np.exp(-(X - 1)**2 - (Y - 1)**2)

im = ax.imshow(
    Z,
    cmap="viridis",
    origin="lower",
    extent=[-3, 3, -3, 3]
)
ax.grid()

cbar = Colorbar(
    im,
    label="$Z$",
    rel_len=0.8,
    ticks=[-0.5, 0, 0.5],
    horizontal=False
)


# --- Global labels ---
plt.xlabel("X axis")
plt.ylabel("Y axis")

# --- Save ---
plt.savefig("figure.tex")