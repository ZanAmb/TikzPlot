import math

import numpy as np
import tikzplot.plots as plt
from tikzplot import Colorbar, TikzConfig

TikzConfig.modifyParam(MAX_POINTS_PER_ELEMENT=10000, STANDALONE=True)
# TikzConfig.modifyParam(DEFAULT_HEIGHT=10, DEFAULT_WIDTH=5)

gamma = np.vectorize(math.gamma)
fig = plt.figure()

# 1) fill-between + twinx
ax1 = fig.add_subplot(2, 2, 1)
x = np.linspace(0, 10, 300)
y1 = np.sin(x) + 1.5
y2 = 0.35 * np.cos(x) + 0.8
ax1.plot(x, y1, color="orange", linewidth=1.2, ls="-.", label="$f_1$")
ax1.plot(x, y2, color="teal", linewidth=1.2, label="$f_2$")
ax1.fill_between(x, y1, y2, color="blue", alpha=0.35, label="area")
ax1.set(xlabel="$x$", ylabel="$y_1$", xlim=(0, 10))
ax1.grid(True)
ax1.legend(loc="upper right", ncols=3)
ax1.grid(which="minor", linestyle=":", alpha=0.5)
ax1.set_minorticks_num(4)

ax1r = ax1.twinx()
x = x[::50]
ax1r.errorbar(x, 2*np.exp(-x / 3), fmt="bo", yerr=0.5*np.exp(-x / 2.5), linewidth=1.5, ms=1)
ax1r.set_ylim(0.05, 10)
ax1r.set_yscale("log")
ax1r.set_ylabel("$y_2$")

# 2) histogram + line plot
ax2 = fig.add_subplot(2, 2, 2)
data = np.random.normal(loc=0.0, scale=1.0, size=2000)
counts, bins = np.histogram(data, bins=30)
bin_centers = 0.5 * (bins[:-1] + bins[1:])
ax2.hist(data, bins=bins, color="gray", alpha=0.55)
ax2.plot(bin_centers, counts, color="black")
ax2.set(xlabel="value", ylabel="count", xlim=(-4, 4), ylim=(0, 200))

# 3) imshow + colorbar
ax3 = fig.add_subplot(2, 2, 3)
dx, dy = 0.05, 0.05

x = np.arange(-3.0, 3.0, dx)
y = np.arange(-3.0, 3.0, dy)
X, Y = np.meshgrid(x, y)
Z2 = (1 - X / 2 + X**5 + Y**3) * np.exp(-(X**2 + Y**2))
im = ax3.imshow(Z2, origin="lower", cmap="seismic", aspect="auto")
Colorbar(im, rel_len=0.75, label=r"$\gamma$")
ax3.set(xlabel="$x$", ylabel="$y$")
ax3.grid()

# 4) existing 3D plot
ax4 = fig.add_subplot(2, 2, 4, projection="3d")

N = 31
x = np.linspace(0.0, 10.0, N)
lambdas = list(reversed(range(1, 10)))

cmap = Colorbar(axis=ax4, cmap="gist_rainbow", lower=1, upper=10, rel_len=0.8, divisions=9)
facecolors = [cmap.color(l) for l in lambdas]

for i, l in enumerate(lambdas):
    ax4.fill_between(
        x,
        l,
        l**x * np.exp(-l) / gamma(x + 1),
        x,
        l,
        0,
        color=facecolors[i],
        alpha=0.5,
    )

ax4.set(
    xlim=(0, 10),
    ylim=(1, 9),
    zlim=(0, 0.35),
    xlabel="$x$",
    ylabel=r"$\lambda$",
    zlabel="probability",
)

plt.savefig("demo.tex")