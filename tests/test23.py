import tikzplot.plots as plt
import numpy as np

X, Y = np.meshgrid(np.arange(0, 2 * np.pi, .25), np.arange(0, 2 * np.pi, .25))
U = np.cos(X)
V = np.sin(Y)
M = np.hypot(U, V)
fig, ax = plt.subplots()
ax.quiver(X, Y, U, V, M, scale=0.2, pivot="middle", cmap="jet", alpha=0.5, lw=0.5)
ax.scatter(X,Y, s=50, marker="+", color="black")

plt.savefig("figure.tex")